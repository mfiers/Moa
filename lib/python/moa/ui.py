#!/usr/bin/env python
# Copyright 2009-2011 Mark Fiers
# The New Zealand Institute for Plant & Food Research
# 
# This file is part of Moa - http://github.com/mfiers/Moa
# 
# Licensed under the GPL license (see 'COPYING')
# 
"""
moa.ui
------

communicate information to the user
"""

import os
import re
import sys
import time
import glob
import errno
import shutil
import readline
import traceback
import subprocess
import contextlib


import jinja2

import moa.logger as l
from moa.sysConf import sysConf

################################################################################
##
## user interface
##
################################################################################

FORMAT_CODES_ANSI = {}

for c in sysConf.ansi:
    FORMAT_CODES_ANSI[c] = chr(27) + "["  + sysConf.ansi[c] + "m"
    
FORMAT_CODES_NOANSI = dict([(x,"") for x in FORMAT_CODES_ANSI.keys()])
 
def exitError(message=''):
    sysConf.pluginHandler.run("post_error")
    if message:
        fprint("{{green}}Moa{{reset}}:{{red}}{{bold}}Error:{{reset}} %s" % message, f='jinja')
    sys.exit(-1)

def exit(message):
    fprint("{{green}}Moa{{reset}}: %s" % message, f='jinja')
    sys.exit(-1)

def error(message):
    fprint("{{green}}Moa{{reset}}:{{red}}{{bold}}Error:{{reset}} %s" % message, f='jinja')

def message(message):
    fprint("{{green}}Moa:{{reset}} %s" % message, f='jinja')
    
def warn(message):
    fprint("{{green}}Moa{{reset}}:{{blue}}Warning:{{reset}} %s" % message, f='jinja')

def fprint(message, **kwargs):
    sys.stdout.write(fformat(message, **kwargs))
    
def fformat(message, f='text', newline = True, ansi = None):
    if f == 'text':
        l.debug("deprecated use of text formatter")

    if ansi == True:
        codes = FORMAT_CODES_ANSI
    elif ansi == False:
        codes = FORMAT_CODES_NOANSI
    else:
        if sys.stdout.isatty() and sysConf.use_ansi:
            codes = FORMAT_CODES_ANSI
        else:
            codes = FORMAT_CODES_NOANSI

    rt = ""

    if not f:
        rt += message
    elif f[0].lower() == 't':
        rt += message % codes
    elif f[0].lower() == 'j':
        template = jinja2.Template(message)
        rt += template.render(**codes)
    if newline:
        rt += "\n"
        
    return rt


################################################################################
##
## readline enabled user prompt
##
#########################################################################

## See if we can do intelligent things with job variables
def untangle(txt):
    return sysConf.job.conf.interpret(txt)
    
## Handle moa directories
_FSCOMPLETECACHE = {}

def fsCompleter(text, state):
    def g(*a):
        #pass
        with open('/tmp/fscomp.%d.log' % os.getuid(), 'a') as F:
            F.write("\t".join(map(str, a)) + "\n")

    g("text   : ", text)
    g("state  :", state)

    if _FSCOMPLETECACHE and text in _FSCOMPLETECACHE.keys():
        try:
            #rv = _FSCOMPLETECACHE[text]
            #g(str(rv))
            rv = _FSCOMPLETECACHE[text][state]
            g('from cache', rv)
            return rv
        except:
            g('%s' % _FSCOMPLETECACHE)
            g('cache problem')
            import traceback
            E = traceback.format_exc()
            g(E)
            return None

    #see what we should complete
    if '{{' in text:
        #remove spaces within jinja codes
        text2 = re.sub(r'{{\s*(\w*?)\s*}}', r'{{\1}}', text)
        g("rem {{ :", text2)        
    else:
        text2 = text

    #only trying to find a prefix for the last word of the current
    #string: stored in 'ctext'. The rest is in 'prefix'
    if ' ' in text2:
        addPrefix = True
        prefix, ctext = text2.rsplit(' ', 1)
    else:
        addPrefix = False
        prefix, ctext = "", text2

    g('prefix :', prefix)
    g('ctext  :', ctext)

    if '{{' in ctext:
        #jinja untangle
        cutext = untangle(ctext)
    else:
        cutext = ctext

    detangle = False
    if cutext != ctext:
        detangle = True

    g('untang :', cutext)
    
    if os.path.isdir(cutext) and not cutext[-1] == '/': 
        sep = '/'
    else: sep = ''

    
    if prefix or cutext[:2] == './' or \
            cutext[:3] == '../' or cutext[0] == '/':
        #try to expand path
        #get all possibilities
        pos = glob.glob(cutext + sep + '*')
    else:
        #see if there is an executable starting with this
        #
        #seems impossible - cannot call compgen from a script :(
        #cl = ("compgen -c %s" % cutext).split()
        #P = subprocess.Popen(cl, shell=False,
        #                     stdout=subprocess.PIPE,
        #                     stderr=subprocess.PIPE)
        #out, err = P.communicate()
        #print out
        #print err
        pos = []
        
    np = []
    for i, p in enumerate(pos):
        if os.path.isdir(p) and not p[-1] == '/':
            p += '/'
        if addPrefix:
            p = prefix + ' ' + p
        if detangle:
            p = p.replace(cutext, ctext)
        np.append(p)
    g('pos', np)

    _FSCOMPLETECACHE[text] = np
    g(_FSCOMPLETECACHE)
    try:
        rv = np[state]
        return rv
    except IndexError:
        return None
    
def askUser(prompt, d):
    
    def startup_hook():
        readline.insert_text('%s' % d)
  
    readline.set_completer_delims("\n`~!@#$%^&*()-=+[]\|;:'\",<>?")
    readline.set_startup_hook(startup_hook)

    readline.set_completer(fsCompleter)
    readline.parse_and_bind("tab: complete")
    
    vl = raw_input(prompt)

    readline.set_startup_hook() 
    return vl 
    
