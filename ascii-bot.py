#!/usr/bin/python
# -*- coding:utf-8 -*-
#Facepalm temporarily removed by Aaron Berk

import socket, urllib2, re, os
import urllib, httplib
from datetime import datetime
import time

COMMAND_LIST = """!batman !karuption !monkey !bunny !unccliff
!iggy !frylock !facpalm !spider !cupcake !marx !kirbyhug
""".split()

ADMINS = ['elimisteve', 'paul_be']

USER = 'mr_ascii'
auto_connect = True

bot_default     = USER + "_bot"
network_default = 'irc.freenode.net'
chan_default    = '#sbhx-ascii'

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

end = '\n'

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
left_priv_messages = {}

# Dictionaries of the form d == {'username1': 4, 'username2': 17}
utter_counts = {}
bot_response_counts = {}

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

#def timescrapes():
#    """Sends current time in given city to IRC channel"""
#    html = urllib2.urlopen('http://www.timeanddate.com/worldclock/').read()
#    local = 'Los Angeles'
#    city = data.split(':!time')[1].strip('\r\n ')
#    print "city = ", city
#    if not city:
#        city = local
#    city = ' '.join([word.capitalize() for word in city.split()]) #cap words
#    print "city = ", city
#    time = html.split(city)[1].split('>')[3].split('<')[0]
#    irc_msg(time)
#    return

#def timescrapes24():
#    """Sends current time in given city to IRC channel"""
#    html = urllib2.urlopen('http://www.timeanddate.com/worldclock/').read()
#    local = 'Los Angeles'
#    city = data.split(':!time24')[1].strip('\r\n ')
#    if not city:
#        city = local
#    city = ' '.join([word.capitalize() for word in city.split()]) #cap words
#    time = html.split(city)[1].split('>')[3].split('<')[0]
#    if time.split()[2] == 'PM':
#        hours = int(time.split()[1].split(':')[0]) + 12
#        minutes = time.split()[1].split(':')[1]
#        time = ' '.join([time.split()[0], str(hours) + ':' + str(minutes)])
#    else:
#        time = ' '.join(time.split()[:2])
#    irc_msg(time)
    #str(datetime.now())[:16].split()[1]
#    return


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
   try:
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

# elimisteve; 2011.03.30
def cmd_count(msg):
    return sum([x.count(y) for x in msg.split() for y in COMMAND_LIST])

