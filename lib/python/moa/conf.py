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


def cache():
    """
    Read the coucdb variables and store them in moa.mk
    """
    if not os.path.exists('moa.mk'):
        l.debug("moa.mk doesn't exist. nothing to cache")
        return

    with flock('moa.mk.lock'):
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
            if k[-9:] == "__couchdb":
                moaCouchKeys.add(k[:-9])
                moaCouchTerms[k[:-9]] = v


        F.seek(0)
        for line in F.readlines():
            line = line.strip()
            if not line: continue
            k,o,v = re.split(r'\s*(\+?=)\s*', line.strip())
            if not k in moaCouchKeys:
                G.write("%s%s%s\n" % (k,o,v))
                
        for k in moaCouchKeys:
            cdbk, cdbv = moaCouchTerms[k].split()
            val = moaGet(cdbk, cdbv)
            G.write("%s=%s\n" % (k,val))
            
        F.close()
        G.close()
        os.remove('moa.mk.tmp')
   
   
def change(mode, args):
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

    with flock('moa.mk.lock'):
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
                 (not k.replace("__couchdb", "") in incomingKeys):
                #write, unless the mode=='set' and the key needs
                #an update
                G.write(line)
            else:
                l.debug("Omitting line - needs replacement:")
                l.debug(" : %s " % line.strip())
                
        if mode == 'set':
            oper = "="
        else:
            oper = "+="
            
        for k,v in incomingArgs:
            l.debug("writing new line to moa.mk:")
            l.debug(" : %s%s%s" % (k, oper, v))
            G.write("%s%s%s\n" % (k, oper, v))

        F.close()
        G.close()
        os.remove('moa.mk.tmp')
    moaConfCache()
    
