import socket, urllib2, re, os
from datetime import datetime

USER = 'elimisteve'
auto_connect = True

bot_default     = USER + "_bot"
network_default = 'irc.freenode.net'
chan_default    = '#sbhackerspace'

if not auto_connect:
    botname = raw_input('Say my name! (' + bot_default + ') ')
    if not botname:
        botname = bot_default

    network = raw_input('IRC network? (' + network_default + ') ')
    if not network:
        network = network_default

    chatchannel = raw_input('Channel Name (' + chan_default + ') #')
    if not chatchannel:
        chatchannel = chan_default
else:
    chatchannel = chan_default
    network = network_default
    botname = bot_default

# Detect platform
# Windows needs \r\n, Linux just needs \n
# if 'win' in os.uname()[0].lower():
#     end = '\r\n'
# else:
end = '\n'

shit_on = True
shitlist = """
Microsoft Windows iOS Apple Camarillo Ventura Russia China
""".split()

profanity_on = True
profanity = """
fuck shit bitch asshole cunt tits twat fag dick
""".split()

#scripting project projects PCBs
good_on = True
goodlist = """
Android Python Django Ruby Rails Clojure Bash Linux Emacs
Dropbox Wikileaks infosec DEFCON BSD hacking BackTrack
Gentoo Slackware 
""".split()

start_time = str(datetime.now())[:16]

port = 6667

premess = 'PRIVMSG ' + chatchannel + ' :'
irc = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
irc.connect( ( network, port ) )
print irc.recv( 4096 )
irc.send( 'NICK ' + botname + end )
irc.send( 'USER ' + USER + 'bot botty bot bot: Python IRC' + end )
irc.send( 'JOIN ' + chatchannel + end )

# Used to store messages users leave for one another
left_messages = {}
priv_messages = {}

# Dictionaries of the form d == {'username1': 4, 'username2': 17}
utter_counts = {}
bot_response_counts = {}

# DO NOT CONFUSE THIS WITH irc.msg
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

def timescrapes():
    """Sends current time in given city to IRC channel"""
    html = urllib2.urlopen('http://www.timeanddate.com/worldclock/').read()
    local = 'Los Angeles'
    city = data.split(':!time')[1].strip('\r\n ')
    print "city = ", city
    if not city:
        city = local
    city = ' '.join([word.capitalize() for word in city.split()]) #cap words
    print "city = ", city
    time = html.split(city)[1].split('>')[3].split('<')[0]
    irc_msg(time)
    return

def timescrapes24():
    """Sends current time in given city to IRC channel"""
    html = urllib2.urlopen('http://www.timeanddate.com/worldclock/').read()
    local = 'Los Angeles'
    city = data.split(':!time24')[1].strip('\r\n ')
    if not city:
        city = local
    city = ' '.join([word.capitalize() for word in city.split()]) #cap words
    time = html.split(city)[1].split('>')[3].split('<')[0]
    if time.split()[2] == 'PM':
        hours = int(time.split()[1].split(':')[0]) + 12
        minutes = time.split()[1].split(':')[1]
        time = ' '.join([time.split()[0], str(hours) + ':' + str(minutes)])
    else:
        time = ' '.join(time.split()[:2])
    irc_msg(time)
    #str(datetime.now())[:16].split()[1]
    return


loadfile = "projectlinks.txt"
i = 0
def read():
    """Reads local db"""
    dbfile = open(loadfile, 'r')
    dbold = dbfile.read()
    dbfile.seek(0)
    for line in dbfile:
        irc_msg(line)
    dbfile.seek (0)
    dbfile.close()

def empty():
    """Empties local db"""
    dbfile = open(loadfile, 'w')
    dbfile.close()

def writea():
    """Write given project info to local db"""
    dbfile = open(loadfile, 'r')
    dbold = dbfile.read()
    dbfile.close()
    link = data.split(':!project add')[1]
    link = username + str(link)
    dbfile = open(loadfile, 'w')
    dbfile.write(link + str(dbold))
    dbfile.close()

def inc_bot_response_counts():
    pass
   # try:
   #     bot_response_counts[username] += 1
   # except:
   #     #bot_response_counts[username] = 1
   #     print "inc_bot_response_counts is broken"

def inc_utter_counts():
    pass
   # try:
   #     utter_counts[username] += 1
   # except:
   #     #utter_counts[username] = 1
   #     print "inc_utter_counts is broken"


