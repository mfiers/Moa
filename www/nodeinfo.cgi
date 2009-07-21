#!/usr/bin/env python

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
