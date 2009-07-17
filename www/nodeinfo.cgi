#!/usr/bin/env python

import os
import sys
import cgi
#import cgitb; cgitb.enable()  # for troubleshooting
import simplejson
import subprocess 

MOAROOT = '/data/moa'

form = cgi.FieldStorage()
path = form.getvalue("path")


def runMake(path, *args):
    cl = "/opt/moa/bin/runMake %s %s" % (path, " ".join(args))
    return subprocess.Popen(
        cl, stdout=subprocess.PIPE,
        shell=True).communicate()[0]

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

#process targets
rv = runMake(path, 'targets')
data['targets'] = rv.split()

#process variables
rv = runMake(path, 'show')

for line in rv.split("\n"):
    line = line.strip()
    if not line: continue
    k,v = line.split(':', 1)
    data['vars'][k] = v

data['message'] = "Success loading data"
fire(data)
