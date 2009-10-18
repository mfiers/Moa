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

import httplib
import simplejson

import moa.logger
l = moa.logger.l

class Couchdb:
    
    """ Wrapper class for operations on a couchDB. This code is gracefully
    adapted from ?
    """

    def __init__(self,
                 host='localhost', 
                 port=5984):
        
        self.host = host
        self.port = port

    def connect(self):
        # No close()???
        return httplib.HTTPConnection(self.host, self.port)


    # high level operations
    def createDb(self, dbName):
        
        """ Creates a new database on the server"""

        l.debug("Creating db %s" % dbName)
        r = self.put("/%s/" % dbName, '')
        if r.has_key('error'):
            if r['error'] == 'file_exists':
                l.warning("Database already exists, ignoring/..")
                return r
            else:
                error(r)
        return r
        
    def deleteDb(self, dbName):
        """Deletes the database on the server"""
        r = self.delete('/%s/' % dbName)
        return r

    def listDb(self):
        """List the databases on the server"""
        return self.get('/_all_dbs')

    def infoDb(self, dbName):
        """Returns info about the couchDB"""
        return self.get('/%s/' % dbName)

    def allDocs(self, dbName):
        """ returns all docs in a db """
        return self.get("/%s/_all_docs" % dbName)
        
    # Document operations
    def listDoc(self, dbName):
        """List all documents in a given database"""
        return self.get('%s/_all_docs' % dbName)

    def openDoc(self, dbName, docId):
        """Open a document in a given database"""
        return self.get('/%s/%s' % (dbName,docId))

    def forceSave(self, dbName, body, docId):
        #try a regular save:
        r = self.saveDoc(dbName, body, docId)
        if r.get('error', None) == 'conflict':
            if not body.has_key("_rev"):
                l.warning("save conflict - older revision and retrying")
                olddoc = self.openDoc(dbName, docId)
                body['_rev'] = olddoc['_rev']
                r = self.saveDoc(dbName, body, docId)
        return r
            
    def saveDoc(self, dbName, body, docId=None):
        """Save/create a document to/in a given database"""
        if not docId:
            return self.post("/%s/" % (dbName), body)

        return self.put("/%s/%s" % (dbName, docId), body)


    def deleteDoc(self, dbName, doc):
        return self.delete('/%s/%s?rev=%s' % (
            dbName, doc["_id"], doc["_rev"]))

    #low level routines, calling get, post, put & delete
    def get(self, uri):
        c = self.connect()
        headers = {"Accept": "application/json"}
        c.request("GET", uri, None, headers)
        return simplejson.loads(c.getresponse().read())

    def post(self, uri, body):
        c = self.connect()
        headers = {"Content-type": "application/json"}
        c.request('POST', uri,
                  simplejson.dumps(body),
                  headers)
        return simplejson.loads(c.getresponse().read())

    def put(self, uri, body):
        body = simplejson.dumps(body)
        c = self.connect()
        if len(body) > 0:
            headers = {"Content-type": "application/json"}
            c.request("PUT", uri, body, headers)
        else:
            c.request("PUT", uri, body)
        return simplejson.loads(c.getresponse().read())

    def delete(self, uri):
        c = self.connect()
        c.request("DELETE", uri)
        return simplejson.loads(c.getresponse().read())

# Handle couchdb related commands
def moaRegister(args):
    
    global _dbName
    global _server

    docid = args[0]
    newdoc = {}

    #see if there was already a doc with this name:
    doc = _server.openDoc(_dbName, docid)
    if doc.has_key('error'):
        l.debug("No previous record found (%s)" % doc['error'])
    else:
        #remember the _rev(ision) id.. for an update
        if doc: newdoc['_rev'] = doc['_rev']

    for x in args[1:]:
        l.debug("registring %s" % x)
        k,v = x.split('=', 1)
        #process the moa_ids - make it a list
        if k == 'moa_ids': newdoc[k] = v.split()
        else: newdoc[k] = v

    l.debug("New doc created (with %d keys)" % len(newdoc))
    r = _server.saveDoc(_dbName, newdoc, docid)
    if r.has_key('error') and r['error'] == 'not_found':
        #maybe the db isn't created -yet- try that
        l.warning("Db is not created? Trying..")
        _server.createDb(_dbName)
        r = _server.saveDoc(_dbName, newdoc, docid)
        if r.has_key('error'):
            l.error("Error writing document")
            error(r)
    elif r.has_key('error'):
        l.error("Error writing document")
        error(r)
    else:
        l.info("Success, document is written to the db")
        return True
    return True

def moaGet(docid, query):
    """ Get a single value from a record """
    global _server
    global _dbName
    doc = _server.openDoc(_dbName, docid)
    if not doc:
        l.error("Cannot find document /moa/%s" % docid)
        sys.exit(-1)
    if not doc.has_key(query):
        l.error("Cannot find document /moa/%s/%s" % (docid, query))
        sys.exit(-1)
            
    return doc[query]

def getJids():
    """ Get a list of jids """
    return [d['id'] for d in _server.allDocs(_dbName)['rows']]

def getDocStr(id):
    doc = _server.openDoc(_dbName, id)
    return simplejson.dumps(doc, sort_keys=True, indent=4)


_server = None
_serverName = None
_serverPort = None
_dbName = None

def connect(s, p, d):
    """connect to a couchdb server"""
    global _serverName
    global _serverPort
    global _server
    global _dbName
    _serverName = s
    _serverPort = p
    _dbName = d
    _server = Couchdb(s, p)
