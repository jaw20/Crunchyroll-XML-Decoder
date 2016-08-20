import sys
import re
import requests
import pickle
from getpass import getpass

def getuserstatus(session=''):
    status = 'Guest'
    user1 = 'Guest'
    if session == '':
        session = requests.session()
        with open('cookies') as f:
            cookies = requests.utils.cookiejar_from_dict(pickle.load(f))
            session = requests.session()
            session.cookies = cookies
            del session.cookies['c_visitor']
    #print session.cookies #session = requests.session()
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0',
               'Connection': 'keep-alive'}
    site = session.get('https://www.crunchyroll.com/acct/membership', headers=headers, verify=True).text
    #open('tempfile','w').write(site).encoding('UTF-8')
    #print site.encode('utf-8')
    if re.search(re.escape('      ga(\'set\', \'dimension5\', \'registered\');'), site):
        status = 'Free Member'
    elif re.search(re.escape('      ga(\'set\', \'dimension5\', \'premium\');'), site):
        if re.search(re.escape('      ga(\'set\', \'dimension6\', \'premiumplus\');'), site):
            status = 'Premium+ Member'
        else:
            status = 'Premium Member'
    if status != 'Guest':
        user1 = re.findall('<a href=\"/user/(.+)\" ', site).pop()
    return [status,user1]

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

    #headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0',
    #           'Connection': 'keep-alive'}
    #url = 'http://www.crunchyroll.com/'
    #site = session.get(url, headers=headers).text
    #print session.get('https://www.crunchyroll.com/acct/membership/', headers=headers, verify=True).text.encode('utf-8')
    #print getuserstatus(session)
    #if re.search(username+'(?i)', site):
    #    if username == '':
    #        print 'Login as Guest.'
    #    else:
    #        print 'Login successful.'
    #    pickle.dump(requests.utils.dict_from_cookiejar(session.cookies), open('cookies', 'w'))
    #    with open('cookies', 'w') as f:
    #        pickle.dump(requests.utils.dict_from_cookiejar(session.cookies), f)
    #else:
    #    print 'Login failed.'
    #    sys.exit()
    userstatus = getuserstatus(session)
    if username != '' and userstatus[1] == 'Guest':
        print 'Login failed.'
        sys.exit()
    else:
        print 'Login as '+userstatus[0]+' successfully.'
        pickle.dump(requests.utils.dict_from_cookiejar(session.cookies), open('cookies', 'w'))
        with open('cookies', 'w') as f:
            pickle.dump(requests.utils.dict_from_cookiejar(session.cookies), f)	

if __name__ == '__main__':
    try:
        if sys.argv[1][0] == 'y':
            username = raw_input(u'Username: ')
            password = getpass('Password(don\'t worry the password are typing but hidden:')
    except IndexError:
        username = ''
        password = ''
    login(username, password)
