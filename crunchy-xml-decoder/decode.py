#!/usr/bin/python
"""
Subtitle Decoder
Uses some library files from
http://xbmc-addon-repository.googlecode.com
Thanks!
"""

# -*- coding: utf-8 -*-
# import lxml
import os
import re
import shutil
import subprocess
import sys
import HTMLParser

import altfuncs
from bs4 import BeautifulSoup
from crunchyDec import CrunchyDec
from unidecode import unidecode

# ----------


print 'Booting up...'
try:
    page_url = sys.argv[1]
except IndexError:
    page_url = raw_input('Please enter Crunchyroll video URL:\n')

lang = altfuncs.config()
player_revision = altfuncs.playerrev(page_url)
html = altfuncs.gethtml(page_url)

h = HTMLParser.HTMLParser()
title = re.findall('<title>(.+?)</title>', html)[0].replace('Crunchyroll - Watch ', '')
if len(os.getcwd()+'\\export\\'+title+'.ass') > 255:
	title = re.findall('^(.+?) \- ', title)[0]

### Taken from http://stackoverflow.com/questions/6116978/python-replace-multiple-strings ###
rep = {' / ':' - ', '/':' - ', ':':'-', '?':'.', '"':"''", '|':'-', '&quot;':"''", '*':'.'}

rep = dict((re.escape(k), v) for k, v in rep.iteritems())
pattern = re.compile("|".join(rep.keys()))
title = pattern.sub(lambda m: rep[re.escape(m.group(0))], title)

### End stolen code ###

media_id = page_url[-6:]
xmlconfig = BeautifulSoup(altfuncs.getxml('RpcApiVideoPlayer_GetStandardConfig', media_id), 'xml')

try:
    if '4' in xmlconfig.find_all('code')[0]:
        print xmlconfig.find_all('msg')[0].text
        sys.exit()
except IndexError:
    pass

vid_id = xmlconfig.find('media_id').string


xmllist = altfuncs.getxml('RpcApiSubtitle_GetListing', media_id)
xmllist = unidecode(xmllist).replace('><', '>\n<')

if '<media_id>None</media_id>' in xmllist:
    print 'The video has hardcoded subtitles.'
    hardcoded = True
    sub_id = False
else:
    try:
        sub_id = re.findall("id=([0-9]+)' title='.+" + lang.replace('(', '\(').replace(')', '\)') + "'", xmllist).pop()
        hardcoded = False
    except IndexError:
        try:
            sub_id = re.findall("id=([0-9]+)' title='.+English", xmllist).pop()  # default back to English
            print 'Language not found, reverting to English'
            lang = 'English|English (US)'
            hardcoded = False
        except IndexError:
            print "The video's subtitles cannot be found, or are region-locked."
            hardcoded = True
            sub_id = False

if not hardcoded:
    xmlsub = altfuncs.getxml('RpcApiSubtitle_GetXml', sub_id)
    formattedSubs = CrunchyDec().returnsubs(xmlsub)
    subfile = open(title + '.ass', 'wb')
    subfile.write(formattedSubs.encode('utf-8-sig'))
    subfile.close()
    shutil.move(title + '.ass', '.\export\\')

print 'Subtitles for '+title+' have been downloaded'
