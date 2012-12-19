// Steve Phillips / elimisteve
// 2011.03.25

package main

import (
	"fmt"
	"github.com/elimisteve/ddg"
	"github.com/elimisteve/fun"
	"log"
	"net"
	"strings"
)

const (
	IRC_SERVER         = "irc.freenode.net:6667"

	BOT_NICK           = "sbhx_gobot"
	IRC_CHANNEL        = "#sbhackerspace"
	THIS_SERVER_NAME   = "home?"
	VERBOSE            = true

	// REPO_BASE_PATH     = "/home/ubuntu/django_projects/"
	REPO_BASE_PATH     = "/home/steve/sbhx/"
	OWNER_NICK         = "elimisteve"

	PRIVMSG_PRE        = "PRIVMSG "
	PRIVMSG_POST       = " :"
	IRC_CHAN_MSG_PRE   = PRIVMSG_PRE + IRC_CHANNEL + PRIVMSG_POST
	REPO_INDEX_FILE    = ".index" // Deprecated
	GIT_PORT           = "6666"
	// WEBHOOK_PORT       = "7777"
	LOCAL_GITHUB_REPOS = "/home/steve/sbhx/"
	REVENGE_MSG        = "I never forgive. I never forget."
)

var NICKS_TO_NOTIFY = []string{"elimisteve", "elimisteve1", "elimisteve11",
                               "elimisteve12"}

type GitCommit struct {
	Author string
	Email string
	Repo string
	RepoOwner string
	Message string
	Date string
	Hash string
}

func checkError(where string, err error) {
	if err != nil {
		log.Fatalf(where + ": " + err.Error())
	}
}

// Only one connection allowed (subject to change)
var conn net.Conn

// Anything passed to this channel is echoed into IRC_CHANNEL
var irc = make(chan string)

// IRC nicks to seek revenge against
var revenge = []string{}

func main() {
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
		for { ircMsg(<-irc) }
	}()

	//
	// Main loop
	//
	read_buf := make([]byte, 512)
	for {
		// n bytes read
		n, err := conn.Read(read_buf)
		checkError("conn.Read", err)
		rawData := string(read_buf[:n])
		rawData = strings.TrimRight(rawData, " \t\r\n") // Remove trailing whitespace
		fmt.Printf("%v\n", rawData)
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
		// Thank user when given OP... then seek revenge
		// TODO: Use regex to parse `rawData`
		if strings.Contains(rawData, "MODE " + IRC_CHANNEL + " +o " + BOT_NICK) {
			irc <- nick + ": thanks :-)"
			for _, user := range revenge {
				rawIrcMsg("KICK " + IRC_CHANNEL + " " + user + " :" + REVENGE_MSG)
			}
			revenge = []string{}
		}
		// Seek revenge on those who remove bot's OP
		// TODO: Use regex to parse `rawData`
		if strings.Contains(rawData, "MODE " + IRC_CHANNEL + " -o " + BOT_NICK) {
			irc <- ":-("
			revenge = append(revenge, nick)
		}
		//
		// Re-join if kicked
		//
		if fun.ContainsAllStrings(rawData, "KICK", BOT_NICK) {
			rawIrcMsg("JOIN " + IRC_CHANNEL)
			revenge = append(revenge, nick)
		}
		//
		// Respond to queries for word definitions using DuckDuckGo
		//
		if strings.HasPrefix(msg, "!define ") {
			query := msg[1:]
			resp, err := ddg.ZeroClick(query)
			if err != nil {
				irc <- fmt.Sprintf("Error querying DuckDuckGo: %v\n", err)
			} else {
				irc <- fmt.Sprintf("%s: %s\n", query, resp.Abstract)
			}
		}
		//
		// Response to DuckDuckGo queries
		//
		if strings.HasPrefix(msg, "!ddg ") {
			resp, err := ddg.ZeroClick(msg[len("!ddg "):])
			if err != nil {
				irc <- fmt.Sprintf("Error querying DuckDuckGo: %v\n", err)
			} else {
				irc <- fmt.Sprintf("DuckDuckGo: %s\n", resp.Abstract)
			}
		}
		//
		// ADD YOUR CODE (or function calls) HERE
		//
	}
}

func ircSetup() net.Conn {
	var err error
	// Avoid the temptation... `conn, err := ...` silently shadows the
	// global `conn` variable!
	conn, err = net.Dial("tcp", IRC_SERVER)
	checkError("net.Dial", err)

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

// privMsg is a helper function that wraps rawIrcMsg, prefacing each
// message with IRC_CHAN_MSG_PRE (usually `PRIVMSG $IRC_CHANNEL `)
func privMsg(nickOrChannel, msg string) {
	rawIrcMsg(PRIVMSG_PRE + nickOrChannel + PRIVMSG_POST + msg)
}

func privMsgOwner(msg string) {
	privMsg(OWNER_NICK, msg)
}
