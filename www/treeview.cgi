#!/usr/bin/env python
#
#     Copyright 2009 Mark Fiers
#
#    This file is part of Moa 
#
#    Moa is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    Moa is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with Moa.  If not, see <http://www.gnu.org/licenses/>.
#
#    See: http://github.com/mfiers/Moa/

import os
import sys
import cgi
import cgitb; cgitb.enable()  # for troubleshooting
import simplejson

MOAROOT = os.environ.get('MOAROOT')

form = cgi.FieldStorage()
root = form.getvalue("root")

if not root or root == 'source':
    curdir = MOAROOT
else:
    curdir = os.path.join(MOAROOT, root)

#curdir = os.abspath(curdir)
    
subdirs = os.listdir(curdir)
subdirs.sort()

data = []
for x in subdirs:
    subdir = os.path.join(curdir, x)
    this = {'text' : x,
            'expanded': False,
            'id' : subdir}
    
    if os.path.isdir(subdir):
        this['hasChildren'] = True
        
    data.append(this)
        
print "Content-type: text/json"
print

print simplejson.dumps(data)
