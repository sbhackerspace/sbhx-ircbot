#!/usr/bin/env python
# Steve Phillips / elimisteve
# 2011.03.21

import feedparser, socket, time

#
# Connection Info
#
USER = 'sbhx_github'
botname     = USER #+ "_bot"
network     = 'irc.freenode.net'
chatchannel = '#sbhackerspace'

port = 6667
end = '\n'

premess = 'PRIVMSG ' + chatchannel + ' :'
irc = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
irc.connect( ( network, port ) )
print irc.recv( 4096 )
irc.send( 'NICK ' + botname + end )
irc.send( 'USER ' + USER + 'bot botty bot bot: Python IRC' + end )
irc.send( 'JOIN ' + chatchannel + end )

#
# Helper Functions
#
def irc_msg(msg):
    """Sends msg to channel"""
    irc.send(premess + msg + end)
    return

def getuser():
    """Returns nick of current message author"""
    try:
        #user = data.split()[2].strip(':')
        #user = data.split()[0].split('~')[0].strip(':!')
        user = data.split()[0].split('!')[0].strip(':')
    except:
        user = data.split('!')[0].strip(':')
    return user

#
# GitHub
#
account_name = 'sbhackerspace'
branch = 'master'
repo_names = ['sbhx-snippets',
              'sbhx-ircbot', 'sbhx-rov', 'sbhx-sicp']
              #'sbhx-androidapp', 'sbhx-projecteuler'
              ## These two don't get parsed correctly for some reason...
              #]
SLEEP_SECONDS = float(60*2.4)/len(repo_names)  # Check each repo once/couple minutes

def check_github():
    old_version = {}
    for repo in repo_names:
        old_version[repo] = feedparser.parse(
            'https://github.com/' + account_name +
            '/' + repo + '/commits/' + branch + '.atom'
            )

    time.sleep(SLEEP_SECONDS)  # Wait then compare

    for repo in repo_names:
        new = feedparser.parse('https://github.com/' + account_name +
                               '/' + repo + '/commits/' + branch + '.atom')
        try:
            if new.entries[0] != old_version[repo].entries[0]:
                #author = new.entries[0].author.split()[0]  # First name
                author = new.entries[0].author_detail.href.split('/')[-1]
                commit_msg = new.entries[0].title
                print '\n'
                print "[" + repo + "] " + author + ": " + commit_msg
                print '\n'
                irc_msg("[" + repo + "] " + author + ": " + commit_msg)
        except:
            print "GitHub fucked up, I think. Here's what they gave us:"
            print new
#
# Main loop
#
while True:
   data = irc.recv ( 4096 )
   datasp = data.split(' :')[0]
   datasp = str(datasp)

   username = getuser()
#   inc_utter_counts()

   if 'PING' in data:
      irc.send( 'PONG ' + data.split()[1] + end )

   print data
   check_github()
