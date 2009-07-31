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
#import cgitb; cgitb.enable()  # for troubleshooting
import simplejson
import subprocess 

MOAROOT = '/data/moa'

form = cgi.FieldStorage()
path = os.path.abspath(form.getvalue("path"))
runmakepath = os.path.join(
    os.environ["MOABASE"], 'bin', 'runMake')

def runMake(path, *args):
    cl = "%s %s %s" % (
        runmakepath, path, " ".join(args))
    return subprocess.Popen(
        cl, stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        shell=True).communicate()

def fire(data):
    print "Content-type: text/json"
    print
    print simplejson.dumps(data)
    sys.exit()

#get node help - just for starters
#see if this is a moa dir
if not os.path.exists(os.path.join(path, 'Makefile')):
    fire({'message' : 'Not a moa dir (%s)' % path})

data = {}
data['vars'] = {}
data['targets'] = []
data['error'] = ""

#process targets
rv,err = runMake(path, 'targets')
data['targets'] = rv.split()
if err:
    data['error'] += err + "\n"

#process variables
rv, err = runMake(path, 'show')

for line in rv.split("\n"):
    line = line.strip()
    if not line: continue
    try:
        k,v = line.split(':', 1)
        data['vars'][k.strip()] = v.strip()
    except:
        data['error'] += "Invalid line:\n"
        data['error'] += "%s\n\n" % line
    

if err:
    data['error'] += rv + "\n"
data['message'] = "Success loading data"
fire(data)
