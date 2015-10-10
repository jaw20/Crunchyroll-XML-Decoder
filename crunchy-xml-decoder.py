import sys
import argparse
import os
import subprocess
from getpass import getpass
sys.path.append('crunchy-xml-decoder')
import functtest
import ultimate
import login
import decode

import time

#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#(CHECKING)#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#
if not os.path.exists("export"):
    os.makedirs("export")

def defaultsettings():
    dsettings='''[SETTINGS]
# Set this to the preferred quality. Possible values are: "android" (hard-subbed), "360p", "480p", "720p", "1080p", or "highest" for highest available.
# Note that any quality higher than 360p still requires premium, unless it's available that way for free (some first episodes).
# We're not miracle workers.
video_quality = highest

# Set this to the desired subtitle language. If the subtitles aren't available in that language, it reverts to the second language option (below).
# Available languages: English, Espanol, Espanol_Espana, Francais, Portugues, Turkce, Italiano, Arabic, Deutsch
language = English

# If the first language isn't available, what language would you like as a backup? Only if then they aren't found, then it goes to English as default
language2 = English

# Set this if you want to use --forced-track rather than --default-track for subtitle
forcesubtitle = False

# Set this if you want to use a US session ID
forceusa = False

# Set this if you want to Localize the cookies (this option is under testing and may generate some problem and it willnot work with -forceusa- option)
localizecookies = false
'''
    open('.\\settings.ini', 'w').write(dsettings.encode('utf-8'))

if not os.path.exists(".\\settings.ini"):
    defaultsettings()
	
if not os.path.exists(".\\cookies"):
    if raw_input(u'Do you have an account [Y/N]?').lower() == 'y':
        username = raw_input(u'Username: ')
        password = getpass('Password(don\'t worry the password are typing but hidden:')
        login.login(username, password)
    else:
        login.login('', '')


#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#(Argument Parser)#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#
parser = argparse.ArgumentParser()
parser.add_argument("-u","--url", type=str,help="Crunchyroll Anime Link. if you get an error, try using double quotation marks (\")")
parser.add_argument("-sn","--season-number", metavar='#', type=int, nargs = 1, help="Crunchyroll Anime Season Number,it's optional option you can ignore")
parser.add_argument("-en","--episode-number", metavar='#', type=int, nargs = 1, help="Crunchyroll Anime Episode Number,it's optional option you can ignore")
parser.add_argument("-l","--login", metavar=('Username','Password'), nargs = 2, help="Crunchyroll login: -l User password. if your password has a blank, use double quotation marks (\"). Example: \"This is a password.\"")
parser.add_argument("-g","--guest", action='store_true', help="Crunchyroll login as guest")
parser.add_argument("-s","--subs-only", action='store_true', help="Download Crunchyroll Anime Subtitle only. if you get an error, try using double quotation marks (\")")
parser.add_argument("-q","--queue", type=str, nargs = '?', metavar='Queue Directory', const='.\\queue.txt', help="Run List of Crunchyroll Anime Link in queue file")
parser.add_argument("-d","--debug", action='store_true', help="Run crunchy-xml-decoder in Debug Mode")
parser.add_argument("-ds","--default-settings", action='store_true', help="Restore default settings")
arg = parser.parse_args()
sys.argv=[]
#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#(    )#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#
def queueu(queuepath):
    if not os.path.exists(queuepath):
        open(queuepath, 'w').write(u'#the any line that has hash before the link will be skiped\n')
        subprocess.call('notepad.exe '+queuepath)
    lines = open(queuepath).readlines()
    for line in lines:
        if line.rstrip('\n') ==''.join(line.rstrip('\n').split('#', 1)):
            #print ''.join(line.rstrip('\n').split('#', 1))
            ultimate.ultimate(line.rstrip('\n'), '', '')
            for i in range(0, len(lines)):
                if lines[i]== line:
                    lines[i]='#'+lines[i]
                    new_line_2=''
                    for new_line_ in lines:
                        try:
                            new_line_2=new_line_2+new_line_
                        except:
                            new_line_2=new_line_
                    open(queuepath, 'w').write(new_line_2)

def makechoise():
    seleccion = 0
    print '''Options:
0.- Exit
1.- Download Anime 
2.- Download Subtitle only
3.- Login
4.- Login As Guest
5.- Run Queue
6.- Restore default settings
'''
    try:
        seleccion = int(input("> "))
    except:
        try:
            os.system('cls')
        except:
            try:
                os.system('clear')
            except:
                pass
        print "ERROR: Invalid option."
        makechoise()
    if seleccion == 1 :
        ultimate.ultimate(raw_input('Please enter Crunchyroll video URL:\n'), '', '')
    elif seleccion == 2 :
        decode.decode(raw_input('Please enter Crunchyroll video URL:\n'))
    elif seleccion == 3 :
        username = raw_input(u'Username: ')
        password = getpass('Password(don\'t worry the password are typing but hidden:')
        login.login(username, password)
        makechoise()
    elif seleccion == 4 :
        login.login('', '')
        makechoise()
    elif seleccion == 5 :
        queueu('.\\queue.txt')
    elif seleccion == 6 :
        defaultsettings()
        makechoise()
    elif seleccion == 7 :
        import debug
    elif seleccion == 0 :
        sys.exit()
    else:
        try:
            os.system('cls')
        except:
            try:
                os.system('clear')
            except:
                pass
        print "ERROR: Invalid option."
        makechoise()
#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#(    )#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#
if arg.url:
    page_url = arg.url
if arg.season_number:
    seasonnum = arg.season_number[0]
else:
    seasonnum = ''
if arg.episode_number:
    epnum = arg.episode_number[0]
else:
    epnum = ''
if arg.guest:
    login.login('', '')
if arg.login:
    username = arg.login[0]
    password = arg.login[1]
    login.login(username, password)
if arg.debug:
    import debug
    sys.exit()
if arg.subs_only:
    if arg.url:
        decode.decode(page_url)
    else:
        decode.decode(raw_input('Please enter Crunchyroll video URL:\n'))
    sys.exit()
if arg.default_settings:
    defaultsettings()
    sys.exit()
if arg.queue:
    queueu(arg.queue)
if arg.url and not arg.subs_only:
    ultimate.ultimate(page_url, seasonnum, epnum)
else:
    makechoise()

























#print 'username'
#print 'password'
#print 'page_url'
#print 'seasonnum'
#import ultimate