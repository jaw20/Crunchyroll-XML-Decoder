import sys
import os
import datetime
import shelve
import random
import re
import string
import json
import dateutil.tz
import dateutil.relativedelta
import dateutil.parser
import requests
import zipfile
import shutil
from zipfile import ZipFile

userdata = shelve.open('shelf', writeback=True)


def makeapi(method, options):
    print "Crunchyroll ----> get JSON"
    payload = {'api_ver': userdata['API_VERSION'], 'device_type': userdata['API_DEVICE_TYPE']}
    payload.update(options)
    headers = userdata['API_HEADERS']
    url = userdata['API_URL']+'/'+method
    req = requests.post(url, params=payload, headers=headers)
    json_data = req.text
    return json.loads(json_data)


def floatint(num):
    if float(num) % 1 == 0:
        return str(int(float(num)))
    else:
        return str(float(num))


def login():
    # Load Persistent Vars
    global userdata

    change_language = "0"

    if change_language == "0":
        userdata.setdefault('API_LOCALE', "enUS")
    elif change_language == "1":
        userdata['API_LOCALE'] = "enUS"
    elif change_language == "2":
        userdata['API_LOCALE'] = "enGB"
    elif change_language == "3":
        userdata['API_LOCALE'] = "jaJP"
    elif change_language == "4":
        userdata['API_LOCALE'] = "frFR"
    elif change_language == "5":
        userdata['API_LOCALE'] = "deDE"
    elif change_language == "6":
        userdata['API_LOCALE'] = "ptBR"
    elif change_language == "7":
        userdata['API_LOCALE'] = "ptPT"
    elif change_language == "8":
        userdata['API_LOCALE'] = "esLA"
    elif change_language == "9":
        userdata['API_LOCALE'] = "esES"

    userdata['API_URL'] = 'http://api-manga.crunchyroll.com'
    userdata['API_HEADERS'] = {'User-Agent': 'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0)',
                               'Host': 'api-manga.crunchyroll.com', 'Accept-Encoding': 'gzip, deflate',
                               'Content-Type': 'application/x-www-form-urlencoded', 'Connection': 'Keep-Alive'}
    userdata['API_VERSION'] = "1"
    userdata['API_DEVICE_TYPE'] = 'com.crunchyroll.manga.flash'

    # userdata['username'] = __settings__.getSetting("crunchy_username")
    # userdata['password'] = __settings__.getSetting("crunchy_password")
    userdata.setdefault('premium_type', 'UNKNOWN')
    current_datetime = datetime.datetime.now(dateutil.tz.tzutc())

    # Check to see if a session_id doesn't exist or if the current auth token is invalid
    # and if so start a new session and log it in.
    if (not 'session_id' in userdata) or (not 'auth_expires' in userdata)\
            or current_datetime > userdata['auth_expires']:
        # Start new session
        print "Crunchyroll ----> Starting new session"
        request = makeapi('cr_start_session', {'device_id': userdata["device_id"],
                                               'access_token': userdata['API_ACCESS_TOKEN']})
        # print request
        if request['error'] is False:
            userdata['session_id'] = request['data']['session_id']
            userdata['session_expires'] = (current_datetime + dateutil.relativedelta.relativedelta(hours=+4))
            userdata['test_session'] = current_datetime
            print "Crunchyroll ----> New session created! Session ID is: " + str(userdata['session_id'])
        elif request['error'] is True:
            print "Crunchyroll ----> Error starting new session. Error message is: " + str(request['message'])
            return False
        # Login the session we just started.
        if not userdata['username'] or not userdata['password']:
            print "Crunchyroll ----> No Username or Password set"
            print "Crunchyroll ----> NO CRUNCHYROLL ACCOUNT FOUND!"
            return False
        else:
            print "Crunchyroll ----> Logging in the new session we just created."
            char_set = string.ascii_letters + string.digits
            hash_id = ''.join(random.sample(char_set, 40))
            userdata["hash_id"] = hash_id
            request = makeapi('cr_login', {'session_id': userdata['session_id'],
                                           'password': userdata['password'],
                                           'account': userdata['username'],
                                           'hash_id': userdata["hash_id"]})
            # print request
            if request['error'] is False:
                userdata['auth_token'] = request['data']['auth']
                userdata['auth_expires'] = dateutil.parser.parse(request['data']['expires'])
                userdata['user_id'] = request['data']['user']['user_id']
                userdata['premium_type'] = 'free'\
                    if not request['data']['user']['premium'] else request['data']['user']['premium']
                print "Crunchyroll ----> Login successful."
            elif request['error'] is True:
                print "Crunchyroll ----> Error logging in new session. Error message was: " + str(request['message'])
                return False
        # Verify user is premium
        if userdata['premium_type'] in 'anime|drama|manga':
            print "Crunchyroll ----> User is a premium "+str(userdata['premium_type'])+" member."
            return True
        else:
            print "Crunchyroll ----> User is not premium. "
            return True

    # Check to see if a valid session and auth token exist and if so reinitialize a new session using the auth token.
    elif "session_id" in userdata and "auth_expires" in userdata\
            and userdata['auth_expires'] > current_datetime > userdata['session_expires']:

        # Restart new session
        print "Crunchyroll ----> Valid auth token was detected. Restarting session."
        request = makeapi('cr_start_session', {'device_id': userdata["device_id"],
                                               'access_token': userdata['API_ACCESS_TOKEN'],
                                               'auth': userdata['auth_token']})
        try:
            if request['error'] is False:
                userdata['session_id'] = request['data']['session_id']
                userdata['auth_expires'] = dateutil.parser.parse(request['data']['expires'])
                userdata['premium_type'] = 'free'\
                    if not request['data']['user']['premium'] else request['data']['user']['premium']
                userdata['auth_token'] = request['data']['auth']
                # 4 hours is a guess. Might be +/- 4.
                userdata['session_expires'] = (current_datetime + dateutil.relativedelta.relativedelta(hours=+4))
                userdata['test_session'] = current_datetime
                print "Crunchyroll ----> Session restart successful. New session_id is: " + str(userdata['session_id'])

                # Verify user is premium
                if userdata['premium_type'] in 'anime|drama|manga':
                    print "Crunchyroll ----> User is a premium "+str(userdata['premium_type'])+" member."
                    return True
                else:
                    print "Crunchyroll ----> User is not premium."
                    return True

            elif request['error'] is True:
                # Remove userdata so we start a new session next time around.
                del userdata['session_id']
                del userdata['auth_expires']
                del userdata['premium_type']
                del userdata['auth_token']
                del userdata['session_expires']
                print "Crunchyroll ----> Error restarting session. Error message was: " + str(request['message'])
                userdata.Save()
                return False
        except:
            userdata['session_id'] = ''
            userdata['auth_expires'] = current_datetime - dateutil.relativedelta.relativedelta(hours=+24)
            userdata['premium_type'] = 'unknown'
            userdata['auth_token'] = ''
            userdata['session_expires'] = current_datetime - dateutil.relativedelta.relativedelta(hours=+24)
            print "Crunchyroll ----> Error restarting session. Error message was: " + str(request['message'])
            userdata.Save()
            return False

    # If we got to this point that means a session exists and it's still valid, we don't need to do anything.
    elif "session_id" in userdata and current_datetime < userdata['session_expires']:
        # This section below is Stupid Slow
        # return True
        if userdata['test_session'] is None or current_datetime > userdata['test_session']:
            # Test once every 10 min
            userdata['test_session'] = (current_datetime + dateutil.relativedelta.relativedelta(minutes=+10))
            print "Crunchyroll ----> A valid session was detected. Using existing session_id of: "\
                  + str(userdata['session_id'])
            # Verify user is premium
            if userdata['premium_type'] in 'anime|drama|manga':
                print "Crunchyroll ----> User is a premium "+str(userdata['premium_type'])+" member."
                return True
            else:
                print "Crunchyroll ----> User is not premium."
                return True

