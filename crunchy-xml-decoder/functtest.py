import sys
import os
import re
import platform
import subprocess
import shutil



python_bit_=re.findall("[0-9][0-9] bit",sys.version).pop()
python_version_=re.findall("[0-9]\.[0-9]",sys.version).pop()
Crypto_link_=""
lxml_link_=""
print "python version="+re.findall("[0-9]\.[0-9]\.[0-9]",sys.version).pop()+" "+python_bit_
print "OS Version="+platform.platform().replace("-"," ")
print "System Type="+os.environ['PROCESSOR_ARCHITECTURE']


if os.path.exists(".\\video-engine\\rtmpdump.exe"):
    bin_dir__="."
elif os.path.exists("..\\video-engine\\rtmpdump.exe"):
    bin_dir__=".."
else:
    print "Can't find the Binary Folder"
#python_bit_="645 bit"
#python_version_="3.3"
#print(re.findall("[0-9]\.[0-9]",sys.version).pop())
#from lxml import etree
#print(etree.LXML_VERSION)
#print sys.argv[1]
#if sys.argv[1] == 'Crypto_':
#    from Crypto.Cipher import AES
#else:
#    if sys.argv[1] == 'lxml_':
#        #from lxml import __init__
#        from lxml import etree
        #print('test')
        #etree.LXML_VERSION
#    else:
#        print('Function Error')
try:
    from Crypto.Cipher import AES
    print('Crypto installed')	
except ImportError:
    print('Crypto not installed')
    try:
        if python_bit_=="32 bit":
            Crypto_link_={'2.6':'http://www.voidspace.org.uk/downloads/pycrypto26/pycrypto-2.6.win32-py2.6.exe','2.7':'http://www.voidspace.org.uk/downloads/pycrypto26/pycrypto-2.6.win32-py2.7.exe','3.2':'http://www.voidspace.org.uk/downloads/pycrypto26/pycrypto-2.6.win32-py3.2.exe','3.3':'http://www.voidspace.org.uk/downloads/pycrypto26/pycrypto-2.6.win32-py3.3.exe'}[python_version_]
        elif python_bit_=="64 bit":
            Crypto_link_={'2.6':'http://www.voidspace.org.uk/downloads/pycrypto26/pycrypto-2.6.win-amd64-py2.6.exe','2.7':'http://www.voidspace.org.uk/downloads/pycrypto26/pycrypto-2.6.win-amd64-py2.7.exe','3.2':'http://www.voidspace.org.uk/downloads/pycrypto26/pycrypto-2.6.win-amd64-py3.2.exe','3.3':'http://www.voidspace.org.uk/downloads/pycrypto26/pycrypto-2.6.win-amd64-py3.3.exe'}[python_version_]
        else:
            Crypto_link_="Something Has Gone Wrong While Retrieving Crypto link\nPlease Download Crypto Manually"
    except KeyError:
        print "Something Has Gone Wrong While Retrieving Crypto link\nPlease Download Crypto Manually"
try:
    from lxml import etree
    print('lxml installed')
except ImportError:
    print('lxml not installed')
    try:
        if python_bit_=="32 bit":
            lxml_link_={'2.6':'https://pypi.python.org/packages/2.6/l/lxml/lxml-3.2.5.win32-py2.6.exe#md5=f93ea5c1bf9b72bdd8acbd72c794b1b5','2.7':'https://pypi.python.org/packages/2.7/l/lxml/lxml-3.2.5.win32-py2.7.exe#md5=00536d2ff2b5e9e0b221a936b6fff169','3.2':'https://pypi.python.org/packages/3.2/l/lxml/lxml-3.2.5.win32-py3.2.exe#md5=57479eea394d44c5ac0c66e383201029'}[python_version_]
        elif python_bit_=="64 bit":
            lxml_link_={'2.6':'https://pypi.python.org/packages/2.6/l/lxml/lxml-3.2.5.win-amd64-py2.6.exe#md5=90d59a70db1ab0bce2425d0de2aaa0da','2.7':'https://pypi.python.org/packages/2.7/l/lxml/lxml-3.2.5.win-amd64-py2.7.exe#md5=4382f7e29ef288e60975017dcd2cf361'}[python_version_]
        else:
            lxml_link_="Something Has Gone Wrong While Retrieving Lxml link\nPlease Download Lxml Manually"
    except KeyError:
        print "Something Has Gone Wrong While Retrieving Lxml link\nPlease Download Lxml Manually"

if Crypto_link_ or lxml_link_:
    if not os.path.exists("temp"):
        os.makedirs("temp")
if Crypto_link_:
    print Crypto_link_
    subprocess.call('video-engine\wget.exe -c --no-check-certificate -O "temp\crypto.exe" '+ Crypto_link_)
if lxml_link_:
    print lxml_link_
    subprocess.call('video-engine\wget.exe -c --no-check-certificate -O "temp\lxml.exe" '+ lxml_link_)
if Crypto_link_ or lxml_link_:
    print "Extracting....."
    try:
        subprocess.call(bin_dir__ + '\\video-engine\\7z_64.exe x -otemp\ temp\ ', stdout=open(os.devnull, 'w'))
    except:
        subprocess.call(bin_dir__ + '\\video-engine\\7z.exe x -otemp\ temp\ ', stdout=open(os.devnull, 'w'))

if os.path.exists("temp"):
    if os.path.exists(".\\temp\\PLATLIB\\Crypto"):
        shutil.move('.\\temp\\PLATLIB\\Crypto' , bin_dir__ + '\\crunchy-xml-decoder\\')
    if os.path.exists(".\\temp\\PLATLIB\\lxml"):
        shutil.move('.\\temp\\PLATLIB\\lxml' , bin_dir__ + '\\crunchy-xml-decoder\\')
    shutil.rmtree("temp")

