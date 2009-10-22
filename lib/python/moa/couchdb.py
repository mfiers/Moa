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
Moa script - couchdb related code
"""

import re
import sys
import httplib
import simplejson
import pprint

import moa.logger
from moa.logger import exitError
l = moa.logger.l

VIEWS = {
  'language' : 'javascript',
  'views' : {
        'projects' : 
        { 'map' : "function(doc) { emit(null, doc.project); }",
          'reduce' : 
          """ function(keys, values, rereduce) {
                rv = [];
                for ( var i in values ) {
                  if (rv.indexOf(values[i]) == -1) {
                    rv.push(values[i]);
                  }
                } 
                return rv;
              } """
          },
        'owners' : 
        { 'map' : "function(doc) { emit(null, doc.owner); }",
          'reduce' : 
          """ function(keys, values, rereduce) {
                rv = [];
                for ( var i in values ) {
                  if (rv.indexOf(values[i]) == -1) {
                    rv.push(values[i]);
                  }
                } 
                return rv;
              } """
          },
        'jids' : 
        { 'map' : "function(doc) { emit(null, doc._id); }",
          'reduce' : 
          """ function(keys, values, rereduce) {
                rv = [];
                for ( var i in values ) {
                  if (rv.indexOf(values[i]) == -1) {
                    rv.push(values[i]);
                  }
                } 
                return rv;
              } """
          },
        }
  }

def JSONError(doc):
    """
    Dump a JSON error to screen
    """
    l.error(simplejson.dumps(doc, sort_keys=True, indent=4))
    sys.exit(-1)
  
class Couchdb:    
    """ 
    Wrapper class for operations on a couchDB. This code is gracefully
    adapted from http://wiki.apache.org/couchdb/Getting_started_with_Python
    """

    def __init__(self,
                 host='localhost', 
                 port=5984,
                 db='moa'):
        
        self.host = host
        self.port = port
        self.db = db

    def connect(self):
        """
        Connect - (ell, create an httpconnection object)
        """
        # No close()???
        return httplib.HTTPConnection(self.host, self.port)


    # high level operations
    def createDb(self):
        """ Creates a new database on the server
        """
        l.debug("Creating db %s" % self.db)
        r = self.put("/%s/" % self.db, '')

        if r.has_key('error'):
            if r['error'] == 'file_exists':
                l.warning("Database already exists, ignoring/..")
                return r
            else:
                JSONError(r)

        self.addDefaultViews()
        return r
   
    def addDefaultViews(self):
        """
        adds the default views to a fresh database
        """
        global VIEWS
        l.debug("registering the default views")
        self.saveDoc(VIEWS, "_design/moa")


    def addview(self, name, mapfunc, reducefunc=None, force=False):
        """
        Adds a view to the default _design/moa document
        """
        l.debug("Adding a new view")
        views = self.openDoc('_design/moa')
        if not views.has_key('language'):
            views['language'] = 'javascript'
        if not views.has_key('views'):
            views['views'] = {}
        l.debug("views present %s" % views['views'].keys())
        if not force and (views['views'].has_key(name)):
            l.debug("view '%s' is present" % name)
            return True

        #set the new/updated view
        views['views'][name] = {
            'map': " ".join(mapfunc.split())}
        if reducefunc:
            views['views'][name]['reduce'] = \
                " ".join(reducefunc.split())
        self.saveDoc(views, '_design/moa')
        l.debug("saved new view")

    def deleteDb(self):
        """Deletes the database on the server"""
        r = self.delete('/%s/' % self.db)
        return r

    def listDb(self):
        """List the databases on the server"""
        return self.get('/_all_dbs')

    def infoDb(self):
        """Returns info about the couchDB"""
        return self.get('/%s/' % self.db)

    def allDocs(self):
        """ returns all docs in a db """
        return self.get("/%s/_all_docs" % self.db)
        
    # Document operations
    def listDoc(self):
        """List all documents in a given database"""
        return self.get('%s/_all_docs' % self.db)

    def openDoc(self, docId):
        """Open a document in a given database"""
        return self.get('/%s/%s' % (self.db, docId))

    def openView(self, view):
        """Open a view"""
        #http://localhost:5984/moa/_design/moa/_view/projects
        return self.get('/%s/_design/moa/_view/%s' % (
                self.db, view))

    def forceSave(self, body, docId):
        """
        Force a save, if a regular save doesn't work.

        A save can fail if it should have been an update. This
        function loads the old document and gets the revision ID.
        
        This is dangerous!! Shouldn't use it :P
        """
        #try a regular save:
        r = self.saveDoc(self.db, body, docId)
        if r.get('error', None) == 'conflict':
            l.debug("inital error saving")
            if not body.has_key("_rev"):
                l.warning("save conflict - older revision and retrying")
                olddoc = self.openDoc(self.db, docId)
                body['_rev'] = olddoc['_rev']
                r = self.saveDoc(self.db, body, docId)
        return r
            
    def saveDoc(self, body, docId=None):
        """Save/create a document to/in a given database"""
        if not docId:
            return self.post("/%s/" % (self.db), body)

        return self.put("/%s/%s" % (self.db, docId), body)


    def deleteDoc(self, doc):
        """
        Delete a document from the server
        """
        return self.delete('/%s/%s?rev=%s' % (
            self.db, doc["_id"], doc["_rev"]))

    #low level routines, calling get, post, put & delete
    def get(self, uri):
        """ Get an uri from couchdb and parse it with simpljson """
        c = self.connect()
        headers = {"Accept": "application/json"}
        c.request("GET", uri, None, headers)
        return simplejson.loads(c.getresponse().read())

    def post(self, uri, body):
        """ Post an uri to couchdb, convert the body using simplejson
        """
        c = self.connect()
        headers = {"Content-type": "application/json"}
        c.request('POST', uri,
                  simplejson.dumps(body),
                  headers)
        return simplejson.loads(c.getresponse().read())

    def put(self, uri, body):
        """ As post - using PUT """
        body = simplejson.dumps(body)
        c = self.connect()
        if len(body) > 0:
            headers = {"Content-type": "application/json"}
            c.request("PUT", uri, body, headers)
        else:
            c.request("PUT", uri, body)
        return simplejson.loads(c.getresponse().read())

    def delete(self, uri):
        """ Delete request to the db """
        c = self.connect()
        c.request("DELETE", uri)
        return simplejson.loads(c.getresponse().read())

couchdb = None

def connect(options):
    """ 
    Connect to the couchdb server
    """
    global couchdb
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


def handler(options, args):
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
    allJids = _jids()
    args = [re.sub("[^0-9A-Za-z_]", "", x) for x in args]
    allargs = " ".join(args).split()
    ccargs = "".join(allargs)
    shargs = re.sub("[aeouiAEOUI]", "", ccargs)
    #aim at a 5 letter jid

    if (len(shargs) >= 5) and (not shargs[:5] in allJids):
        print shargs[:5]
        return
    if (len(ccargs) >= 2225) and (not ccargs[:5] in allJids):
        print ccargs[:5]
        return
        


#def initdb(options, args):
def _projects():
    """
    Return a list of all projects
    """
    data = couchdb.openView('projects')
    return data['rows'][0]['value']

def _jids():
    """
    Return a list of jids
    """
    data = couchdb.openView('jids')
    return data['rows'][0]['value']

def projects():
    """
    Get a list of all projects
    """
    print "\n".join(_projects())

def owners():
    """
    Get a list of all projects
    """
    data = couchdb.openView('owners')
    print "\n".join(data['rows'][0]['value'])


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
    docid, query = args
    doc = couchdb.openDoc(docid)
    if not doc:
        l.error("Cannot find document /moa/%s" % docid)
        sys.exit(-1)
    if not doc.has_key(query):
        l.error("Cannot find document /moa/%s/%s" % (docid, query))
        sys.exit(-1)
    print doc[query]


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


    

