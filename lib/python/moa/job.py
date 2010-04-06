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
Create new jobs.
"""

import os
import re
import sys

import moa.utils
import moa.logger
import moa.conf
import moa.runMake

from moa.exceptions import *

l = moa.logger.l
    
MOABASE = os.environ["MOABASE"]
TEMPLATEDIR = os.path.join(MOABASE, 'template')

NEW_MAKEFILE_HEADER = """#!/usr/bin/env make
## Moa Makefile
## http://mfiers.github.com/Moa

include $(MOABASE)/template/moa/prepare.mk

## moa_preprocess & moa_postprocess are targets that can
## be overridden here. They are executed before & after
## the main execution

.PHONY: moa_preprocess
moa_preprocess:

.PHONY: moa_postprocess
moa_postprocess:

"""

        
def check(what):
    """
    Check if a template exists

        >>> check('gather')
        True
        >>> check('nonexistingtemplate')
        False

    """
    templatefile = os.path.join(TEMPLATEDIR, what + '.mk')
    if not os.path.exists(templatefile):
        return False
    return True

def list():
    """
    List all known templates

        >>> result = list()
        >>> len(result) > 0
        True
        >>> '__moaBase' in result
        False
        >>> type(result) == type([])
        True
        >>> 'gather' in result
        True
    """
    r = []
    for path, dirs, files in os.walk(TEMPLATEDIR):
        relPath = path.replace(TEMPLATEDIR, '')
        if relPath and relPath[0] == '/':
            relPath = relPath[1:]
        if relPath[:3] == 'moa' :
            continue
        if relPath[:4] == 'util' :
            continue
        if relPath and relPath[-1] != '/':
            relPath += '/'
        files.sort()
        for f in files:
            if f[0] == '.': continue
            if f[0] == '_': continue
            if f[0] == '#': continue
            if f[-1] == '~': continue
            if not '.mk' in f: continue
            r.append(relPath  + f.replace('.mk', ''))
    return r

def _getDescription(template):
    """ Parse a template and extract the moa_description """
    desc = ''
    with open(os.path.join(TEMPLATEDIR, '%s.mk' % template), 'r') as F:
        inDesc = False
        while True:
            line = F.readline()
            if not line: break
            line = line.strip()

            if inDesc:
                desc += " " + line
            elif line[:15] == 'moa_description':
                inDesc = True                
                desc = line.split('=', 1)[1].strip()
            if inDesc :
                if desc and desc[-1] == '\\':
                    desc = desc[:-1]
                else:
                    break
    return " ".join(desc.split())

def listLong():
    for template in list():
        yield template, _getDescription(template)

def newJob(template,
           title = None,
           wd = '.',
           parameters = [],
           force = False,
           noInit = False):
    """
    Create a new template based makefile in the current dir.


    >>> moa.utils.removeMoaFiles(P_EMPTY)
    >>> newJob(template = 'moatest',
    ...        title = 'test job creation',
    ...        wd=P_EMPTY,
    ...        parameters=['moa_precommand="ls"'])
    >>> os.path.exists(os.path.join(P_EMPTY, 'Makefile'))
    True
    >>> os.path.exists(os.path.join(P_EMPTY, 'moa.mk'))
    True
    >>> moa.conf.getVar(P_EMPTY, 'title')
    'test job creation'
    >>> moa.conf.getVar(P_EMPTY, 'moa_precommand')
    '"ls"'
    >>> moa.utils.removeMoaFiles(P_EMPTY)
        
    """
    l.debug("Creating template '%s'" % template)
    l.debug("- in wd %s" % wd)

    #is this a valid template??
    check(template)
            
    if not wd: wd = os.getcwd()
    if not os.path.isdir(wd):
        l.info("Creating wd %s" % wd)
        os.makedirs(wd)

    if not title and template != 'traverse':
        l.debug("no title (template %s)" % template)
        l.warning("It is strongly recommended to specify a title")
        l.warning("You can still do so by using moa set title='somthing meaningful'")
        title = ""

    if title:
        l.debug('creating a new moa makefile with title "%s" in %s' % (
            title, wd))
    else:
        l.debug('creating a new moa makefile in %s' % ( wd))

    makefile = os.path.join(wd, 'Makefile')
    moamk = os.path.join(wd, 'moa.mk')
    moamklock = os.path.join(wd, 'moa.mk.lock')
    
    if os.path.exists(makefile):
        l.debug("Makefile exists!")
        if not force:
            l.critical("makefile exists, use -f (--force) to overwrite")
            sys.exit(1)


    l.debug("Start writing %s" % makefile)
    F = open(makefile, 'w')
    F.write(NEW_MAKEFILE_HEADER)
    F.write("$(call moa_load,%s)\n" % template)

    #include moabase
    F.close()

    if title:
        with moa.utils.flock(moamklock):    
            moamkdata = []

            #open & rewrite an older moa.mk
            if os.path.exists(moamk):
                moamkdata = open(moamk).readlines()
                    
            F = open(moamk, 'w')
            for line in moamkdata:
                if re.match("^title *=", line) and title:
                    continue
                F.write(line)
                
            if title:
                F.write("title=%s\n" % title)
                l.debug("writing title=%s to moa.mk" % title)

            F.close()       
            l.debug('Written moa.mk')

    params = []
    for p in parameters:
        if not '=' in p: continue
        params.append(p)
        moa.conf.writeToConf(wd, moa.conf.parseClArgs(params))

    if noInit:
        return

    l.debug("Running moa initialization")
    moa.runMake.go(wd = wd,
                   target='initialize',
                   captureOut = False,
                   makeArgs=[],
                   verbose=False)                   
    l.debug("Written %s, try: moa help" % makefile)

