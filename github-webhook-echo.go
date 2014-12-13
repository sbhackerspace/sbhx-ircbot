// Steve Phillips / elimisteve
// Created 2011.03.25
// Updated 2014.12.12

package main

import (
	"encoding/json"
	"fmt"
	"io/ioutil"
	"log"
	"net"
	"net/http"
	"strings"

	"github.com/elimisteve/fun"
)

const (
	IRC_SERVER = "irc.freenode.net:6667"

	BOT_NICK    = "sbhx_github"
	IRC_CHANNEL = "#sbhackerspace"

	PRIVMSG_PRE      = "PRIVMSG "
	PRIVMSG_POST     = " :"
	IRC_CHAN_MSG_PRE = PRIVMSG_PRE + IRC_CHANNEL + PRIVMSG_POST
	GITHUB_PORT      = "9000"
)

// Only one connection allowed (subject to change)
var conn net.Conn

// Anything passed to this channel is echoed into IRC_CHANNEL
var irc = make(chan string)

func main() {
	go webhookListener()

	// If the constants are valid, this program cannot crash. Period.
	defer func() {
		if err := recover(); err != nil {
			msg := fmt.Sprintf("Recovered from nasty error in main: %v\n", err)
			// ircMsg(msg)
			fmt.Print(msg)
		}
	}()

	// Connect to IRC
	conn = ircSetup()
	defer conn.Close()

	// Anything passed to the `irc` channel (get it?) is echoed into
	// IRC_CHANNEL
	go func() {
		for {
			ircMsg(<-irc)
		}
	}()

	//
	// Main loop
	//
	b := make([]byte, 512)
	for {
		// n bytes read
		n, err := conn.Read(b)
		if err != nil {
			log.Printf("Error reading conn; reconnecting. Err: %v\n", err)
			conn.Close()
			conn = ircSetup()
			continue
		}

		rawData := string(b[:n])
		rawData = strings.TrimRight(rawData, " \t\r\n") // Remove trailing whitespace
		log.Printf("%v\n", rawData)
		//
		// Respond to PING
		//
		if strings.HasPrefix(rawData, "PING") {
			rawIrcMsg("PONG " + rawData)
			continue
		}
		//
		// Parse nick, msg
		//

		// Avoids ~global var risk by resetting these to "" each loop
		var msg, nick = "", ""

		// Parse nick when safe to do so
		// TODO: Look at IRC spec; not sure this is guaranteed to work
		if fun.ContainsAnyStrings(rawData, "PRIVMSG", "MODE", "JOIN", "KICK") {
			// structure of `rawData` == :nick!host PRIVMSG #channel :msg

			// nick == everything after first char, before first !
			nick = strings.SplitN(rawData[1:], "!", 2)[0]
			fmt.Printf("Nick: '%v'\n", nick)
		}
		// Parse msg when safe to do so
		// TODO: Make this much more precise
		if fun.ContainsAnyStrings(rawData, "PRIVMSG", "KICK") {
			// msg == everything after second :
			msg = strings.SplitN(rawData, ":", 3)[2]
			fmt.Printf("Message: '%v'\n", msg)
		}

		//
		// `nick` and `msg` now (probably) defined
		//

		//
		// Re-join if kicked
		//
		if fun.ContainsAllStrings(rawData, "KICK", BOT_NICK) {
			rawIrcMsg("JOIN " + IRC_CHANNEL)
		}
	}
}

func ircSetup() net.Conn {
	var err error
	// Avoid the temptation... `conn, err := ...` silently shadows the
	// global `conn` variable!
	conn, err = net.Dial("tcp", IRC_SERVER)
	if err != nil {
		log.Fatalf("Error connecting to %s: %v\n", IRC_SERVER, err)
	}

	rawIrcMsg("NICK " + BOT_NICK)
	rawIrcMsg("USER " + strings.Repeat(BOT_NICK+" ", 4))
	rawIrcMsg("JOIN " + IRC_CHANNEL)
	return conn
}

// rawIrcMsg takes a string and writes it to the global TCP connection
// to the IRC server _verbatim_
func rawIrcMsg(str string) {
	conn.Write([]uint8(str + "\n"))
}

