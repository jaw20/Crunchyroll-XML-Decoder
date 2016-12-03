import sys
import linecache
import os
import re
import shutil
import subprocess
import sys
import HTMLParser
import altfuncs
import ultimate

from bs4 import BeautifulSoup
from crunchyDec import CrunchyDec
from unidecode import unidecode
#import ultimate
debugfile = open('.\\debug.p.log', 'w')
def traceit(frame, event, arg):
    if event == "line":
        lineno = frame.f_lineno
        if "__file__" in frame.f_globals:
            filename = frame.f_globals["__file__"]
            if (filename.endswith(".pyc") or filename.endswith(".pyo")):
                filename = filename[:-1]
            line = linecache.getline(filename, lineno)
        else:
            line = ''
        #filename = frame.f_globals["__file__"]
        #if (filename.endswith(".pyc") or filename.endswith(".pyo")):
        #    filename = filename[:-1]
        name = frame.f_globals["__name__"]
        #line = linecache.getline(filename, lineno)
        #print "%s:%s: %s" % (name, lineno, line.rstrip())
        #print "%s: %s" % (lineno, debug_nice(frame.f_globals))

        debugvalue = str("%s:%s: %s\n%s" % (name, lineno, line.rstrip(), debug_nice(frame.f_globals)))+'\n'
        #print debugvalue
        debugfile.write(debugvalue)
        if "xmlconfig" in frame.f_globals:
            #xmlconfig = frame.f_globals["xmlconfig"]
            decodec_xml = open('.\\decodec_xml.txt', 'w')
            decodec_xml.write(str(frame.f_globals["xmlconfig"]))
            decodec_xml.close()
    return traceit

def debug_nice(locals_dict, keys=[]):
    globals()['types'] = __import__('types')
    exclude_keys = ['copyright', 'credits', 'False',
                    'SW_HIDE', 'STDOUT', 'STARTUPINFO',
                    'MAXFD', 'pywintypes', 'STARTF_USESTDHANDLES',
                    'PIPE', 'STD_ERROR_HANDLE', 'CREATE_NEW_CONSOLE',
                    'STARTF_USESHOWWINDOW', 'mswindows', 'STD_INPUT_HANDLE',
                    'CREATE_NEW_PROCESS_GROUP', 'STD_OUTPUT_HANDLE', 'Hashable',
                    'Sized', 'Set', 'Container', 'Iterator', 'ValuesView',
                    'MutableMapping', 'Sequence', 'Mapping', 'MutableSequence',
                    'Callable', 'Iterable', 'ItemsView', 'KeysView', 'MutableSet',
                    'MappingView', 'SafeConfigParser','RawConfigParser',
                    'MAX_INTERPOLATION_DEPTH', 'DEFAULTSECT', 'ConfigParser',
                    'True', 'None', 'Ellipsis', 'quit']
    exclude_valuetypes = [types.BuiltinFunctionType,
                          types.BuiltinMethodType,
                          types.ModuleType,
                          types.TypeType,
                          types.FunctionType
                          ]
    return {k: v for k,v in locals_dict.iteritems() if not
               (k in keys or k in exclude_keys or type(v) in exclude_valuetypes)
               and k[0] != '_'
               }
sys.settrace(traceit)




ultimate.ultimate('', '', '')
debugfile.close()
#ultimate()