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

import moa.utils.logger
l = moa.utils.logger.l
    
MOABASE = os.environ["MOABASE"]
TEMPLATEDIR = os.path.join(MOABASE, 'template')

def roostError(message):
    

    if message:
        l.error(message)
    else:
        l.error('Invalid invocation of "moa roost"')

    sys.exit(-1)
    
def handler(options, args):
    l.debug("roost handler with args %s" % args)

    if len(args) == 0:
        roostError()
        
    command = args[0]
    
    if command == 'create':
        create(options, args[1:])
    elif command == 'open':
        open(options, args[1:])


def create(options, args):
    
    if len(args) != 1:
        roostError("Usage: moa roost create [NAME]") 
    name = args[0]
    
    l.debug("Create a roost")

    roostfile = name + ".roost"
    
    if os.path.exists(roostfile):
        if options.force:
            os.remove(roostfile)
        else:
            roostError("%s exists. Use -f to override" % roostfile)
    
    os.system('find . -type d  -o -name "moa.mk" -o  -name "Makefile" > moa.files')
    os.system('tar czf %s.roost -T moa.files --no-recursion' % name)
    os.system('rm moa.files')

def open(options, args):
    
    if len(args) == 0:
        roostError("You should specify a roost to open")

    roostfile = args[0]
    if len(args) > 1:
        target = args[1]
    else:
        target = '.'

    #first find the roostfile
    if not os.path.exists(roostfile):
        #see if it needs an extension
        if not '.roost' == roostfile[-6:]:
            roostfile += '.roost'
    if not os.path.exists(roostfile):        
        #try the roost dir in moabase
        roostfile = os.path.join(MOABASE, roostfile)
    if not os.path.exists(roostfile):
        roostError("Cannot find your roost")

    l.debug("discovered roostfile at %s" % roostfile)

    if (not target == '.') and (not os.path.exists(target)):
        os.mkdir(target)

    if not options.force:
        indir = os.listdir(target)
        if os.path.basename(roostfile) in indir:
            indir.remove( os.path.basename(roostfile))
        if len( indir) > 0:
            roostError("Target dir is not empty, use -f to force")

    
    print roostfile
    print target
            
            
    

    
        
        
