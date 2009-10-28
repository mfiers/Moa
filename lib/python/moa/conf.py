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
Moa script - moa.mk configuration related code
"""

import re
import os
import sys

import moa.logger
from moa.logger import exitError
import moa.utils

l = moa.logger.l

def handler(options, args):
    """ 
    Handle conf related commands
    """
    command = args[0]
    newargs = args[1:]

    if command == 'set':
        confChange('set', newargs)                  
    elif command == 'append':
        confChange('append', newargs)
    else:
        exitError("Invalud moa conf invocation")

def confChange(mode, args):
    """
    save the arguments in moa.mk
    """   
    #parse all arguments..
    incomingKeys = set()
    incomingArgs = []
    for a in args:
        k, v = [x.strip() for x in a.split('=', 1)]
        incomingKeys.add(k)
        incomingArgs.append((k,v))
    l.debug("Incoming keys : %s" % incomingKeys)

    #set a lock on moa.mk
    if os.path.exists('moa.mk.tmp'):
        l.debug("removing an older?? moa.mk.tmp")
        os.unlink('moa.mk.tmp')

    with moa.utils.flock('moa.mk.lock'):
        #move moa.mk to a new location
        if os.path.exists('moa.mk'):
            os.rename('moa.mk', 'moa.mk.tmp')
        else:
            #create an empty dummy file
            open('moa.mk.tmp', 'w').close()
        
        #open filehandles to both files:
        F = open('moa.mk.tmp', 'r')
        G = open('moa.mk', 'w')
        
        #parse through the old file
        for line in F.readlines():
            l.debug("trying line %s" % line)
            k,o,v = re.split(r'\s*(\+?=)\s*', line.strip())
            if mode == 'set' and k not in incomingKeys:
                G.write(line)                
            if mode != 'set':
                #if the mode is not 'set', write 
                G.write(line)                

        if mode == 'set':
            oper = "="
        else:
            oper = "+="
            
        for k,v in incomingArgs:
            if v:
                G.write("%s%s%s\n" % (k, oper, v))
                l.debug("writing: %s%s%s to moa.mk" % (k, oper, v))
            else:
                l.debug("removing key %s" % k)

        F.close()
        G.close()
        os.unlink('moa.mk.tmp')
    
