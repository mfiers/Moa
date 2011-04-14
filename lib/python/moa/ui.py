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
import contextlib

import jinja2

import moa.logger as l
from moa.sysConf import sysConf

################################################################################
##
## user interface
##
################################################################################

FORMAT_CODES_ANSI = {
    'reset'     : chr(27) + "[0m",
    'bold'      : chr(27) + "[1m",
    'underline' : chr(27) + "[4m",
    
    'black'     : chr(27) + "[30m",
    'red'       : chr(27) + "[31m",
    'green'     : chr(27) + "[32m",
    'yellow'    : chr(27) + "[33m",
    'blue'      : chr(27) + "[34m",
    'white'     : chr(27) + "[37m",

    'bred'      : chr(27) + "[41m",
    'bgreen'    : chr(27) + "[42m",
    'byellow'   : chr(27) + "[42m",
    }

FORMAT_CODES_NOANSI = dict([(x,"") for x in FORMAT_CODES_ANSI.keys()])
 
def exitError(message):
    fprint("{{red}}{{bold}}Error:{{reset}} %s" % message, f='jinja')
    sys.exit(-1)

def error(message):
    fprint("{{red}}{{bold}}Error:{{reset}} %s" % message, f='jinja')

def message(message):
    fprint("{{green}}Note:{{reset}} %s" % message, f='jinja')
    
def warn(message):
    fprint("{{blue}}Warning:{{reset}} %s" % message, f='jinja')

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

    if f == 'text':
        rt += message % codes
    elif f == 'jinja':
        template = jinja2.Template(message)
        rt += template.render(**codes)
    if newline:
        rt += "\n"
        
    return rt


################################################################################
##
## readline enabled user prompt
##
################################################################################

## Handle moa directories
def fsCompleter(text, state):
    if os.path.isdir(text) and not text[-1] == '/': text += '/'
    pos = glob.glob(text + '*')
    try:
        return pos[state]
    except IndexError:
        return None
    
def askUser(prompt, d):
    
    def startup_hook():
        readline.insert_text('%s' % d)
  
    readline.set_completer_delims("\n `~!@#$%^&*()-=+[{]}\|;:'\",<>?")
    #readline.set_pre_input_hook(_rl_set_hook)

    readline.set_startup_hook(startup_hook)

    readline.set_completer(fsCompleter)
    readline.parse_and_bind("tab: complete")
    
    vl = raw_input(prompt)

    readline.set_startup_hook() 
    return vl 
    