// ircMsg is a helper function that wraps rawIrcMsg, prefacing each
// message with IRC_CHAN_MSG_PRE (usually `PRIVMSG $IRC_CHANNEL `)
func ircMsg(msg string) {
	rawIrcMsg(IRC_CHAN_MSG_PRE + msg)
}

//
//
// Listen for GitHub pushes
//
//

// webhookListener listens on GITHUB_PORT (default: 9000) for JSON
// HTTP POSTs, parses the relevant data, then sends it over a channel
// to a function waiting for strings to echo into IRC_CHANNEL
func webhookListener() {
	http.HandleFunc("/", webhookHandler)
	log.Printf("Listening on port %v...\n", GITHUB_PORT)
	log.Fatal(http.ListenAndServe(":"+GITHUB_PORT, nil))
}

func webhookHandler(w http.ResponseWriter, r *http.Request) {
	defer r.Body.Close()
	body, err := ioutil.ReadAll(r.Body)
	if err != nil {
		log.Printf("Error in webhookHandler: %v\n", err)
		return
	}

	push := &GithubPush{}
	err = json.Unmarshal(body, push)
	if err != nil {
		log.Printf("Error unmarshaling \n\n%s\n\n -- %v\n", body, err)
		return
	}

	summary := push.SummarizeHeadCommit()
	log.Printf("Echoing this summary to IRC:\n%s\n\n", summary)
	ircMsg(summary)
}

func (push *GithubPush) SummarizeHeadCommit() string {
	head := push.HeadCommit

	name := head.Committer.Name
	username := head.Committer.Username
	repo := push.Repository.FullName
	msg := head.Message
	url := head.Url

	return fmt.Sprintf(
		`%s (%s) just pushed %d commit(s) to %s. Latest: %q. %v`,
		name, username, len(push.Commits), repo, msg, url)
}

