from sys import argv
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

userdata = shelve.open('login', writeback=True)


def makeapi(method, options):
    print "Crunchyroll ----> get JSON"
    payload = options
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

login()