while True:
   data = irc.recv ( 4096 )
   datasp = data.split(' :')[0]
   datasp = str(datasp)

   username = getuser()
   inc_utter_counts()

   if 'PING' in data:
      irc.send( 'PONG ' + data.split()[1] + end )

   if ':!quit' in data.lower():
       irc_msg("I am immortal.")

   if ':!time' in data:
       if ':!time24' in data:
           try:
               timescrapes24()
           except:
               irc_msg("Error try: !time <city> ex. !time Berlin")
       else:
           try:
               timescrapes()
           except:
               irc_msg("Error try: !time <city> ex. !time Berlin")


   if ':!project' in data:
      if ':!project read' in data:
          try: read()
          except: irc_msg("Could not read")

      if ':!project empty' in data:
          empty()

      if ':!project add' in data:
          writea()

   if 'KICK' in data:
      irc.send( 'JOIN ' + chatchannel + end )

   # Return URLs to Google search queries
   if ':!google ' in data:
       query = data.split(':!google ')[1].strip().replace(' ','+')
       search = "http://www.google.com/search?q=" + query
       irc_msg(search)

   if ':!lucky ' in data:
       try:
           query = data.split(':!lucky ')[1].strip().replace(' ','+')
       except:
           irc_msg("!lucky <search_term>")
       search = "http://www.google.com/search?btnI=I'm+Feeling+Lucky&q=" + query
       irc_msg(search)

   if ':!wikilink ' in data:
       url = data.split(':!wikilink ')[1]
       html = urllib2.urlopen('http://sbhackerspace.com/wiki/index.php?title=Links&action=edit').read()
       textarea = re.findall(r'<textarea.*>(.*)</textarea>', html, re.DOTALL)[0]
       appended_data = end + '* ' + url
       new_textarea = textarea + appended_data
       print new_textarea
   print data

   # Save messages to a dictionary of the form
   # dict['recipient'] = ['message 1', 'message 2', 'message 3']
   if ':!msg ' in data:
       try:
           recip, msg = data.split(':!msg ')[1].strip("\r\n ").split(' ', 1)
       except:
           #irc_msg("Notice: " + username + " can't get anything right.")
           irc_msg("Options: !time <city>, !msg <recipient> <message>, " + \
                       "!privmsg <recipient> <message>")
       date, time = str(datetime.now())[:16].split()
       try:
           msg += " (from " + username + " at " + time + " on " + date + ")"
       except:
           msg = username + ' tried to crash the bot. Bastard.'
       try:
           left_messages[recip].append(msg)
       except KeyError:
           left_messages[recip] = []
           left_messages[recip].append(msg)
       except:
           pass
           #irc_msg(username + ' is trying to kill me!')

   # Send messages to user but only if they say something in
   # the channel, not because they've joined, quit, etc
   if username in left_messages and 'ACTION' not in data \
           and 'QUIT' not in data and 'JOIN' not in data \
           and 'KICK' not in data:
       utter_counts = len(left_messages[username])
       irc_msg(username + ' has ' + str(utter_counts) + ' message(s)! ')
       for m in range(utter_counts):
           irc_msg(left_messages[username][m])
       del left_messages[username]

   if ':!privmsg ' in data:
       try:
           recip, msg = data.split(':!privmsg ')[1].strip("\r\n ").split(' ', 1)
       except:
           irc_msg("Options: !time <city>, !msg <recipient> <message>, " + \
                       "!privmsg <recipient> <message>")
           msg = ""
       date, time = str(datetime.now())[:16].split()  # Ghetto, but works
       msg += " (from " + username + " at " + time + " on " + date + ")"
       try:
           priv_messages[recip].append(msg)
       except KeyError:
           priv_messages[recip] = []
           priv_messages[recip].append(msg)
       except:
           irc_msg(username + 'fucked up my code. Bastard.')

   # if ':!privmsg ' in data:
   #     try:
   #         recip, msg = data.split(':!privmsg ')[1].strip("\r\n ").split(' ', 1)
   #     except:
   #         irc_msg("Options: !time <city>, !msg <recipient> <message>, " + \
   #                     "!privmsg <recipient> <message>")
   #     date, time = str(datetime.now())[:16].split()  # Ghetto, but works
   #     msg += " (from " + username + " at " + time + " on " + date + ")"
   #     try:
   #         priv_messages[recip].append(msg)
   #     except KeyError:
   #         priv_messages[recip] = []
   #         priv_messages[recip].append(msg)
   #     except:
   #         irc_msg(username + 'fucked up my code. Bastard.')

   # if username in priv_messages:
   #     utter_counts = len(priv_messages[username])
   #     irc.send('PRIVMSG ' + username + ' : You have ' +
   #              str(utter_counts) + ' private message(s):' + end)
   #     for m in range(utter_counts):
   #         irc.send('PRIVMSG ' + username + ' : ' + priv_messages[username][m] + end)
   #     del priv_messages[username]

   if '_bot' not in username.lower():
       if profanity_on:
           for word in profanity:
               if word.lower() in data.lower() and \
                       'motherfucker' not in data.lower():
                   irc_msg('Hey ' + username + ': watch your mouth, motherfucker')
                   inc_bot_response_counts()
                   break
       if shit_on:
           for word in shitlist:
               if word.lower() in data.lower() and \
                       'radioshack' not in data.lower():
                   irc_msg('Notice: ' + username +
                           ' is a dipshit for mentioning ' + word)
                   inc_bot_response_counts()
                   break
       if good_on:
           for word in goodlist:
               if word.lower() in data.lower():
                   irc_msg('Notice: ' + username +
                           ' is redeemed for mentioning ' + word)
                   inc_bot_response_counts()
                   break

   if ':!wiki ' in data:
       page = data.split(':!wiki ')[1]
       url = "http://sbhackerspace.com/wiki/index.php?title="
       irc_msg(url + page)
       inc_bot_response_counts()

   if ':!help' in data:
       irc_msg("Slut.")
       irc_msg("Options: !time <city>, !msg <recipient>, !privmsg <recipient>")
       #irc_msg("More: !")
       inc_bot_response_counts()

   # if username == 'paul_be' or username == 'm0tan':
   #     irc_msg('Hey ' + username + ', am I annoying yet?')

   # if username == 'elimisteve':
   #     irc_msg('STFU ' + username + '!')

   if ':!members' in data:
       member_list = []
       #url = data.split(':!members')[1]
       html = urllib2.urlopen('http://sbhackerspace.com/wiki/index.php?title=Members&action=edit').read()
       textarea = re.findall(r'<textarea.*>(.*)</textarea>', html, re.DOTALL)[0]
       for line in textarea.split('\n'):
           member_list.append(line.split(',')[0].split()[-1].replace(']', ''))
       irc_msg('Current Members (from wiki): ' + ', '.join(member_list))
       inc_bot_response_counts()

   # if ':!stats' in data:
   #     irc_msg("Since " + start_time)
   #     irc_msg("----------------------")
   #     irc_msg("Total Speakers: %d" % len(utter_counts))
   #     total_utter = sum([utter_counts[nick] for nick in utter_counts])
   #     irc_msg("Total Utterances: %d" % total_utter)
   #     total_bot_utter = sum([bot_response_counts[nick]
   #                            for nick in bot_response_counts])
   #     irc_msg("Total Bot Responses: %d" % total_bot_utter)
   #     nick_width = max([len(nick) for nick in utter_counts])
   #     irc_msg("") # Blank line
   #     irc_msg("Nick%sMsg Count" % (' ' * nick_width))
   #     irc_msg("%s" % ('-' * (nick_width+13)))
   #     for nick in utter_counts:
   #         irc_msg(nick + ' ' + str(utter_counts[nick]))
   #     inc_bot_response_counts()

   if ":!userlist" in data:
       irc_msg("/userlist")

   if ':!ircbot ' in data:
       url = data.split(':!ircbot ')[1]
       html = urllib2.urlopen('http://stevendphillips.com/ircbot/@edit/index').read()
       textarea = re.findall(r'<textarea.*>(.*)</textarea>', html, re.DOTALL)[0]
       print textarea
       print '\n\n\n\n'
       appended_data = '* ' + url
       new_textarea = textarea + appended_data
       # HTTP POST
       for line in [line.strip() for line in new_textarea.split('\n')]:
           irc_msg(line)

   if ':!echo ' in data:
       msg = data.split(':!echo ')[1]
       irc_msg(msg)

   if ':!shitlist ' in data:
       cmd = data.split(':!shitlist ')[1].strip()
       if cmd.lower() == 'off':
           shit_on = False
       elif cmd.lower() == 'on':
           shit_on = True
       else:
           irc_msg("You said: " + cmd.lower())
           irc_msg("shitlist enabled? " + str(shit_on))
           irc_msg("!shitlist on|off")

   if ':!goodlist ' in data:
       cmd = data.split(':!goodlist ')[1].strip('\r\n ')
       if cmd.lower() == 'off':
           good_on = False
       elif cmd.lower() == 'on':
           good_on = True
       else:
           irc_msg("!goodlist on|off")
           
   if ':!profanity ' in data:
       cmd = data.split(':!profanity ')[1].strip('\r\n ')
       if cmd.lower() == 'off':
           profanity_on = False
       elif cmd.lower() == 'on':
           profanity_on = True
       else:
           irc_msg("!profanity on|off")
