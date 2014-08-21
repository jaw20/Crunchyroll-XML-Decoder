import cookielib
import fileinput
import sys
import re
import requests


def login(user, passw):
    lheaders = [('Referer', 'https://www.crunchyroll.com/login'),
                ('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; rv:26.0) Gecko/20100101 Firefox/26.0'),
                ('Content-Type', 'application/x-www-form-urlencoded')]

    loginurl = 'https://www.crunchyroll.com/?a=formhandler'
    payload = {'formname': 'RpcApiUser_Login', 'fail_url': 'http://www.crunchyroll.com/login',
               'name': user, 'password': passw}
    res = requests.post(loginurl, params=payload, cookies=cookie_jar, headers=lheaders)
    return res.text

try:
    with open('cookies.txt'):
        pass
except IOError:
    cookie_jar = cookielib.MozillaCookieJar('cookies.txt')
    cookie_jar.save()
if sys.argv[1][0] == 'n':
    print 'No cookies created.'
    sys.exit()
else:
    cookie_jar = cookielib.MozillaCookieJar('cookies.txt')
    cookie_jar.load()
    username = raw_input('Username: ')
    password = raw_input('Password: ')
    login(username, password)
    for c in cookie_jar:
        c.expires = 9999999999  # Saturday, November 20th 2286, 17:46:39 (GMT)

    headers = [('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; rv:26.0) Gecko/20100101 Firefox/26.0'),
               ('Connection', 'keep-alive')]
    url = 'http://www.crunchyroll.com/'
    site = requests.get(url, cookies=cookie_jar, headers=headers).text
    if re.search(username+'(?i)', site):
        print 'Login successful.'
        cookie_jar.save()

        for line in fileinput.input('cookies.txt', inplace=1):
            line = line.strip()
            if not 'c_visitor' in line:
                print line
    else:
        print 'Login failed.'
        sys.exit()
