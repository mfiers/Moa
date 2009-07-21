#!/usr/bin/env python

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
