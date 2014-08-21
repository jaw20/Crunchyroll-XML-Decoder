# -*- coding: utf-8 -*-
"""
Subtitle Decoder
Uses some library files from
http://xbmc-addon-repository.googlecode.com
Thanks!
"""
import lxml
import os
import re
import requests
import subprocess
import sys
import urllib
import urllib2
import urlparse
from bs4 import BeautifulSoup
from ConfigParser import ConfigParser
from crunchyDec import CrunchyDec
from unidecode import unidecode


def getHTML(url):
    parts = urlparse.urlsplit(url)
    if not parts.scheme or not parts.netloc:
        print 'Apparently not an URL'
        sys.exit()
    payload = {'Referer': 'http://crunchyroll.com/', 'Host': 'www.crunchyroll.com',
               'User-Agent': 'Mozilla/5.0  Windows NT 6.1; rv:26.0 Gecko/20100101 Firefox/26.0'}
    res = requests.get(url, params=payload)
    return res.text


def getXML(req, media_id):
    url = 'http://www.crunchyroll.com/xml/'
    if req == 'RpcApiSubtitle_GetXml':
        payload = {'req':'RpcApiSubtitle_GetXml', 'subtitle_script_id':media_id}
    elif req == 'RpcApiVideoPlayer_GetStandardConfig':
        payload = {'req' : 'RpcApiVideoPlayer_GetStandardConfig', 'media_id' : media_id, 'video_format' : '0',
                   'video_quality' : '0', 'auto_play' : '1', 'show_pop_out_controls' : '1', 'current_page' : 'http://www.crunchyroll.com/'}
    else:
        payload = {'req' : req, 'media_id' : media_id, 'video_format' : '0', 'video_encode_quality' : '0'}
    headers ={'Referer':'http://static.ak.crunchyroll.com/flash/'+player_revision+'/StandardVideoPlayer.swf',
              'Host':'www.crunchyroll.com', 'Content-type':'application/x-www-form-urlencoded',
              'User-Agent':'Mozilla/5.0 (Windows NT 6.1; rv:26.0) Gecko/20100101 Firefox/26.0)'}
    res = requests.post(url, params=payload, headers=headers)
    return res.text

print 'Booting up...'
url = sys.argv[1]
if not url.startswith('http://') and not url.startswith('https://') :
    url = 'http://'+url
media_id = url[-6:]
html = getHTML(url)
try:
    player_revision = re.findall(r'flash\\/(.+)\\/StandardVideoPlayer.swf', html).pop()
except IndexError:
    url = url+'?skip_wall=1' #perv
    html = getHTML(url)
    try:
        player_revision = re.findall(r'flash\\/(.+)\\/StandardVideoPlayer.swf', html).pop()
    except IndexError:
        player_revision = '20130909142002.8076eb3d810c6daeb988fbfdeb3945ab' #update every so often, only used when the original page is region-locked, but that's what _start_proxy is for
soup = BeautifulSoup(html, 'lxml')
title = unidecode(unicode(soup.title.string)).replace('Crunchyroll - Watch ','').replace('/',' - ').replace(':','-').replace('?','.').replace('"','\'')
config = ConfigParser()
config.read('settings.ini')
lang = config.get('SETTINGS', 'language')
if lang == 'Espanol_Espana':
    lang = 'Espanol (Espana)'
elif lang == 'Francais':
    lang = 'Francais (France)'
elif lang == 'Portugues':
    lang = 'Portugues (Brasil)'
elif lang == 'English':
    lang = 'English|English (US)'
#xmlconfig = getXML('RpcApiVideoPlayer_GetStandardConfig', media_id)
#print xmlconfig
xmlmeta = BeautifulSoup(getXML('RpcApiVideoPlayer_GetMediaMetadata', media_id), 'xml')
vid_id = xmlmeta.find('media_id').string
xmlstream = getXML('RpcApiVideoEncode_GetStreamInfo', media_id)
if '<code>' in xmlstream:
    print 'Video (and subtitles) not available in your region, or cannot be found. (try _start_proxy)'
    sys.exit()
xmllist = getXML('RpcApiSubtitle_GetListing', vid_id)

xmllist = unidecode(xmllist)
if '<media_id>None</media_id>' in xmllist:
    print 'The video has hardcoded subtitles, or are region-locked.'
    sys.exit()

xmllist = xmllist.replace('><','>\r\n<')

try:
    sub_id = re.findall("id=([0-9]+)' title='.+"+lang.replace('(','\(').replace(')','\)')+"'", xmllist).pop()
    hardcoded = False
except IndexError:
    print 'The video\'s subtitles cannot be found, or are region-locked.'
    sys.exit()

xmlsub = getXML('RpcApiSubtitle_GetXml', sub_id)
formattedSubs = CrunchyDec().returnsubs(xmlsub)

try:
    subfile = open(title+'.ass', 'wb')
except IOError:
    title = title.split(' - ', 1)[0] #episode name too long, splitting after episode number
    subfile = open(title+'.ass', 'wb')
subfile.write(formattedSubs.encode('utf-8-sig'))
subfile.close()
subprocess.call('move /y "'+title+'.ass" ".\\export\\"', shell=True)
print 'Subtitles for '+title+' have been downloaded'