login()

# seriesid = input('input series id: ')
# manga_url = raw_input('Input url to the series: ')
manga_url = sys.argv[1]
seriesid = requests.get(manga_url).text
seriesid = re.findall('<span id=\"sharing_add_queue_button\" group_id=\"([0-9]+)\"></span>', seriesid).pop()
series = makeapi('list_chapters', {'series_id': seriesid, 'user_id': userdata['user_id']})
manga_name = series['series']['locale'][userdata['API_LOCALE']]['name'].replace('/', ' - ')\
    .replace(':', '-').replace('?', '.').replace('"', '\'').strip()
try:
    os.mkdir(manga_name)
except OSError:
    pass

# chapter = input('input chapter number: ')
# i = series['chapters'][chapter]
for i in series['chapters']:
    print i['number']
    chapterid = i['chapter_id']
    chap_name = i['locale'][userdata['API_LOCALE']]['name'].replace('/', ' - ')\
        .replace(':', '-').replace('?', '.').replace('"', '\'').strip()
    vol_num = i['volume_number']
    if vol_num == u'0':
        vol_num = u'S'

    if chap_name != '':
        if chap_name == 'Chapter '+floatint(i['number']):
            zipname = manga_name+' V'+vol_num+' #'+floatint(i['number'])+'.cbz'
        else:
            zipname = manga_name+' V'+vol_num+' #'+floatint(i['number'])+' - '+chap_name+'.cbz'
    else:
        zipname = manga_name+' V'+vol_num+' #'+floatint(i['number'])+'.cbz'

    if os.path.exists(manga_name+'\\'+zipname):
        continue

    myzip = ZipFile(zipname, 'w', zipfile.ZIP_DEFLATED)

    comic = makeapi('list_chapter', {'chapter_id': str(chapterid),
                                     'session_id': userdata['session_id'], 'auth': userdata['auth_token']})

    if vol_num != 'S':
        cover = requests.get(url=comic['volume']['encrypted_image_url']).content
        covername = manga_name+' V'+vol_num+'.jpg'
        coverf = open(covername, 'wb')
        coveri = []
        for b in cover:
            coveri.append(chr(ord(b) ^ 66))
        coverf.write(''.join(coveri))
        coverf.close()
        shutil.move(covername, manga_name+'\\'+covername)

    totalp = len(comic['pages'])
    for p in comic['pages']:
        if not p['locale']:
            image = requests.get(url=p['image_url']).content
        else:
            image = requests.get(url=p['locale'][userdata['API_LOCALE']]['encrypted_composed_image_url']).content
        name = 'P'+p['number'].zfill(4)+'.jpg'
        imagei = []
        for b in image:
            imagei.append(chr(ord(b) ^ 66))
        myzip.writestr(name, ''.join(imagei))
        print 'Downloaded page '+p['number']+'/'+str(totalp)
    myzip.close()

    shutil.move(zipname, manga_name+'\\'+zipname)