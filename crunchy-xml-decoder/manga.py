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
from itertools import izip
from time import sleep

userdata = shelve.open('shelf', writeback=True)

"""
Start API crap that needs rewriting (mostly stolen from another CR script)
"""


def makeapi(method, options):
    # print "Crunchyroll ----> get JSON"
    if method == 'list_chapter':
        payload = {'api_ver': userdata['API_VERSION'], 'format': 'json'}
    else:
        payload = {'api_ver': userdata['API_VERSION'], 'device_type': userdata['API_DEVICE_TYPE'], 'format': 'json'}
    payload.update(options)
    headers = userdata['API_HEADERS']
    url = userdata['API_URL']+'/'+method
    global session
    req = session.get(url, params=payload, headers=headers)
    if req.status_code == 404:
        # print 'Caught 404, trying again in 4s.'
        sleep(4)
        req = session.get(url, params=payload, headers=headers)
    json_data = req.text
    return json.loads(json_data)


def floatint(num):
    if float(num) % 1 == 0:
        return str(int(float(num)))
    else:
        return str(float(num))


def decrypt(jpeg):
    return ''.join(chr(ord(b) ^ 66) for b, in izip(jpeg))


def login():
    # Load Persistent Vars
    global userdata
    try:
        change_language = "0"
        userdata['username'] = 'username'
        userdata['password'] = 'password'

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

        if not 'device_id' in userdata:
            char_set = string.ascii_letters + string.digits
            device_id = ''.join(random.sample(char_set, 15))
            userdata["device_id"] = device_id
            print 'Crunchyroll ----> New device_id created. New device_id is: ' + str(device_id)
        userdata['API_URL'] = 'http://api-manga.crunchyroll.com'
        userdata['API_HEADERS'] = {'User-Agent': 'Manga/2.1.2.2 (iPod touch; iOS 6.1.6; Scale/2.00)',
                                   'Host': 'api-manga.crunchyroll.com', 'Accept-Encoding': 'gzip, deflate',
                                   'Content-Type': 'application/x-www-form-urlencoded', 'Connection': 'keep-alive'}
        ### Android ###
        # userdata['API_VERSION'] = "1.0"
        # userdata['API_ACCESS_TOKEN'] = 'FLpcfZH4CbW4muO'  # formerly '1M8BbXptBS4VhMP'
        # userdata['API_DEVICE_TYPE'] = 'com.crunchyroll.manga.android'  # formerly 'com.crunchyroll.manga.crunchyroid'

        ### Flash ###
        # userdata['API_VERSION'] = "1"
        # userdata['API_ACCESS_TOKEN'] # none, refactor code for this
        # userdata['API_DEVICE_TYPE'] = 'com.crunchyroll.manga.flash'

        ### iOS ###
        userdata['API_VERSION'] = "1.0"
        userdata['API_ACCESS_TOKEN'] = 'Ge9rurkgXzzmzZQ'
        userdata['API_DEVICE_TYPE'] = 'com.crunchyroll.manga.iphone'

        userdata.setdefault('premium_type', 'UNKNOWN')
        current_datetime = datetime.datetime.now(dateutil.tz.tzutc())

    except:
        current_datetime = datetime.datetime.now(dateutil.tz.tzutc())
        print "Unexpected error:", sys.exc_info()
        userdata['session_id'] = ''
        userdata['auth_expires'] = current_datetime - dateutil.relativedelta.relativedelta(hours=+24)
        userdata['premium_type'] = 'unknown'
        userdata['auth_token'] = ''
        userdata['session_expires'] = current_datetime - dateutil.relativedelta.relativedelta(hours=+24)
        print "Crunchyroll Catch"
        return False

    # Create unique device_id or receive the existing device_id
    try:
        # userdata['username'] = __settings__.getSetting("crunchy_username")
        # userdata['password'] = __settings__.getSetting("crunchy_password")
        if not 'device_id' in userdata:
            char_set = string.ascii_letters + string.digits
            device_id = ''.join(random.sample(char_set, 15))
            userdata["device_id"] = device_id
            print "Crunchyroll ----> New device_id created. New device_id is: " + str(device_id)
        userdata.setdefault('premium_type', 'UNKNOWN')
        current_datetime = datetime.datetime.now(dateutil.tz.tzutc())
    except:
        print "Unexpected error:", sys.exc_info()
        userdata['session_id'] = ''
        userdata['auth_expires'] = current_datetime - dateutil.relativedelta.relativedelta(hours=+24)
        userdata['premium_type'] = 'unknown'
        userdata['auth_token'] = ''
        userdata['session_expires'] = current_datetime - dateutil.relativedelta.relativedelta(hours=+24)
        print "Crunchyroll Catch"
        return False

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
            # userdata['session_id'] = requests.get('http://www.crunblocker.com/sess_id.php').text
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
                # userdata['session_id'] = requests.get('http://www.crunblocker.com/sess_id.php').text
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

    # This is here as a catch all in case something gets messed up along the way.
    # Remove userdata variables so we start a new session next time around.
    else:
        del userdata['session_id']
        del userdata['auth_expires']
        del userdata['premium_type']
        del userdata['auth_token']
        del userdata['session_expires']
        print "Crunchyroll ----> Something in the login process went wrong."
        return False
