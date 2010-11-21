#!/usr/bin/env python
# 
# Copyright 2009 Mark Fiers, Plant & Food Research
# 
# This file is part of Moa - http://github.com/mfiers/Moa
# 
# Moa is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your
# option) any later version.
# 
# Moa is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
# or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public
# License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with Moa.  If not, see <http://www.gnu.org/licenses/>.
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

import moa.logger as l
import moa.sysConf
from moa.exceptions import *

################################################################################
##
## user interface
##
################################################################################

FORMAT_CODES_ANSI = {
    'reset' : chr(27) + "[0m",
    'bold' : chr(27) + "[1m",
    'underline' : chr(27) + "[4m",
    'black' : chr(27) + "[30m",
    'blue' : chr(27) + "[34m",
    'green' : chr(27) + "[32m",
    'red' : chr(27) + "[31m",
    }

FORMAT_CODES_NOANSI = dict([(x,"") for x in FORMAT_CODES_ANSI.keys()])
    
def fprint(message):
    sysConf = moa.sysConf.sysConf
    if sys.stdout.isatty() and sysConf.use_ansi:
        codes = FORMAT_CODES_ANSI
    else:
        codes = FORMAT_CODES_NOANSI
    print message % codes


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
    
def renumber(path, fr, to):
    """
    Renumber a moa job


    >>> import tempfile
    >>> emptyDir = tempfile.mkdtemp()
    >>> removeFiles(emptyDir, recursive=True)
    >>> fromDir = os.path.join(emptyDir, '10.test')
    >>> problemDir = os.path.join(emptyDir, '20.problem')
    >>> toDir = os.path.join(emptyDir, '20.test')
    >>> os.mkdir(os.path.join(emptyDir, '10.test'))
    >>> os.path.exists(os.path.join(emptyDir, '10.test'))
    True
    >>> os.path.exists(toDir)
    False
    >>> renumber(emptyDir, '10', '20')
    >>> os.path.exists(fromDir)
    False
    >>> os.path.exists(toDir)
    True
    >>> os.mkdir(problemDir)
    >>> renumber(emptyDir, '20', '30')
    Traceback (most recent call last):
      File '/opt/moa/lib/python/moa/utils.py', line 114, in renumber
        raise MoaFileError(fullDir)
    MoaFileError: Moa error handling file

    
    @param path: the path to operate in
    @type path: String
    @param fr: number to rename from
    @type fr: String representing a number
    @param to: number to rename to
    @type to: String representing a number
    """

    frDir = None
    toDir = None
    l.debug("moa ren %s %s" % (fr, to))
    for x in os.listdir(path):        
        if x[0] == '.' : continue
        
        fullDir = os.path.join(path, x)

        xsplit = x.split('.')
        if xsplit[0] == fr:
            if frDir:
                l.error("more than one directory starting with %s" % fr)
                raise MoaFileError(fullDir)
            frDir = fullDir
            toDir = os.path.join(path, to + "." + ".".join(xsplit[1:]))
        if xsplit[0] == to:
            l.error("target directory starting with %s already exists" % to)
            raise MoaFileError(fullDir)

    if not frDir:
        l.error("Cannot find a directory starting with %s" % fr)
        raise MoaFileError(path)
    if not toDir:
        l.error("Cannot find a directory starting with %s" % to)
        raise MoaFileError(path)
    
    if not os.path.isdir(frDir):
        l.error("%s is not a directory" % frDir)
        raise MoaFileError(frDir)
    #if not os.path.isdir(toDir):
    #    l.error("%s is not a directory" % toDir)
    #    raise MoaFileError(toDir)

    l.info("renaming: %s" % (frDir))
    l.info("  to: %s" % (toDir))
    os.rename(frDir, toDir)
        
