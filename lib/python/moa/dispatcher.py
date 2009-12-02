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
moa wrapper for the API 
"""

import os
import sys
import site
import optparse
import subprocess

#moa specific libs - first prepare for loading libs
if not os.environ.has_key('MOABASE'):
    raise Exception("MOABASE is undefined")

#process the .pth file in the $MOABASE/bin folder !
site.addsitedir(os.path.join(os.environ['MOABASE'], 'lib', 'python'))

MOABASE = os.environ["MOABASE"]
TEMPLATEDIR = os.path.join(MOABASE, 'template')

##
## Read the moa configutation file 
ETC = {}
for line in open(os.path.join(MOABASE, 'etc', 'moa.conf.mk')).readlines():
    line = line.strip()
    if not line: 
        continue
    if line[0] == '#': 
        continue
    l = [x.strip() for x in line.split('=', 1)]
    if len(l) == 2:
        ETC[l[0]] = l[1]

import moa.template
import moa.archive
import moa.conf


def _startMake(d, args):
    """
    A function to run Make in a certain directory d with specific args
    """
    if type(args) == type("str"):
        args = [args]
    p = subprocess.Popen(
        ["make"] + args,
        shell=False,
        cwd = d,
        stdout = subprocess.PIPE,
        stderr = subprocess.PIPE)
    return p

def _runMake(d, args):
    """
    Do a full make run
    """
    p = _startMake(d, args)
    out, err = p.communicate()
    rc = p.returncode
    return rc, out, err

##
## API Command Dispatcher
## 

def _isMoaDir(d):
    if not os.path.exists(os.path.join(d, 'Makefile')):
        return False

def execute(d, args = []):
    """
    Execute 'make' in directory d
    """
    _startMake(d, args)

def _getProjectInfo(d):
    rc, out, err = _runMake(d, 'project_info')
    if rc != 0: return "", ""
    return out.strip().split(None, 1)
    

def isMoa(d):
    """ is directory d a 'moa' directory? """
    
    if not os.path.exists(os.path.join(d, 'Makefile')):
        return False
    rc, out, err = _runMake(d, 'is_moa')
    
    if not rc == 0: return False
    if not out.strip() == "Yes": return False
    return True

def info(d):
    
    rv = { 'directory' : d,
           'isMoaDir' : True}

    if not isMoa(d):
        rv['isMoaDir'] = False
        return rv

    projectRoot, projectTitle = _getProjectInfo(d)
    rv['projectRoot'] = projectRoot
    rv['projectTitle'] = projectTitle

    return rv
    
    


    
#     #Create new jobs
#     elif command == 'template':
#         moa.template.handler(options, newargs)
#     elif command == 'new':
#         #shortcut for moa template net
#         moa.template.new(options, newargs)

#     #pack & unpack trees
#     elif command == 'archive':
#         moa.archive.handler(options, newargs)
#     elif command == 'list':
#         #shortcut for moa template list
#         moa.template.list()
#     #configuration stuff
#     elif command == 'conf':
#         moa.conf.handler(options, newargs)
#     else:
#         #fire arguments of to make
#         l.debug('Running "make %s"' % (" ".join(sys.argv[1:])))
#         retcode = subprocess.call(["make"]+sys.argv[1:])
#         l.debug("Make returned with code %s" % retcode)
#         sys.exit(0)
