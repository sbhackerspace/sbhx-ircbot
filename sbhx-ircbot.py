import socket, urllib2, re, os
import urllib, httplib
import time
from datetime import datetime

USER = 'sbhx'
auto_connect = True

bot_default     = USER + "_bot"
network_default = 'irc.freenode.net'
chan_default    = '#prototypemagic'

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

bad_on = False
badlist = """
Microsoft Windows iOS Apple Camarillo Ventura Russia China
Bieber Beiber Gentoo
""".split()

profanity_on = False
profanity = """
fuck shit bitch asshole cunt tits twat fag dick
""".split()

#scripting project projects PCBs
good_on = False
goodlist = """
Android Python Django Ruby Rails Clojure Bash Linux Emacs
Dropbox Wikileaks infosec DEFCON BSD hacking BackTrack
Slackware
""".split()

start_time = str(datetime.now())[:16]

irc = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
port = 6667
premess = 'PRIVMSG ' + chatchannel + ' :'

def new_connection(irc_obj):
    irc_obj.connect( ( network, port ) )
    print irc_obj.recv( 4096 )
    irc_obj.send( 'NICK ' + botname + end )
    irc_obj.send( 'USER ' + USER + 'bot botty bot bot: Python IRC' + end )
    irc_obj.send( 'JOIN ' + chatchannel + end )
    return irc_obj

# Used to store messages users leave for one another
left_messages = {}
left_priv_messages = {}

# Dictionaries of the form d == {'username1': 4, 'username2': 17}
utter_counts = {}
bot_response_counts = {}

a2morse = {'a': '.-', 'g': '--.', 'm': '--', 's': '...', 'y': '-.--',
           '4': '....-', 'b': '-...', 'h': '....', 'n': '-.',
           't': '-', 'z': '--..', '5': '.....', 'c': '-.-.',
           'i': '..', 'o': '---', 'u': '..-', '0': '-----',
           '6': '-....', 'd': '-..', 'j': '.---', 'p': '.--.',
           'v': '...-', '1': '.----', '7': '--...', 'e': '.',
           'k': '-.-', 'q': '--.-', 'w': '.--', '2': '..---',
           '8': '---..', 'f': '..-.', 'l': '.-..', 'r': '.-.',
           'x': '-..-', '3': '...--', '9': '----.'}

morse2a = {}

# DO NOT CONFUSE THIS WITH irc.msg
def irc_msg(msg):
    """Sends msg to channel"""
    irc.send(premess + msg + end)
    return

def priv_msg(user, msg):
    """Sends private msg to username"""
    irc.send('PRIVMSG ' + user + ' :' + msg.strip('\r\n ') + end)

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
    print "city = " + city
    if not city:
        city = local
    city = ' '.join([word.capitalize() for word in city.split()]) #cap words
    print "city = " + city
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
        if hours == 24:
            hours = 12;
        minutes = time.split()[1].split(':')[1]
        time = ' '.join([time.split()[0], str(hours) + ':' + str(minutes)])
    else: # if 'AM'
        hours = int(time.split()[1].split(':')[0])
        if hours == 12:
            hours = 0;
        minutes = time.split()[1].split(':')[1]
        time = ' '.join([time.split()[0], str(hours) + ':' + str(minutes)])
        #time = ' '.join(time.split()[:2])
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
    link = get_content('project add')
    link = username + str(link)
    dbfile = open(loadfile, 'w')
    dbfile.write(link + str(dbold))
    dbfile.close()

def inc_bot_response_counts():
   try:  ### Slide right one space
       bot_response_counts[username] += 1
       print "Bot responses to", username, " ==", bot_response_counts[username]
   except:
       try:
           bot_response_counts[username] = 1
       except:
           print "inc_bot_response_counts is REALLY broken"

def inc_utter_counts():
   try:
       utter_counts[username] += 1
       print "Utter count of", username, " ==", bot_response_counts[username]
   except:
       try:
           utter_counts[username] = 1
       except:
           print "inc_utter_counts is REALLY broken"

def get_content(keyword):
    return data.split(':!' + keyword + ' ')[1].strip('\r\n ')

