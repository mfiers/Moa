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
Wrapper for db related routines
"""

import re
import sys
import random

from moa.db import couchdb
from moa.db import anydb

import moa.logger
from moa.logger import exitError
l = moa.logger.l

def connect(options):
    """ 
    Connect to the current db server
    """
    if ':' in options.couchserver:
        serverName, serverPort = \
            options.couchserver.split(':')
    else:
        serverName = options.couchserver
        serverPort = 5984

    l.debug("Connect couchdb %s %s %s" % 
            (serverName, serverPort, options.couchdb))

    #invoke the couch object
    couchdb = Couchdb(serverName, serverPort, options.couchdb)


def handler(conf, options, args):
    """
    Handler for all second level commands
    """
    connect(options)
    command = args[0]
    newargs = args[1:]

    if command == 'jids':
        printJids()
    elif command == 'register':
        register(options, newargs)
    elif command == 'get':
        get(options, newargs)
    elif command == 'doc':
        doc(options, newargs)
    elif command == 'generate_jid':
        generate_jid(options, newargs)
    elif command == 'projects':
        projects()
    elif command == 'owners':
        owners()
    else:
        exitError("Invalid invocation of: moa couchdb")


def generate_jid(options, args):
    """
    Generate a unique, short, jid
    """
    #aim at a 4 letter jid
    jidlen = 4
    allJids = _jids()

    args = [re.sub("[^0-9A-Za-z]", "", x) for x in args]
    allargs = " ".join(args).split()
    catargs = "".join(args)

    attempt = "".join([x[0] for x in allargs])[:jidlen]
    if (len(attempt) == jidlen) and (not attempt in allJids):
        print attempt
        return

    attempt = "".join([x[:2] for x in allargs])[:jidlen]
    if (len(attempt) == jidlen) and (not attempt in allJids):
        print attempt
        return

    attempt = catargs[:jidlen]
    if (len(attempt) == jidlen) and (not attempt in allJids):
        print attempt
        return

    attempt = re.sub("[aeouiAEOUI]", "", catargs)[:jidlen]
    if (len(attempt) == jidlen) and (not attempt in allJids):
        print attempt
        return

    letters = list(catargs)
    for x in range(0,10):
        attempt = "".join([random.choice(letters) for x in range(4)])
        if not attempt in allJids:
            print attempt
            return
        
    letters = list("abcdefghijklmnopqrstuvwxyz0123456789")
    while True:
        attempt = "".join([random.choice(letters) for x in range(4)])
        if not attempt in allJids:
            print attempt
            return


# Handle couchdb related commands
def register(options, args):
    """
    Register a moa node to the couchdb
    All variables are in the arguments
    """
    l.debug("Running moa couchdb register")
    if len(args) == 0:
        exitError("Invalid invocation of moa couchdb register")
    docid = args[0]
    newdoc = {}

    #see if there was already a doc with this name:
    doc = couchdb.openDoc(docid)
    if doc.has_key('error'):
        l.debug("No previous record found (%s)" % doc['error'])
    else:
        #remember the _rev(ision) id.. for an update
        if doc: 
            newdoc['_rev'] = doc['_rev']

    for x in args[1:]:
        l.debug("register %s" % x)
        k, v = x.split('=', 1)
        #process the moa_ids - make it a list
        if k == 'moa_ids': 
            newdoc[k] = v.split()
        else: newdoc[k] = v

    l.debug("New doc created (with %d keys)" % len(newdoc))
    r = couchdb.saveDoc(newdoc, docid)
    if r.has_key('error') and r['error'] == 'not_found':
        #maybe the db isn't created -yet- try that
        l.warning("Db is not created? Trying..")
        couchdb.createDb()
        r = couchdb.saveDoc(newdoc, docid)
        if r.has_key('error'):
            l.error("Error writing document")
            JSONError(r)
    elif r.has_key('error'):
        l.error("Error writing document")
        JSONError(r)
    else:
        l.info("Success, document is written to the db")
        return True
    return True


def get(options, args):
    """ Get a single value from a record """
    docid, key = args    
    print getValueFromDb(docid, key)

def getValueFromDb(docid, key):
    """Get a single value from the db"""
    l.debug("Getting %s from %s" % (key, docid))
    doc = couchdb.openDoc(docid)
    if not doc:
        exitError("Cannot find document /moa/%s" % docid)
    if not doc.has_key(key):
        exitError("Cannot find document /moa/%s/%s" % (docid, key))
    return doc[key]
    

## Get some stats & info from couchdb
def printJids():
    """print a list of jids to the screen"""
    print "\n".join(_jids())

def getJids():
    """ Get a list of jids """
    return [d['id'] for d in couchdb.allDocs()['rows'] if not d['id'][0]=='_']

def doc(options, args):
    """ Print a formatted document to screen """ 
    docId = args[0]
    doc = couchdb.openDoc(docId)
    for k in doc:
        v = doc[k]
        if type(v) in [type(()), type([])]:
            print "%s\t%s" % (k, " ".join(v))
        else:
            print "%s\t%s" % (k, v)


    

