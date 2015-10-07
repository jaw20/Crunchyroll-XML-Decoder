import sys
import re
import requests
import pickle
from getpass import getpass


def login(username, password):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0',
               'Connection': 'keep-alive'}
    session = requests.session()
    session.get('http://www.crunchyroll.com/', headers=headers)


    headers = {'Referer': 'https://www.crunchyroll.com/login',
               'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0',
               'Content-Type': 'application/x-www-form-urlencoded'}

    payload = {'formname': 'RpcApiUser_Login', 'fail_url': 'http://www.crunchyroll.com/login',
               'name': username, 'password': password}
    res = session.post('https://www.crunchyroll.com/?a=formhandler', data=payload, headers=headers).text
    for c in session.cookies:
        c.expires = 9999999999  # Saturday, November 20th 2286, 17:46:39 (GMT)

    del session.cookies['c_visitor']
    del session.cookies['sess_id']

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0',
               'Connection': 'keep-alive'}
    url = 'http://www.crunchyroll.com/'
    site = session.get(url, headers=headers).text
    if re.search(username+'(?i)', site):
        if username == '':
            print 'Login as Guest.'
        else:
            print 'Login successful.'
        pickle.dump(requests.utils.dict_from_cookiejar(session.cookies), open('cookies', 'w'))
        with open('cookies', 'w') as f:
            pickle.dump(requests.utils.dict_from_cookiejar(session.cookies), f)
    else:
        print 'Login failed.'
        sys.exit()

if __name__ == '__main__':
    try:
        if sys.argv[1][0] == 'y':
            username = raw_input(u'Username: ')
            password = getpass('Password(don\'t worry the password are typing but hidden:')
    except IndexError:
        username = ''
        password = ''
    login(username, password)