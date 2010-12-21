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
if 'win' in os.uname()[0].lower():
    end = '\r\n'
else:
    end = '\n'

#iPhone Mac 
shitlist = """
Microsoft Windows iOS Apple Camarillo Ventura Russia China Karuption
""".split()

# piss
profanity = """
fuck shit bitch asshole cunt tits twat 
""".split()

#scripting project projects PCBs
goodlist = """
Android Python Django Ruby Rails Clojure Bash Linux Emacs
Dropbox EFF Wikileaks infosec DEFCON 
""".split()

port = 6667

premess = 'PRIVMSG ' + chatchannel + ' :'
irc = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
irc.connect( ( network, port ) )
print irc.recv( 4096 )
irc.send( 'NICK ' + botname + end )
irc.send( 'USER ' + USER + 'bot botty bot bot: Python IRC' + end )
irc.send( 'JOIN ' + chatchannel + end )

# Used to store messages users leave for one another
messages = {}
priv_messages = {}

# DO NOT CONFUSE THIS WITH irc.msg
def irc_msg(msg):
    """Sends msg to channel"""
    irc.send(premess + msg + end)
    return

def getuser():
    """Returns nick of current message author"""
    try:
        #user = data.split()[2].strip(':')
        user = data.split()[0].split('~')[0].strip(':!')
    except:
        user = data.split('!')[0].strip(':')
    return user

def timescrapes():
    """Sends current time in given city to IRC channel"""
    html = urllib2.urlopen('http://www.timeanddate.com/worldclock/').read()
    local = 'Los Angeles'
    city = data.split(':!time')[1].strip("\r\n ")
    if not city:
        city = local
    city = ' '.join([word.capitalize() for word in city.split()]) #cap words
    time = html.split(city)[1].split('>')[3].split('<')[0]
    irc_msg(time)
    return

def timescrapes24():
    """Sends current time in given city to IRC channel"""
    html = urllib2.urlopen('http://www.timeanddate.com/worldclock/').read()
    local = 'Los Angeles'
    city = data.split(':!time24')[1].strip("\r\n ")
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

while True:
   data = irc.recv ( 4096 )
   datasp = data.split(' :')[0]
   datasp = str(datasp)

   username = getuser()

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
   if ':!google' in data:
       query = data.split(':!google')[1].strip().replace(' ','+')
       search = "http://www.google.com/search?q=" + query
       irc_msg(search)

   if ':!wikilink ' in data:
       url = data.split(':!wikilink ')[1]
       html = urllib2.urlopen('http://sbhackerspace.com/wiki/index.php?title=Links&action=edit').read()
       text_area = re.findall(r'<textarea.*>(.*)</textarea>', html, re.DOTALL)[0]
       appended_data = end + '* ' + url
       new_text_area = text_area + appended_data
       print new_text_area
   print data

   # Save messages to a dictionary of the form
   # dict['recipient'] = ['message 1', 'message 2', 'message 3']
   if ':!msg' in data:
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
           messages[recip].append(msg)
       except KeyError:
           messages[recip] = []
           messages[recip].append(msg)
       except:
           pass
           #irc_msg(username + ' is trying to kill me!')

   # Send messages to user but only if they say something in
   # the channel, not because they've joined, quit, etc
   if username in messages and 'ACTION' not in data \
           and 'QUIT' not in data and 'JOIN' not in data \
           and 'KICK' not in data:
       msg_count = len(messages[username])
       irc_msg(username + ' has ' + str(msg_count) + ' message(s)! ')
       for m in range(msg_count):
           irc_msg(messages[username][m])
       del messages[username]

   if ':!privmsg' in data:
       recip, msg = data.split(':!privmsg ')[1].strip("\r\n ").split(' ', 1)
       date, time = str(datetime.now())[:16].split()  # Ghetto, but works
       msg += " (from " + username + " at " + time + " on " + date + ")"
       try:
           priv_messages[recip].append(msg)
       except KeyError:
           priv_messages[recip] = []
           priv_messages[recip].append(msg)
       except:
           irc_msg(username + 'fucked up my code. Bastard.')

   if username in priv_messages:
       msg_count = len(priv_messages[username])
       irc.send('PRIVMSG ' + username + ' : You have ' +
                str(msg_count) + ' private message(s):' + end)
       for m in range(msg_count):
           irc.send('PRIVMSG ' + username + ' : ' + priv_messages[username][m] + end)
       del priv_messages[username]

   if '_bot' not in username.lower():
       for word in profanity:
           if word.lower() in data.lower() and \
                   'motherfucker' not in data.lower():
               irc_msg('Hey ' + username + ': watch your mouth, motherfucker')
       for word in shitlist:
           if word.lower() in data.lower():
               irc_msg('Notice: ' + username +
                       ' is a dipshit for mentioning ' + word)
       for word in goodlist:
           if word.lower() in data.lower():
               irc_msg('Notice: ' + username +
                       ' is redeemed for mentioning ' + word)

   if ':!wiki ' in data:
       page = data.split(':!wiki ')[1]
       url = "http://sbhackerspace.com/wiki/index.php?title="
       irc_msg(url + page)

   if ':!help' in data:
       irc_msg("Slut.")
       irc_msg("Options: !time <city>, !msg <recipient>, !privmsg <recipient>")
       #irc_msg("More: !")

   # if username == 'paul_be' or username == 'm0tan':
   #     irc_msg('Hey ' + username + ', am I annoying yet?')

   # if username == 'elimisteve':
   #     irc_msg('STFU ' + username + '!')

   if ':!members' in data:
       member_list = []
       #url = data.split(':!members')[1]
       html = urllib2.urlopen('http://sbhackerspace.com/wiki/index.php?title=Members&action=edit').read()
       text_area = re.findall(r'<textarea.*>(.*)</textarea>', html, re.DOTALL)[0]
       for line in text_area.split('\n'):
           member_list.append(line.split(',')[0].split()[-1].replace(']', ''))
       irc_msg('Current Members (from wiki): ' + ', '.join(member_list))