# Will still respond to a few commands, but won't print ascii art
ascii_enabled = True
while True:
   data = irc.recv ( 4096 )
   datasp = data.split(' :')[0]
   datasp = str(datasp)

   username = getuser()
   inc_utter_counts()

   if cmd_count(data) > 2:
       message = username + " has been terminated."
       irc.send( 'KICK ' + chan_default + ' ' + username + " :" + message + end )
       continue

   if 'PING' in data:
      irc.send( 'PONG ' + data.split()[1] + end )

   if ':!quit' in data.lower():
       irc_msg("I am immortal.")

   if ':!help' in data.lower():
       irc_msg("Options: " + ' '.join(COMMAND_LIST) + "  # More to come!")
       inc_bot_response_counts()

   if ':!echo ' in data:
       msg = get_content('echo')
       irc_msg(msg)

   if 'KICK' in data:
      irc.send( 'JOIN ' + chatchannel + end )

   if ':!ascii_off' in data.lower() and username in ADMINS:
       ascii_enabled = False
       irc_msg(botname + " disabled")

   if ':!ascii_on' in data.lower() and username in ADMINS:
       ascii_enabled = True
       irc_msg(botname + " enabled")

   if ascii_enabled:
       if ':!batman' in data.lower():
           irc_msg("       _==/          i     i          \==_")
           irc_msg("     /XX/            |\___/|            \XX\ ")
           irc_msg("   /XXXX\            |XXXXX|            /XXXX\ ")
           irc_msg("  |XXXXXX\_         _XXXXXXX_         _/XXXXXX|")
           irc_msg(" XXXXXXXXXXXxxxxxxxXXXXXXXXXXXxxxxxxxXXXXXXXXXXX")
           irc_msg("|XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX|")
           irc_msg("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
           irc_msg("|XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX|")
           irc_msg(" XXXXXX/^^^^^\XXXXXXXXXXXXXXXXXXXXX/^^^^^\XXXXXX")
           irc_msg("  |XXX|       \XXX/^^\XXXXX/^^\XXX/       |XXX|")
           irc_msg("    \XX\       \X/    \XXX/    \X/        /XX/")
           irc_msg("       *\       V      \X/      V        /* ")
           irc_msg("                        V                  ")
           irc_msg("    \XX\       \X/    \XXX/    \X/       /XX/")
           irc_msg("       *\       V      \X/      V       /*")

       if ':!karuption' in data.lower():
           irc_msg("      ___")
           irc_msg("     //  7")
           irc_msg("    (_,_/\ ")
           irc_msg("     \    \ ")
           irc_msg("      \    \ ")
           irc_msg("      _\    \__")
           irc_msg("     (   \     )")
           irc_msg("      \___\___/")

       if ':!monkey' in data.lower():
           irc_msg("@('_')@")

       if ':!bunny' in data.lower():
           irc_msg('()()')
           irc_msg('(*-*)')
           irc_msg('c(")(")')

       if ':!unccliff' in data.lower():
           irc_msg("                          UNCLE CLIFF ")
           irc_msg("                   ____________ ")
           irc_msg("               ______|            |__")
           time.sleep(1)
           irc_msg("              |             ###      |")
           irc_msg("              |          ###         |____________")
           time.sleep(5)
           irc_msg("              |       #########                   |")
           irc_msg("              |      #         #            ##### |     __")
           irc_msg("           ___|      #         #                  |____|  |_")
           irc_msg("          |          #         #           #######          |")
           time.sleep(5)
           irc_msg("          |          #    #    #          #       #         |")
           irc_msg("    ##    |          #         #          #   #   #         |       ##")
           irc_msg("    ##    |          #         #          #       #         |       ##")
           time.sleep(5)
           irc_msg("    ##    |           #########            #######          |__     ##")
           irc_msg("    ##    |                                                    |    ##")
           irc_msg("    ####  |           ################################         |  ####")
           irc_msg("      ####|       ########################################     |####")
           time.sleep(5)
           irc_msg("        ##|       ###                                          |##")
           irc_msg("          |____________________________________________________|")
           irc_msg("                       ###")
           time.sleep(5)
           irc_msg("                       ###")
           irc_msg("                       ###")
           time.sleep(5)
           irc_msg("            ##############")
           irc_msg("            ##############")
           irc_msg("                  THE END ")

       if ':!iggy' in data.lower():

           irc_msg("                       IGNIGNOKT")
           irc_msg("                     ______                  __________           ##")
           irc_msg("                    |      |                |          |          ##")
           time.sleep(5)
           irc_msg("                    |      |__              |          |          ##")
           irc_msg("                    |         |             |          |          ##")
           irc_msg("                ____|         |             |          |          ##")
           irc_msg("               |              |    _________|          |          ##")
           time.sleep(5)
           irc_msg("               |              |___|                    |          ##")
           irc_msg("               |                                       |          ##")
           irc_msg("               |            ###          ###           |      ##########")
           time.sleep(5)
           irc_msg("               |_        ######          ######        |      ##########")
           irc_msg("                 |    ######                ######     |         ####")
           irc_msg("                 | ######                      ######  |         ####")
           time.sleep(5)
           irc_msg("                 | ###      #####      #####      ###  |         ####")
           irc_msg("                 |                                     |         ####")
           irc_msg("                 |                                     |___      ####")
           time.sleep(5)
           irc_msg("                 |                                         |#########")
           irc_msg("             ____|                                         |#########")
           irc_msg("         ###|              ##################              |")
           irc_msg("      ######|              ##################              |")
           time.sleep(5)
           irc_msg("    ######  |                                              |")
           irc_msg("    ####    |                                              |")
           irc_msg("    ####    |                                              |")
           irc_msg("    ####    |                                              |")
           time.sleep(5)
           irc_msg("            |                                              |")
           irc_msg("            |                                              |")
           irc_msg("            |______________________________________________|")
           irc_msg("                         #####           #####")
           irc_msg("                         #####           #####")
           time.sleep(5)
           irc_msg("                 #############           #############")
           irc_msg("                 #############           #############")
           irc_msg("                                   THE END")

       if ':!frylock' in data.lower():
           irc_msg("              FRYLOCK")
           irc_msg("               __             __")
           irc_msg("        __    /__/| __   __  |\__\ ")
           irc_msg("       /__/|  |  ||/__/|/__/|||  |___")
           irc_msg("       |  ||__| /__/  |||  ||||  |__/|")
           time.sleep(5)
           irc_msg("       | _|/__/||  |  |||  ||||  |  ||")
           irc_msg("       | \__\ |||  | |__|  |||| /__/||")
           irc_msg("       | |  | |||  | |  |  |/__/|  |||")
           irc_msg("     _-| |  | |||  | |  |  ||  ||  |||-_")
           irc_msg("    \_ | |  | |||  | |  |  ||  ||  ||| _/")
           irc_msg("    | -_ |  | |||  | |  |  ||  ||  ||_- |")
           time.sleep(5)
           irc_msg("    \   '-_ | |||  | |  |  ||  || _-'   /")
           irc_msg("    |      '------,,,,,,,,,------'      |")
           irc_msg("     \                                 /")
           irc_msg("     |     _.._       |       _.._     |")
           irc_msg("      \    /___;;;-_| | |_-;;;___\    /")
           irc_msg("      |    \___*__/      \\__*___/    |")
           irc_msg("      |                  \            |")
           time.sleep(5)
           irc_msg("       \                 \\__        /")
           irc_msg("       |                             |")
           irc_msg("       |                             |")
           irc_msg("        \       -.         .-       /")
           irc_msg("        |       .//.     .\\.       |")
           time.sleep(5)
           irc_msg("        |     .//////._.\\\\\\.     |")
           irc_msg("         \   /////////|\\\\\\\\\   /")
           irc_msg("          |_///-'   -___-   '-\\\_| ")
           irc_msg("            \\_      /|\      _//")
           time.sleep(5)
           irc_msg("             '\\\\\\//|\\//////' ")
           irc_msg("               '\\\\\\|//////' ")
           irc_msg("                  '\\\|///' ")
           irc_msg("                      THE END")


       # From paul_be
       if ':!spider' in data.lower():
           irc_msg("/X\(-_-)/X\ ")

       # Also from paul_be
       if ':!cupcake' in data.lower():
           irc_msg("           )")
           irc_msg("          (.)")
           irc_msg("          .|.")
           irc_msg("          l7J")
           irc_msg("          | |")
           irc_msg("      _.--| |--._")
           irc_msg("   .-';  ;`-'& ; `&.")
           irc_msg("  & &  ;  &   ; ;   \ ")
           irc_msg("  \      ;    &   &_/")
           irc_msg("   F\"\"\"---...---\"\"\"J")
           irc_msg("   | | | | | | | | |")
           irc_msg("   J | | | | | | | F")
           irc_msg("    `---.|.|.|.---\'")

       # from avb_wkyhu
       if ':!kirbyhug' in data.lower():
            irc_msg("(>^_^)>")

       # from avb_wkyhu
       if ':!marx' in data.lower():
           irc_msg('                          ___.....        ')
           irc_msg("                       .-'        `.    ")
           irc_msg("                      ' `.---------... ")
           irc_msg("                     (:'            `.\ ")
           irc_msg("                    '  (               .    ")
           time.sleep(2)
           irc_msg("                    (' `.           ':  :    ")
           irc_msg("                   ( (.'- .==._   _= :  `.    ")
           irc_msg("                   `_(   ' _o' `.'_o`-\_:'    ")
           irc_msg("                     :`         .     ::    ")
           irc_msg("                     :: \   .'_,J \  ':.    ")
           time.sleep(3)
           irc_msg("                     =-`._.'_.::::.`_:'=.    ")
           irc_msg("                    .-:-.=:-::.__:.=:-:=-    ")
           irc_msg("                     -:/-:.'=:/::.\.-=:=    ")
           irc_msg("                      '././:/.::|,\`:\=.a._    ")
           irc_msg("                      ba''/:|:|::|:\\``888888.    ")
           time.sleep(3)
           irc_msg("                  _.a(88/  _.='\.   .a388888888a.    ")
           irc_msg('             _.a8883a8/.:"    `:..a838888888888aa.    ')
           irc_msg("        _.a888888388/''        ')'83888888888888888)    ")
           irc_msg("      .888888888388/           (:838888888888888888)    ")
           irc_msg('     .888888888388P           /8"8888888888888888a88)    ')
           time.sleep(4)
           irc_msg("     888888888838P           /8888888888P8888888P88'    ")
           irc_msg("     888888888838           /88388888888a88888888P'    ")
           irc_msg('     888888888838:         /88388888888P888888P"    ')
           irc_msg('      88a88888838a        /88388888888a8888P"    ')
           irc_msg('       "P888888388a      /88388888888a888P" ')
           time.sleep(4)
           irc_msg('         "888883888a...aa88388888888a888P    ')
           irc_msg('           "88838888888888388888888a888P    ')
           irc_msg("            8883888888888388888888a888P    ")
           irc_msg('            "88388888888388888888a888P    ')
       else: # If disabled
           pass

   print data
