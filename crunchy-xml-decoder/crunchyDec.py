from hashlib import sha1
from zlib import decompress
from base64 import b64decode
from bs4 import BeautifulSoup
from Crypto.Cipher import AES


class CrunchyDec:
    def __init__(self):
        pass

    def returnsubs(self, xml):
        _id, _iv, _data = self.strain(xml)
        print "Attempting to decrypt subtitles..."
        decryptedsubs = self.decode(_id, _iv, _data)

        formattedsubs = self.convert(decryptedsubs)
        print "Success!  Subtitles decrypted."
        return formattedsubs

    @staticmethod
    def strain(xml):
        soup = BeautifulSoup(xml, 'xml')
        subtitle = soup.find('subtitle', attrs={'link': None})
        if subtitle:
            _id = int(subtitle['id'])
            _iv = subtitle.iv.string
            _data = subtitle.data.string
            return _id, _iv, _data
        else:
            print "Couldn't parse XML file."

    @staticmethod
    def convert(script):
        soup = BeautifulSoup(script, 'xml')
        header = soup.find('subtitle_script')
        header = "[Script Info]\nTitle: "+header['title']+"\nScriptType: v4.00+\nWrapStyle: "+header['wrap_style']\
                 + "\nPlayResX: "+header['play_res_x']+"\nPlayResY: "+header['play_res_y']+"\n\n"
        styles = "[V4+ Styles]\nFormat: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, " \
                 "BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, " \
                 "Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding\n"
        events = "\n[Events]\nFormat: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n"
        stylelist = soup.findAll('style')
        eventlist = soup.findAll('event')

        for style in stylelist:
            if style['scale_x'] or style['scale_y'] == '0':
                style['scale_x'], style['scale_y'] = '100', '100'  # Fix for Naruto 1-8 where it's set to 0 but ignored
            styles += "Style: " + style['name'] + "," + style['font_name'] + "," + style['font_size'] + ","\
                      + style['primary_colour'] + "," + style['secondary_colour'] + "," + style['outline_colour'] + ","\
                      + style['back_colour'] + "," + style['bold'] + "," + style['italic'] + ","\
                      + style['underline'] + "," + style['strikeout'] + "," + style['scale_x'] + ","\
                      + style['scale_y'] + "," + style['spacing'] + "," + style['angle'] + ","\
                      + style['border_style'] + "," + style['outline'] + "," + style['shadow'] + ","\
                      + style['alignment'] + "," + style['margin_l'] + "," + style['margin_r'] + ","\
                      + style['margin_v'] + "," + style['encoding'] + "\n"

        for event in eventlist:
            events += "Dialogue: 0,"+event['start']+","+event['end']+","+event['style']+","\
                      + event['name']+","+event['margin_l']+","+event['margin_r']+","+event['margin_v']\
                      + ","+event['effect']+","+event['text']+"\n"

        formattedsubs = header+styles+events
        return formattedsubs

    # ---- CRYPTO -----

    @staticmethod
    def decode(mediaid, iv, data):
        # Do some black magic
        eq = (mediaid ^ 88140282) ^ (mediaid ^ 88140282) >> 3 ^ int(88140282 ^ mediaid) * 32
        # Creates a 160-bit SHA1 hash padded to 256-bit using zeroes
        key = sha1('$&).6CXzPHw=2N_+isZK' + str(eq)).digest()+'\x00'*12
        iv = b64decode(iv)
        data = b64decode(data)
        cipher = AES.new(key, AES.MODE_CBC, iv)
        decrypteddata = cipher.decrypt(data)
        return decompress(decrypteddata)
