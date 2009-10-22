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
import moa.couchdb
import moa.utils

l = moa.logger.l

def handler(options, args):
    """ 
    Handle conf related commands
    """
    moa.couchdb.connect(options)
    
    command = args[0]
    newargs = args[1:]

    if command == 'set':
        confChange('set', newargs)                  
    elif command == 'append':
        confChange('append', newargs)
    elif command == 'resolve':
        confResolve()
    else:
        exitError("Invalud moa conf invocation")


def confResolve():
    """
    Read the couchdb variables and store them in moa.mk
    """
    if not os.path.exists('moa.mk'):
        l.debug("moa.mk doesn't exist. nothing to cache")
        return

    l.debug("Start resolving moa.conf")
    with moa.utils.flock('moa.mk.lock'):
        os.rename('moa.mk', 'moa.mk.tmp')        
        #open filehandles to both files:
        F = open('moa.mk.tmp', 'r')
        G = open('moa.mk', 'w')

        moaCouchKeys = set()
        moaCouchTerms = {}
        
        for line in F.readlines():
            line = line.strip()
            if not line: continue
            k,o,v = re.split(r'\s*(\+?=)\s*', line.strip())

            if k[-7:] == "__cache":
                l.debug("resolving %s %s %s" % (k, o, v))

                moaCouchKeys.add(k[:-7])
                moaCouchTerms[k[:-7]] = v

        F.seek(0)
        for line in F.readlines():
            line = line.strip()
            if not line: continue
            k,o,v = re.split(r'\s*(\+?=)\s*', line.strip())
            if not k in moaCouchKeys:
                G.write("%s%s%s\n" % (k,o,v))
                
        for k in moaCouchKeys:
            v = moaCouchTerms[k]

            matchobj = re.search(r'%([0-9A-Za-z]{4})/([A-Za-z0-9_]*?)%', v)
            if matchobj:
                docid = matchobj.groups()[0]
                dockey = matchobj.groups()[1]
            else:
                matchobj = re.match("%([0-9A-Za-z]{4})%", v)
                docid = matchobj.groups()[0]
                dockey = 'pwd'

            replaceVal = moa.couchdb.getValueFromDb(docid, dockey)
            val = v.replace("%%%s/%s%%" % (docid, dockey), replaceVal)
            G.write("%s=%s\n" % (k,val))
            
        F.close()
        G.close()
        os.remove('moa.mk.tmp')
  
   
def confChange(mode, args):
    """
    save the arguments in moa.mk
    """   
    #parse all arguments..
    incomingKeys = set()
    defaultAttribs = {}
    incomingArgs = []
    for a in args:
        k, v = [x.strip() for x in a.split('=', 1)]
        if "_default_attrib" in k:
            defaultAttribs[k[:-15]]=v
        else:
            incomingKeys.add(k)
            incomingArgs.append((k,v))

    #set a lock on moa.mk
    with moa.utils.flock('moa.mk.lock'):
        #move moa.mk to a new location
        if os.path.exists('moa.mk'):
            os.rename('moa.mk', 'moa.mk.tmp')
        else:
            open('moa.mk.tmp', 'w').close()
            
        
        #open filehandles to both files:
        G = open('moa.mk', 'w')
        F = open('moa.mk.tmp', 'r')

        #read the old file
        for line in F.readlines():
            #l.debug("trying line %s" % line)
            k,o,v = re.split(r'\s*(\+?=)\s*', line.strip())
            if mode != 'set':
                #if the mode is not 'set', write 
                G.write(line)                
            elif (not k in incomingKeys) and \
                 (not k.replace("__cache", "") in incomingKeys):
                #write
                G.write(line)
                
        if mode == 'set':
            oper = "="
        else:
            oper = "+="
            
        for k,v in incomingArgs:
            matchObj = re.search("%([0-9A-Za-z]{4})%", v)
            if matchObj and (k in defaultAttribs.keys()):
                docId = matchObj.groups()[0]                
                newRef = '%%%s/%s%%' % (docId, defaultAttribs[k])
                newval = v.replace('%%%s%%' % docId, newRef)
                G.write("%s__cache%s%s\n" % (k, oper, newval))
                l.debug("writing (d): %s__cache%s%s to moa.mk" % (k, oper, newval))
            elif matchObj:
                G.write("%s__cache%s%s\n" % (k, oper, v))
                l.debug("writing: %s__cache%s%s to moa.mk" % (k, oper, v))
            elif re.match("%[0-9A-Za-z]{4}/[A-Za-z0-9_]*%", v):
                G.write("%s__cache%s%s\n" % (k, oper, v))
                l.debug("writing: %s__cache%s%s to moa.mk" % (k, oper, v))
            else:
                G.write("%s%s%s\n" % (k, oper, v))
                l.debug("writing: %s%s%s to moa.mk" % (k, oper, v))
        F.close()
        G.close()
        os.remove('moa.mk.tmp')
    confResolve()
    
