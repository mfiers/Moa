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

.PHONY: moa_preprocess
moa_preprocess:

.PHONY: moa_postprocess
moa_postprocess:

dont_include_moabase=true
"""


def handler(options, args):
    command = newargs[0]
    newargs = newargs[1:]
    if command == 'list':
        list()
    elif command == 'new':
        new(options, newargs)
    else:
        l.error("Usage moa template [new|list]")
        sys.exit()
        
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
        
def new(options, args):
    """
    Create a new template based makefile in the current dir.
    """

    usage = 'Usage: moa new  [-t "TITLE"] [TEMPLATE(s)]'

    if len(args) == 0:
        templates = ['traverse']
    else:
        templates = args

    title = options.title
    if not title and templates != ['traverse']:
        l.debug("no title? %s" % templates)
        l.warning("It is strongly recommended to specify a title")
        l.warning("You can still do so using moa set title='somthing meaningful'")
        title = ""

    if title:
        l.debug('creating a new moa makefile with title "%s"' % title)
    else:
        l.debug('creating a new moa makefile')

    if os.path.exists("./Makefile"):
        l.debug("Makefile exists!")
        if not options.force:
            l.critical("makefile exists, use -f (--force) to overwrite")
            sys.exit(1)

    for t in templates:
        _check(t)

    l.debug("Start writing ./Makefile") 
    F = open("./Makefile", 'w')
    F.write(NEW_MAKEFILE_HEADER)
    for t in templates:
        F.write("include $(shell echo $$MOABASE)/template/%s.mk\n" % t)

    #include moabase
    F.write("include $(shell echo $$MOABASE)/template/__moaBase.mk\n")
    F.close()

    if title:

        with moa.utils.flock('moa.mk.lock'):    
            moamk = []

            #open & rewrite an older moa.mk
            if os.path.exists('moa.mk'):
                moamk = open('moa.mk').readlines()
                    
            F = open('moa.mk', 'w')
            for line in moamk:
                if re.match("^title *=", line) and title:
                    continue
                F.write(line)
                
            if title:
                F.write("title=%s\n" % title)
                l.debug("writing title=%s to moa.mk" % title)

            F.close()       
            l.debug('Written moa.mk')
    
    l.info("Written Makefile, try: moa help")

