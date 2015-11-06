#!/usr/bin/python
# -*- coding:utf-8 -*-
#Facepalm temporarily removed by Aaron Berk

import socket, urllib2, re, os
import urllib, httplib
from datetime import datetime
import time
import random

COMMAND_LIST = """!batman !monkey !bunny !unccliff
!iggy !frylock !spider !cupcake !marx !kirbyhug
!handbanana !tardis !tux !r2d2 !barlek !bender !mbales
!cat !dog !random
""".split()

ADMINS = ['elimisteve', 'paul_be', 'mbales', 'gholms']

USER = 'mr_ascii'
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
		user = data.split()[0].split('!')[0].strip(':')
	except:
		user = data.split('!')[0].strip(':')
	return user


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

"""Add ascii art here to keep somewhat organized"""

def batman():
	irc_msg("       _==/          i     i          \==_")
	irc_msg("     /XX/            |\___/|            \XX\ ")
	irc_msg("   /XXXX\            |XXXXX|            /XXXX\ ")
	irc_msg("  |XXXXXX\_         _XXXXXXX_         _/XXXXXX|")
	irc_msg(" XXXXXXXXXXXxxxxxxxXXXXXXXXXXXxxxxxxxXXXXXXXXXXX")
	time.sleep(1)
	irc_msg("|XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX|")
	irc_msg("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
	irc_msg("|XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX|")
	irc_msg(" XXXXXX/^^^^^\XXXXXXXXXXXXXXXXXXXXX/^^^^^\XXXXXX")
	irc_msg("  |XXX|       \XXX/^^\XXXXX/^^\XXX/       |XXX|")
	time.sleep(1)
	irc_msg("    \XX\       \X/    \XXX/    \X/        /XX/")
	irc_msg("       *\       V      \X/      V        /* ")
	irc_msg("                        V                  ")
	
def karuption():
	irc_msg("      ___")
	irc_msg("     //  7")
	irc_msg("    (_,_/\ ")
	irc_msg("     \    \ ")
	irc_msg("      \    \ ")
	irc_msg("      _\    \__")
	irc_msg("     (   \     )")
	irc_msg("      \___\___/")
	
def unccliff():
	irc_msg("                          UNCLE CLIFF ")
	irc_msg("                      ____________ ")
	irc_msg("               ______|            |__")
	irc_msg("              |             ###      |")
	irc_msg("              |          ###         |____________")
	time.sleep(5)
	irc_msg("              |       #########                   |")
	irc_msg("              |      #         #            ##### |     __")
	irc_msg("           ___|      #         #                  |____|  |_")
	irc_msg("          |          #         #           #######          |")
	irc_msg("          |          #    #    #          #       #         |")
	time.sleep(5)
	irc_msg("    ##    |          #         #          #   #   #         |       ##")
	irc_msg("    ##    |          #         #          #       #         |       ##")
	irc_msg("    ##    |           #########            #######          |__     ##")
	irc_msg("    ##    |                                                    |    ##")
	irc_msg("    ####  |           ################################         |  ####")
	time.sleep(5)
	irc_msg("      ####|       ########################################     |####")
	irc_msg("        ##|       ###                                          |##")
	irc_msg("          |____________________________________________________|")
	irc_msg("                       ###")
	irc_msg("                       ###")
	time.sleep(5)
	irc_msg("                       ###")
	irc_msg("            ##############")
	irc_msg("            ##############")
	irc_msg("                  THE END ")

def monkey():
	irc_msg("@('_')@")

def bunny():
	irc_msg('()()')
	irc_msg('(*-*)')
	irc_msg('c(")(")')

def iggy():
	irc_msg("                       IGNIGNOKT")
	irc_msg("                     ______                  __________           ##")
	irc_msg("                    |      |                |          |          ##")
	irc_msg("                    |      |__              |          |          ##")
	irc_msg("                    |         |             |          |          ##")
	time.sleep(5)
	irc_msg("                ____|         |             |          |          ##")
	irc_msg("               |              |    _________|          |          ##")
	irc_msg("               |              |___|                    |          ##")
	irc_msg("               |                                       |          ##")
	irc_msg("               |            ###          ###           |      ##########")
	time.sleep(5)
	irc_msg("               |_        ######          ######        |      ##########")
	irc_msg("                 |    ######                ######     |         ####")
	irc_msg("                 | ######                      ######  |         ####")
	irc_msg("                 | ###      #####      #####      ###  |         ####")
	irc_msg("                 |                                     |         ####")
	time.sleep(5)
	irc_msg("                 |                                     |___      ####")
	irc_msg("                 |                                         |#########")
	irc_msg("             ____|                                         |#########")
	irc_msg("         ###|              ##################              |")
	irc_msg("      ######|              ##################              |")
	time.sleep(5)
	irc_msg("    ######  |                                              |")
	irc_msg("    ####    |                                              |")
	irc_msg("    ####    |                                              |")
	irc_msg("    ####    |                                              |")
	irc_msg("            |                                              |")
	time.sleep(5)
	irc_msg("            |                                              |")
	irc_msg("            |______________________________________________|")
	irc_msg("                         #####           #####")
	irc_msg("                         #####           #####")
	irc_msg("                 #############           #############")
	time.sleep(5)
	irc_msg("                 #############           #############")
	irc_msg("                                   THE END")
	
def frylock():
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
	time.sleep(5)
	irc_msg("    | -_ |  | |||  | |  |  ||  ||  ||_- |")
	irc_msg("    \   '-_ | |||  | |  |  ||  || _-'   /")
	irc_msg("    |      '------,,,,,,,,,------'      |")
	irc_msg("     \                                 /")
	irc_msg("     |     _.._       |       _.._     |")
	irc_msg("      \    /___;;;-_| | |_-;;;___\    /")
	time.sleep(5)
	irc_msg("      |    \___*__/      \\__*___/    |")
	irc_msg("      |                  \            |")
	irc_msg("       \                 \\__        /")
	irc_msg("       |                             |")
	irc_msg("       |                             |")
	time.sleep(5)
	irc_msg("        \       -.         .-       /")
	irc_msg("        |       .//.     .\\.       |")
	irc_msg("        |     .//////._.\\\\\\.     |")
	irc_msg("         \   /////////|\\\\\\\\\   /")
	irc_msg("          |_///-'   -___-   '-\\\_| ")
	time.sleep(5)
	irc_msg("            \\_      /|\      _//")
	irc_msg("             '\\\\\\//|\\//////' ")
	irc_msg("               '\\\\\\|//////' ")
	irc_msg("                  '\\\|///' ")
	irc_msg("                      THE END")

def cupcake():
	irc_msg("           )")
	irc_msg("          (.)")
	irc_msg("          .|.")
	irc_msg("          l7J")
	irc_msg("          | |")
	time.sleep(5)
	irc_msg("      _.--| |--._")
	irc_msg("   .-';  ;`-'& ; `&.")
	irc_msg("  & &  ;  &   ; ;   \ ")
	irc_msg("  \      ;    &   &_/")
	irc_msg("   F\"\"\"---...---\"\"\"J")
	time.sleep(5)
	irc_msg("   | | | | | | | | |")
	irc_msg("   J | | | | | | | F")
	irc_msg("    `---.|.|.|.---\'")
	
def spider():
	irc_msg("/X\(-_-)/X\ ")
	
def kirbyhug():
	irc_msg("(>^_^)>")
	
def marx():
	irc_msg('                          ___.....        ')
	irc_msg("                       .-'        `.    ")
	irc_msg("                      ' `.---------... ")
	irc_msg("                     (:'            `.\ ")
	irc_msg("                    '  (               .    ")
	time.sleep(5)
	irc_msg("                    (' `.           ':  :    ")
	irc_msg("                   ( (.'- .==._   _= :  `.    ")
	irc_msg("                   `_(   ' _o' `.'_o`-\_:'    ")
	irc_msg("                     :`         .     ::    ")
	irc_msg("                     :: \   .'_,J \  ':.    ")
	time.sleep(5)
	irc_msg("                     =-`._.'_.::::.`_:'=.    ")
	irc_msg("                    .-:-.=:-::.__:.=:-:=-    ")
	irc_msg("                     -:/-:.'=:/::.\.-=:=    ")
	irc_msg("                      '././:/.::|,\`:\=.a._    ")
	irc_msg("                      ba''/:|:|::|:\\``888888.    ")
	time.sleep(5)
	irc_msg("                  _.a(88/  _.='\.   .a388888888a.    ")
	irc_msg('             _.a8883a8/.:"    `:..a838888888888aa.    ')
	irc_msg("        _.a888888388/''        ')'83888888888888888)    ")
	irc_msg("      .888888888388/           (:838888888888888888)    ")
	irc_msg('     .888888888388P           /8"8888888888888888a88)    ')
	time.sleep(5)
	irc_msg("     888888888838P           /8888888888P8888888P88'    ")
	irc_msg("     888888888838           /88388888888a88888888P'    ")
	irc_msg('     888888888838:         /88388888888P888888P"    ')
	irc_msg('      88a88888838a        /88388888888a8888P"    ')
	irc_msg('       "P888888388a      /88388888888a888P" ')
	time.sleep(5)
	irc_msg('         "888883888a...aa88388888888a888P    ')
	irc_msg('           "88838888888888388888888a888P    ')
	irc_msg("            8883888888888388888888a888P    ")
	irc_msg('            "88388888888388888888a888P    ')

def tardis():
	irc_msg('          _ ')
	irc_msg('         /-\ ')
	irc_msg('    _____|#|_____')
	irc_msg('   |_____________|')
	irc_msg('  |_______________|')
	irc_msg('|||_POLICE_##_BOX_|||')
	time.sleep(5)
	irc_msg(' | |¯|¯|¯|||¯|¯|¯| |')
	irc_msg(' | |-|-|-|||-|-|-| |')
	irc_msg(' | |_|_|_|||_|_|_| |')
	irc_msg(' | ||~~~| | |¯¯¯|| |')
	irc_msg(' | ||~~~|!|!| O || |')
	time.sleep(5)
	irc_msg(' | ||~~~| |.|___|| |')
	irc_msg(' | ||¯¯¯| | |¯¯¯|| |')
	irc_msg(' | ||   | | |   || |')
	irc_msg(' | ||___| | |___|| |')
	irc_msg(' | ||¯¯¯| | |¯¯¯|| |')
	time.sleep(5)
	irc_msg(' | ||   | | |   || |')
	irc_msg(' | ||___| | |___|| |')
	irc_msg('|¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯|')
	irc_msg(' ¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯')
	
def tux():
	irc_msg("                  .88888888:. ")
	irc_msg("                88888888.88888.") 
	irc_msg("              .8888888888888888. ")
	irc_msg("              888888888888888888 ")
	irc_msg("              88' _`88'_  `88888 ")
	time.sleep(5)
	irc_msg("              88 88 88 88  88888 ")
	irc_msg("              88_88_::_88_:88888 ")
	irc_msg("              88:::,::,:::::8888 ")
	irc_msg("              88`:::::::::'`8888 ")
	irc_msg("             .88  `::::'    8:88. ")
	time.sleep(5)
	irc_msg("            8888            `8:888. ")
	irc_msg("          .8888'             `888888. ")
	irc_msg("         .8888:..  .::.  ...:'8888888:. ")
	irc_msg("        .8888.'     :'     `'::`88:88888 ")
	irc_msg("       .8888        '         `.888:8888. ")
	time.sleep(5)
	irc_msg("      888:8         .           888:88888 ")
	irc_msg("    .888:88        .:           888:88888: ")
	irc_msg("    8888888.       ::           88:888888 ")
	irc_msg("    `.::.888.      ::          .88888888 ")
	irc_msg("   .::::::.888.    ::         :::`8888'.:. ")
	time.sleep(5)
	irc_msg("  ::::::::::.888   '         .:::::::::::: ")
	irc_msg("  ::::::::::::.8    '      .:8::::::::::::. ")
	irc_msg(" .::::::::::::::.        .:888::::::::::::: ")
	irc_msg(" :::::::::::::::88:.__..:88888:::::::::::' ")
	irc_msg("  `'.:::::::::::88888888888.88:::::::::' ")
	irc_msg("        `':::_:' -- '' -'-' `':_::::'` ")
	
def r2d2():
	irc_msg("       .'/L|__`.")
	irc_msg("      / =[_]O|` \ ")
	irc_msg("      |'+_____':|")
	irc_msg("    __:='|____`-:__")
	irc_msg("   ||[] ||====| []||")
	time.sleep(5)
	irc_msg("   ||[] | |=| | []||")
	irc_msg("   |:||_|=|U| |_||:|")
	irc_msg("   |:|||]_=_ =[_||:|")
	irc_msg("   | |||] [_][]C|| |")
	irc_msg("   | ||-''''''`-|| |")
	time.sleep(5)
	irc_msg("   /|\\_\_|_|_/_//|\ ")
	irc_msg("  |___|   /|\   |___|")
	irc_msg("  `---'  |___|  `---' ")
	irc_msg("         `---' ")

def barklek():
	irc_msg("     ____________ ")
	irc_msg("    /____________\ ")
	irc_msg("   / /  _\__/_  \ \ ")
	irc_msg("   | | // \\// \\ | |")
	irc_msg("   | | \\_//\\_//.| |")
	time.sleep(5)
	irc_msg("   |_\__/_<>_\__/_|")
	irc_msg("     /        \ ")
	irc_msg("    /  ||  ||  \ ")
	irc_msg("  ///            \\\ ")
	irc_msg(" //|              |\\ ")
	time.sleep(5)
	irc_msg(" / \\   Tonight   // \ ")
	irc_msg("|U'U|'---____---'|U'U|")
	irc_msg("|____________________|")
	irc_msg("     \          / ")
	irc_msg("      |        |")
	time.sleep(5)
	irc_msg("      |        | ")
	irc_msg("  ____|        |____")
	irc_msg(" |\__/|        |\__/|")
	irc_msg(" |    /        \    |")
	irc_msg(" |  /    You!    \  |")
	irc_msg(" |/________________\|")
	irc_msg(" |__________________|")
	
def bender():
	irc_msg("     ( ) ")
	irc_msg("      H")
	irc_msg("      H")
	irc_msg("     _H_ ")
	irc_msg("  .-'-.-'-.")
	time.sleep(5)
	irc_msg(" /         \ ")
	irc_msg("|           |")
	irc_msg("|   .-------'._ ")
	irc_msg("|  / /  '.' '. \ ")
	time.sleep(5)
	irc_msg("|  \ \ @   @ / / ")
	irc_msg("|   '---------'    ")    
	irc_msg("|    _______|  ")
	irc_msg("|  .'-+-+-+|  ")
	irc_msg("|  '.-+-+-+| ")
	irc_msg("|   '''''' |")
	irc_msg("'-.__   __.-'")
	irc_msg("     ''' ")

def mbales():
	irc_msg("                $$$$ ")
	irc_msg("              $$____$$ ")
	irc_msg("              $$____$$ ")
	irc_msg("              $$____$$ ")
	irc_msg("              $$____$$ ")
	time.sleep(5)
	irc_msg("              $$____$$ ")
	irc_msg("          $$$$$$____$$$$$$ ")
	irc_msg("        $$____$$____$$____$$$$ ")
	irc_msg("        $$____$$____$$____$$__$$ ")
	irc_msg("$$$$$$  $$____$$____$$____$$____$$ ")
	time.sleep(5)
	irc_msg("$$    $$$$________________$$____$$ ")
	irc_msg("$$      $$______________________$$ ")
	irc_msg("  $$    $$______________________$$ ")
	irc_msg("   $$$__$$______________________$$ ")
	irc_msg("    $$__________________________$$ ")
	time.sleep(5)
	irc_msg("    $$$________________________$$ ")
	irc_msg("      $$______________________$$$ ")
	irc_msg("       $$$____________________$$ ")
	irc_msg("        $$____________________$$ ")
	irc_msg("         $$$________________$$$ ")
	irc_msg("          $$________________$$ ")
	irc_msg("          $$$$$$$$$$$$$$$$$$$$ ")
	
def cat():
	irc_msg(" /\_/\ ")
	irc_msg("( o o ) ")
	irc_msg("==_Y_== ")
	irc_msg("  `-' ")

def dog():
	irc_msg("             .--~~,__ ")
	irc_msg(":-....,-------`~~'._.' ")
	irc_msg(" `-,,,  ,_      ;'~U' ")
	irc_msg("  _,-' ,'`-__; '--. ")
	irc_msg(" (_/'~~      '' '(; ")
	
"""Ascii art above please"""

# Print random ascii art.
# Im sure there is a better way to do this but hell it works...	
def ascii_random():
	for i in range(19):
		ranchoice = random.randint(1,19)
		print ranchoice
		if ranchoice == 1:
			batman()
			break
		if ranchoice == 2:
			karuption()
			break
		if ranchoice == 3:
			unccliff()
			break
		if ranchoice == 4:
			iggy()
			break
		if ranchoice == 5:
			bunny()
			break
		if ranchoice == 6:
			monkey()
			break
		if ranchoice == 7:
			frylock()
			break
		if ranchoice == 8:
			cupcake()
			break
		if ranchoice == 9:
			kirbyhug()
			break
		if ranchoice == 10:
			spider()
			break
		if ranchoice == 11:
			marx()
			break
		if ranchoice == 12:
			tardis()
			break
		if ranchoice == 13:
			tux()
			break
		if ranchoice == 14:
			r2d2()
			break
		if ranchoice == 15:
			barklek()
			break
		if ranchoice == 16:
			bender()
			break
		if ranchoice == 17:
			handbanana()
			break
		if ranchoice == 18:
			dog()
			break
		if ranchoice == 19:
			cat()
			break
	

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
			batman()
		
		if ':!karuption' in data.lower():
			karuption()

		if ':!monkey' in data.lower():
			monkey()

		if ':!bunny' in data.lower():
			bunny()

		if ':!unccliff' in data.lower():
			unccliff()

		if ':!iggy' in data.lower():
			iggy()
		
		if ':!frylock' in data.lower():
			frylock()

		# From paul_be
		if ':!spider' in data.lower():
			spider()

		# Also from paul_be
		if ':!cupcake' in data.lower():
			cupcake()

		# from avb_wkyhu
		if ':!kirbyhug' in data.lower():
			kirbyhug()

		# from avb_wkyhu
		if ':!marx' in data.lower():
			marx()
			
		if ':!handbanana' in data.lower():
			irc_msg("TONIGHT... YOU!!!")
		
		if ':!tardis' in data.lower():
			tardis()

		if ':!tux' in data.lower():
			tux()
			
		if ':!r2d2' in data.lower():
			r2d2()

		if ':!barlek' in data.lower():
			barlek()
			
		if ':!bender' in data.lower():
			bender()
			
		if ':!mbales' in data.lower():
			mbales()
		
		if ':!cat' in data.lower():
			cat()
			
		if ':!dog' in data.lower():
			dog()
			
		if ':!random' in data.lower():
			ascii_random()
			
		else: # If disabled
			pass
	
	print data
	