"""
End API crap
"""

session = requests.session()

login()

# seriesid = input('input series id: ')
# manga_url = raw_input('Input url to the series: ')
# manga_url = sys.argv[1]
# seriesid = requests.get(manga_url).text
# seriesid = re.findall('<span id=\"sharing_add_queue_button\" group_id=\"([0-9]+)\"></span>', seriesid).pop()
mangalist = makeapi('list_series', {'content_type': 'jp_manga'})
for i in mangalist:
    seriesid = i['series_id']
    # if i['total_chapters'] == 0:
        # print i['locale'][userdata['API_LOCALE']]['name']+' has no chapters'
        # continue

    manga_name = i['locale'][userdata['API_LOCALE']]['name'].replace('/', ' - ').replace(':', '-')\
        .replace('?', '.').replace('"', '\'').strip()
    try:
        os.mkdir(manga_name)
    except OSError:
        pass

    files = [name for name in os.listdir(manga_name) if name.endswith('.cbz')]
    chapters = len(files)
    # print manga_name, i['total_chapters'], chapters
    if i['total_chapters'] <= chapters:
        series = makeapi('list_chapters', {'series_id': seriesid, 'user_id': userdata['user_id']})
        maxnum = 0
        for f in files:
            f = float(re.findall('#([.\d]+)', f)[0].rstrip('.'))
            if f > maxnum:
                maxnum = f
        if float(series['chapters'][-1]['number']) == maxnum:
            print 'No new chapters found for '+i['locale'][userdata['API_LOCALE']]['name']
            continue
        # else:
            # print 'ERROR: '+manga_name+' has '+str(float(series['chapters'][-1]['number']))+' on CR, '
            # +str(maxnum)+' on disk'

    else:
        series = makeapi('list_chapters', {'series_id': seriesid, 'user_id': userdata['user_id']})

    # chapter = input('input chapter number: ')
    # c = series['chapters'][chapter-1]
    for c in series['chapters']:
        # chapterid = c['chapter_id']
        chap_name = c.get('locale', '')
        if chap_name:
            chap_name = chap_name[userdata['API_LOCALE']]['name'].replace('/', ' - ')\
                .replace(':', '-').replace('?', '.').replace('"', '\'').strip()
        vol_num = c['volume_number']
        if vol_num == u'0' or vol_num is None:
            vol_num = u'S'
        vol_num = 'V'+vol_num

        # zipname = manga_name+' #'+floatint(i['number'])+'.cbz'

        cnum = floatint(c['number'])

        if chap_name != '':
            if chap_name == 'Chapter '+floatint(c['number']):
                zipname = manga_name+' '+vol_num+' #'+cnum+'.cbz'
            else:
                zipname = manga_name+' '+vol_num+' #'+cnum+' - '+chap_name+'.cbz'
        else:
            zipname = manga_name+' '+vol_num+' #'+cnum+'.cbz'

        if os.path.exists(manga_name+'\\'+zipname):
            continue

        # print 'WE GOT '+str(c['number'])+' (and high hopes)'
        # comic = makeapi('list_chapter', {'chapter_id': str(chapterid),
                                         # 'session_id': userdata['session_id'], 'auth': userdata['auth_token']})
        comic = makeapi('list_chapter', {'series_id': seriesid, 'chapter_num': cnum,
                                         'session_id': userdata['session_id'], 'auth': userdata['auth_token']})

        try:
            covername = manga_name+' '+vol_num+'.jpg'
            if not os.path.exists(manga_name+'\\'+covername):
                cover = session.get(url=comic['volume']['encrypted_image_url']).content
                open(covername, 'wb').write(decrypt(cover))
                shutil.move(covername, manga_name+'\\'+covername)
        except TypeError:
            pass

        # print 'STILL GOING? GOOD.'
        print manga_name+': '+floatint(c['number'])+'/'+floatint(series['chapters'][-1]['number'])

        myzip = ZipFile(zipname, 'w', zipfile.ZIP_DEFLATED)

        totalp = len(comic['pages'])
        ind = 1
        for p in comic['pages']:
            if not p['locale'] or not p['locale'][userdata['API_LOCALE']]['encrypted_composed_image_url']:
                image = session.get(url=p['image_url'], timeout=16).content
            else:
                image = session.get(url=p['locale'][userdata['API_LOCALE']]['encrypted_composed_image_url'], timeout=16).content
            if len(image) == 0:
                print 'Page '+str(ind)+' is missing, skipping.'
                ind += 1
                continue
            name = 'P'+str(ind).zfill(4)+'.jpg'
            myzip.writestr(name, decrypt(image))
            status = 'Downloaded page '+str(ind)+'/'+str(totalp)
            status += chr(8) * (len(status) + 1)
            print status,
            ind += 1
            # sleep(0.5)
        myzip.close()

        shutil.move(zipname, manga_name+'\\'+zipname)