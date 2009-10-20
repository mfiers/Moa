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
Moa script - template related code
"""

import os
import re
import sys

import moa.utils
import moa.logger
l = moa.logger.l
    
MOABASE = os.environ["MOABASE"]
TEMPLATEDIR = os.path.join(MOABASE, 'template')

NEW_MAKEFILE_HEADER = """#!/usr/bin/env make
## Moa Makefile
## http://mfiers.github.com/Moa

-include moa.mk
MOAMK_INCLUDE=done

## moa_preprocess & moa_postprocess are targets that can
## be overridden here. They are executed before & after
## the main execution
moa_preprocess:
\t#write your code here

moa_postprocess:
\t#write your code here

dont_include_moabase=true
"""
def _check(what):
    """Check if a template exists"""
    templatefile = os.path.join(TEMPLATEDIR, what + '.mk')
    if not os.path.exists(templatefile):
        l.debug("cannot find %s" % templatefile)
        l.error("No template for %s exists" % what)
        sys.exit(1)        
    return True

def list():
    """
    List all known templates
    """
    r = []
    for f in os.listdir(TEMPLATEDIR):
        if f[0] == '.': continue
        if f[0] == '_': continue
        if f[0] == '#': continue
        if f[-1] == '~': continue
        if f == 'gsml': continue
        if not '.mk' in f: continue
        r.append(f.replace('.mk', ''))
    r.sort()
    for r1 in r: print r1
        
def new(what, title=None, force=False):
    """
    Create a new template based makefile in the current dir.
    """
    l.debug('creating a new moa makefile with title "%s"' % title)
    if os.path.exists("./Makefile"):
        l.debug("Makefile exists!")
        if not force:
            l.critical("makefile exists, use force to overwrite")
            sys.exit(1)

    for t in what:
        _check(t)
    
    #try to get a project name from the parent dir
    project = ""
    if os.path.exists("../moa.mk"):
        F = open('../moa.mk', 'r')
        for line in F.readlines():
            matchObject = re.match("^project *=(.*)$", line)
            if matchObject:
                project = matchObject.groups()[0]
        F.close()
        
    l.debug("Start writing ./Makefile") 
    F = open("./Makefile", 'w')
    F.write(NEW_MAKEFILE_HEADER)
    for t in what:
        F.write("include $(shell echo $$MOABASE)/template/%s.mk\n" % t)

    #now include moabase
    F.write("include $(shell echo $$MOABASE)/template/__moaBase.mk\n")
    F.close()

    if title and (title != '-'):

        with moa.utils.flock('moa.mk.lock'):    
            moamk = []

            #open & rewrite an older moa.mk
            if os.path.exists('moa.mk'):
                moamk = open('moa.mk').readlines()
                    
            F = open('moa.mk', 'w')
            projectSeen = False
            for line in moamk:
                if not re.match("^title *=", line):
                    F.write(line)
                if re.match("^project *=", line):
                    #if there is already a project line - 
                    #do not try to reset it.
                    projectSeen = True

            F.write("title=%s\n" % title)
            if project and not projectSeen:
                F.write("project=%s\n" % project)

            F.close()       
            l.debug('Written "title=%s" to moa.mk' % title)
    
    l.info("Written Makefile, try: make help")