def remove_tags(html):
    tags = re.findall(r"(<.*?>)", html, re.DOTALL)
    for tag in tags:
        print tag
        html = html.replace(tag, '')#.replace('<', '').replace('>', '')
    return html


while True:
   try:
       data = irc.recv ( 4096 )
   except:
       time.sleep(15)
       irc = new_connection(irc)
       continue

   datasp = data.split(' :')[0]
   datasp = str(datasp)

   username = getuser()
#   inc_utter_counts()

   if 'PING' in data:
      irc.send( 'PONG ' + data.split()[1] + end )

   if ':!quit' in data.lower() or ':!stats' in data.lower() or \
           ':!kick' in data.lower():
        message = username + " has been terminated."
        irc.send( 'KICK ' + chan_default + ' ' + username + " :" + message + end )

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
       query = get_content('google').replace(' ','+')
       search = "http://www.google.com/search?q=" + query
       irc_msg(search)

   if ':!g ' in data:
       query = get_content('g').replace(' ','+')
       search = "http://www.google.com/search?q=" + query
       irc_msg(search)

   if ':!lucky ' in data:
       try:
           query = get_content('lucky').replace(' ','+')
       except:
           irc_msg("!lucky <search_term>")
       search = "http://www.google.com/search" + \
           "?btnI=I'm+Feeling+Lucky&q=" + query
       irc_msg(search)

   if ':!wikilink ' in data:
       url = get_content('wikilink')
       html = urllib2.urlopen(
           'http://sbhackerspace.com/wiki/index.php' +
           '?title=Links&action=edit').read()
       textarea = re.findall(r'<textarea.*>(.*)</textarea>',
                             html, re.DOTALL)[0]
       appended_data = end + '* ' + url
       new_textarea = textarea + appended_data
       print new_textarea
   print data

   # Save messages to a dictionary of the form
   # dict['recipient'] = ['message 1', 'message 2', 'message 3']
   if ':!msg ' in data:
       try:
           # recips can be a single nick or a comma-delimited list of nicks
           recips, msg = get_content('msg').split(' ', 1)
       except:
           #irc_msg("Notice: " + username + " can't get anything right.")
           irc_msg("Options: !time <city>, !msg <recipient> <message>, " +
                   "!privmsg <recipient> <message>")
       date, time = str(datetime.now())[:16].split()
       try:
           msg += " (from " + username + " at " + time + " on " + date + ")"
       except:
           msg = username + ' tried to crash the bot. Bastard.'
       fails = []
       for recip in recips.split(','):
           try:
               left_messages[recip].append(msg)
           except KeyError:
               left_messages[recip] = []
               left_messages[recip].append(msg)
           except:
               fails.append(recip)
               #irc_msg(username + ' is trying to kill me!')
       if len(fails) > 0:
           if len(fails) == len(recips):
               irc_msg("User error.  Replace current user and reboot.")
           else:
               irc_msg("Okay, %s.  Skipped %s." % (username, ', '.join(fails)))
       else:
           irc_msg("Okay, %s." % username)
       del fails

   if ':!privmsg ' in data:
       try:
           recip, msg = get_content('privmsg').split(' ', 1)
       except:
           irc_msg("Options: !time <city>, !msg <recipient> <message>, " +
                   "!privmsg <recipient> <message>")
           msg = ""
       date, time = str(datetime.now())[:16].split()  # Ghetto, but works
       msg += " (from " + username + " at " + time + " on " + date + ")"
       # print "recip ==", recip
       # print
       # print "msg ==", msg
       # print
       try:
           left_priv_messages[recip].append(msg)
       except KeyError:
           left_priv_messages[recip] = []
           left_priv_messages[recip].append(msg)
       except:
           irc_msg(username + 'fucked up my code. Bastard.')
       else:
           irc_msg('Okay, %s.' % username)

   # Send messages to user but only if they say something in
   # the channel, not because they've joined, quit, etc
   if username in left_messages and 'ACTION' not in data \
           and 'QUIT' not in data and 'JOIN' not in data \
           and 'KICK' not in data:
       msg_count = len(left_messages[username])
       irc_msg(username + ' has ' + str(msg_count) + ' message(s)! ')
       for m in range(msg_count):
           irc_msg(left_messages[username][m])
       del left_messages[username]

   if username in left_priv_messages:
       msg_count = len(left_priv_messages[username])
       irc.send('PRIVMSG ' + username + ' :You have ' +
                str(msg_count) + ' private message(s):' + end)
       for m in range(msg_count):
           irc.send('PRIVMSG ' + username + ' : ' +
                    left_priv_messages[username][m] + end)
       del left_priv_messages[username]

   if not username.lower().endswith('bot'):
       if profanity_on:
           for word in profanity:
               if word.lower() in data.lower() and \
                       'motherfucker' not in data.lower():
                   irc_msg('Hey ' + username +
                           ': watch your mouth, motherfucker')
                   inc_bot_response_counts()
                   break
       if bad_on:
           for word in badlist:
               if word.lower() in data.lower() and \
                       'radioshack' not in data.lower() and \
                       'fios' not in data.lower():
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
       page = get_content('wiki')
       url = "http://sbhackerspace.com/wiki/index.php?title="
       irc_msg(url + page)
       inc_bot_response_counts()

   if ':!help' in data:
       irc_msg("Options: !time <city>, !msg <recipient> <message>, " +
               "!privmsg <recipient> <message>")
       inc_bot_response_counts()

   # if username == 'paul_be' or username == 'm0tan':
   #     irc_msg('Hey ' + username + ', am I annoying yet?')

   # if username == 'elimisteve':
   #     irc_msg('STFU ' + username + '!')

   if ':!members' in data:
       member_list = []
       #url = data.split(':!members')[1]
       html = urllib2.urlopen(
           'http://sbhackerspace.com/wiki/index.php' +
           '?title=Members&action=edit').read()
       textarea = re.findall(r'<textarea.*>(.*)</textarea>',
                             html, re.DOTALL)[0]
       for line in textarea.split('\n'):
           member_list.append(line.split(',')[0].split()[-1].replace(']', ''))
       irc_msg('Current Members (from wiki): ' + ', '.join(member_list))
       inc_bot_response_counts()

   # if ':!stats' in data:
       # priv_msg(username, "Since " + start_time)
       # priv_msg(username, "----------------------")
       # priv_msg(username, "Total Speakers: %d" % len(utter_counts))
       # total_utter = sum([utter_counts[nick] for nick in utter_counts])
       # priv_msg(username, "Total Utterances: %d" % total_utter)
       # total_bot_utter = sum([bot_response_counts[nick]
       #                        for nick in bot_response_counts])
       # priv_msg(username, "Total Bot Responses: %d" % total_bot_utter)
       # nick_width = max([len(nick) for nick in utter_counts])
       # priv_msg(username, "") # Blank line
       # priv_msg(username, "Nick%sMsg Count" % (' ' * nick_width))
       # priv_msg(username, "%s" % ('-' * (nick_width+13)))
       # for nick in utter_counts:
       #     priv_msg(username, nick + ' ' + str(utter_counts[nick]))
       # inc_bot_response_counts()

   if ":!userlist" in data:
       irc_msg("/userlist")

   if ':!ircbot ' in data:# and data.split(':!ircbot')[1] == '':
       url = get_content('ircbot')
       html = urllib2.urlopen('http://stevendphillips.com/ircbot/@edit/index').read()
       textarea = re.findall(
           r'<textarea.*>(.*)</textarea>', html, re.DOTALL)[0].strip('\r\n ')
       print textarea
       print '\n\n\n\n'
       appended_data = '\n' + '* ' + url
       new_textarea = textarea + appended_data
       # HTTP POST
       params = urllib.urlencode({'text': new_textarea})
       headers = {"content-type": "text/html"}
       conn = httplib.HTTPConnection('stevendphillips.com' + ":80")
       conn.request("POST", "/ircbot/", params, headers)
       response = conn.getresponse()
       print response.status, response.reason
       data = response.read()
       print data
       conn.close()
       # Show user what the wiki page now looks like
       for line in [line.strip() for line in new_textarea.split('\n')]:
           priv_msg(username, line)
       priv_msg(username, "") # Blank line
       priv_msg(username, 'New Feature List: http://stevendphillips.com/ircbot')

   if ':!ircbot' in data and ':!ircbot ' not in data:
       html = urllib2.urlopen('http://stevendphillips.com' +
                              '/ircbot/@edit/index').read()
       textarea = re.findall(
           r'<textarea.*>(.*)</textarea>', html, re.DOTALL)[0].strip('\r\n ')
       for line in [line.strip() for line in textarea.split('\n')]:
           priv_msg(username, line)

   if ':!echo ' in data:
       msg = get_content('echo')
       irc_msg(msg)

   if ':!badlist ' in data:
       cmd = get_content('badlist')
       if cmd.lower() == 'off': bad_on = False
       elif cmd.lower() == 'on': bad_on = True
       else: irc_msg("!badlist on|off")

   if ':!goodlist ' in data:
       cmd = get_content('goodlist')
       if cmd.lower() == 'off': good_on = False
       elif cmd.lower() == 'on': good_on = True
       else: irc_msg("!goodlist on|off")

   if ':!profanity ' in data:
       cmd = get_content('profanity')
       if cmd.lower() == 'off':
           profanity_on = False
           bad_on = False
       elif cmd.lower() == 'on':
           profanity_on = True
           bad_on = True
       else: irc_msg("!profanity on|off")

   if ':!shutup' in data or ':!lists off' in data:
       bad_on = False
       good_on = False
       profanity_on = False
       irc_msg("All lists disabled")

   if ':!fuckyou' in data or ':!lists on' in data:
       bad_on = True
       good_on = True
       profanity_on = True
       irc_msg("Careful, " + username + "...")

   if ':!define' in data and ':!define ' not in data:
       irc_msg("!define searchterm")

   if ':!define ' in data:
       query = get_content('define').replace(' ', '+')
       url = "http://www.google.com/search?q=define:"
       request = urllib2.Request(url + query)
       request.add_header('User-agent', 'Mozilla 3.10')
       html = urllib2.urlopen(request).read()
       try:
           definition = re.findall(r'<div class=s><div>(.*?)</div>',
                                   html, re.DOTALL)[0]
           if type(definition) is tuple:
               definition = definition[0]

           definition = definition.replace('&quot;', '"')
           definition = remove_tags(definition)
           if '&nbsp;' in definition:
               ndx = definition.index('&nbsp')
               definition = definition[:ndx]
           irc_msg(query.replace('+', ' ') + ': ' + str(definition))
       except:
           irc_msg("!define searchterm")
           continue

   if ':!urbandef' in data and ':!urbandef ' not in data:
       irc_msg("!urbandef searchterm")

   if ':!urbandef ' in data:
       query = get_content('urbandef').replace(' ', '+')
       url = "http://www.urbandictionary.com/define.php?term="
       request = urllib2.Request(url + query)
       request.add_header('User-agent', 'Mozilla 3.10')
       html = urllib2.urlopen(request).read()
       try:
           definition = re.findall(r'<div class="definition">(.*?)</div>',
                                   html, re.DOTALL)[0]
           if type(definition) is tuple:
               definition = definition[0]
           definition = definition.replace('&quot;', '"').replace('\r', ' ')
           definition = remove_tags(definition)
           irc_msg(query.replace('+', ' ') + ': ' + str(definition))
       except:
           irc_msg("!urbandef searchterm")

   if ':!whoami' in data.lower() or ':!saymyname' in data.lower():
       irc_msg(username)

   if ':!morse ' in data.lower():
       ndx = data.lower().index(':!morse')
       irc_msg(' '.join([a2morse[x] if x in a2morse else x for x in data.lower().replace(':!morse ', '')[ndx:]]))

   if ':!convert ' in data.lower():
       query = get_content('convert').replace(' ', '+')
       url = "http://www.google.com/search?q=convert+"
       request = urllib2.Request(url + query)
       request.add_header('User-agent', 'Mozilla 3.10')
       html = urllib2.urlopen(request).read()
       try:
           definition = re.findall(r'<h2 class=r .*?><b>(.*?)</b>',
                                   html, re.DOTALL)[0]
           if type(definition) is tuple:
               definition = definition[0]
           definition = definition.replace('&quot;', '"')
           definition = remove_tags(definition)
           irc_msg(definition)
       except:
           irc_msg("!convert [what you want converted]")
