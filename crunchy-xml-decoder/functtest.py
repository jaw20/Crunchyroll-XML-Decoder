import sys

#from lxml import etree
#print(etree.LXML_VERSION)
#print sys.argv[1]
if sys.argv[1] == 'Crypto_':
    from Crypto.Cipher import AES
else:
    if sys.argv[1] == 'lxml_':
        #from lxml import __init__
        from lxml import etree
        #print('test')
        #etree.LXML_VERSION
    else:
        print('Function Error')