type GithubPush struct {
	Ref     string      `json:"ref"`
	Before  string      `json:"before"`
	After   string      `json:"after"`
	Created bool        `json:"created"`
	Deleted bool        `json:"deleted"`
	Forced  bool        `json:"forced"`
	BaseRef interface{} `json:"base_ref"`
	Compare string      `json:"compare"`
	Commits []struct {
		Id        string `json:"id"`
		Distinct  bool   `json:"distinct"`
		Message   string `json:"message"`
		Timestamp string `json:"timestamp"`
		Url       string `json:"url"`
		Author    struct {
			Name     string `json:"name"`
			Email    string `json:"email"`
			Username string `json:"username"`
		} `json:"author"`
		Committer struct {
			Name     string `json:"name"`
			Email    string `json:"email"`
			Username string `json:"username"`
		} `json:"committer"`
		Added    []string      `json:"added"`
		Removed  []interface{} `json:"removed"`
		Modified []interface{} `json:"modified"`
	} `json:"commits"`
	HeadCommit struct {
		Id        string `json:"id"`
		Distinct  bool   `json:"distinct"`
		Message   string `json:"message"`
		Timestamp string `json:"timestamp"`
		Url       string `json:"url"`
		Author    struct {
			Name     string `json:"name"`
			Email    string `json:"email"`
			Username string `json:"username"`
		} `json:"author"`
		Committer struct {
			Name     string `json:"name"`
			Email    string `json:"email"`
			Username string `json:"username"`
		} `json:"committer"`
		Added    []string      `json:"added"`
		Removed  []interface{} `json:"removed"`
		Modified []interface{} `json:"modified"`
	} `json:"head_commit"`
	Repository struct {
		Id       int    `json:"id"`
		Name     string `json:"name"`
		FullName string `json:"full_name"`
		Owner    struct {
			Name  string `json:"name"`
			Email string `json:"email"`
		} `json:"owner"`
		Private          bool        `json:"private"`
		HtmlUrl          string      `json:"html_url"`
		Description      string      `json:"description"`
		Fork             bool        `json:"fork"`
		Url              string      `json:"url"`
		ForksUrl         string      `json:"forks_url"`
		KeysUrl          string      `json:"keys_url"`
		CollaboratorsUrl string      `json:"collaborators_url"`
		TeamsUrl         string      `json:"teams_url"`
		HooksUrl         string      `json:"hooks_url"`
		IssueEventsUrl   string      `json:"issue_events_url"`
		EventsUrl        string      `json:"events_url"`
		AssigneesUrl     string      `json:"assignees_url"`
		BranchesUrl      string      `json:"branches_url"`
		TagsUrl          string      `json:"tags_url"`
		BlobsUrl         string      `json:"blobs_url"`
		GitTagsUrl       string      `json:"git_tags_url"`
		GitRefsUrl       string      `json:"git_refs_url"`
		TreesUrl         string      `json:"trees_url"`
		StatusesUrl      string      `json:"statuses_url"`
		LanguagesUrl     string      `json:"languages_url"`
		StargazersUrl    string      `json:"stargazers_url"`
		ContributorsUrl  string      `json:"contributors_url"`
		SubscribersUrl   string      `json:"subscribers_url"`
		SubscriptionUrl  string      `json:"subscription_url"`
		CommitsUrl       string      `json:"commits_url"`
		GitCommitsUrl    string      `json:"git_commits_url"`
		CommentsUrl      string      `json:"comments_url"`
		IssueCommentUrl  string      `json:"issue_comment_url"`
		ContentsUrl      string      `json:"contents_url"`
		CompareUrl       string      `json:"compare_url"`
		MergesUrl        string      `json:"merges_url"`
		ArchiveUrl       string      `json:"archive_url"`
		DownloadsUrl     string      `json:"downloads_url"`
		IssuesUrl        string      `json:"issues_url"`
		PullsUrl         string      `json:"pulls_url"`
		MilestonesUrl    string      `json:"milestones_url"`
		NotificationsUrl string      `json:"notifications_url"`
		LabelsUrl        string      `json:"labels_url"`
		ReleasesUrl      string      `json:"releases_url"`
		CreatedAt        int         `json:"created_at"`
		UpdatedAt        string      `json:"updated_at"`
		PushedAt         int         `json:"pushed_at"`
		GitUrl           string      `json:"git_url"`
		SshUrl           string      `json:"ssh_url"`
		CloneUrl         string      `json:"clone_url"`
		SvnUrl           string      `json:"svn_url"`
		Homepage         string      `json:"homepage"`
		Size             int         `json:"size"`
		StargazersCount  int         `json:"stargazers_count"`
		WatchersCount    int         `json:"watchers_count"`
		Language         string      `json:"language"`
		HasIssues        bool        `json:"has_issues"`
		HasDownloads     bool        `json:"has_downloads"`
		HasWiki          bool        `json:"has_wiki"`
		HasPages         bool        `json:"has_pages"`
		ForksCount       int         `json:"forks_count"`
		MirrorUrl        interface{} `json:"mirror_url"`
		OpenIssuesCount  int         `json:"open_issues_count"`
		Forks            int         `json:"forks"`
		OpenIssues       int         `json:"open_issues"`
		Watchers         int         `json:"watchers"`
		DefaultBranch    string      `json:"default_branch"`
		Stargazers       int         `json:"stargazers"`
		MasterBranch     string      `json:"master_branch"`
		Organization     string      `json:"organization"`
	} `json:"repository"`
	Pusher struct {
		Name  string `json:"name"`
		Email string `json:"email"`
	} `json:"pusher"`
	Organization struct {
		Login            string `json:"login"`
		Id               int    `json:"id"`
		Url              string `json:"url"`
		ReposUrl         string `json:"repos_url"`
		EventsUrl        string `json:"events_url"`
		MembersUrl       string `json:"members_url"`
		PublicMembersUrl string `json:"public_members_url"`
		AvatarUrl        string `json:"avatar_url"`
	} `json:"organization"`
	Sender struct {
		Login             string `json:"login"`
		Id                int    `json:"id"`
		AvatarUrl         string `json:"avatar_url"`
		GravatarId        string `json:"gravatar_id"`
		Url               string `json:"url"`
		HtmlUrl           string `json:"html_url"`
		FollowersUrl      string `json:"followers_url"`
		FollowingUrl      string `json:"following_url"`
		GistsUrl          string `json:"gists_url"`
		StarredUrl        string `json:"starred_url"`
		SubscriptionsUrl  string `json:"subscriptions_url"`
		OrganizationsUrl  string `json:"organizations_url"`
		ReposUrl          string `json:"repos_url"`
		EventsUrl         string `json:"events_url"`
		ReceivedEventsUrl string `json:"received_events_url"`
		Type              string `json:"type"`
		SiteAdmin         bool   `json:"site_admin"`
	} `json:"sender"`
}
