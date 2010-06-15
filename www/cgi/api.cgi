#!/usr/bin/env python2.6

import os
import sys
import cgi
import site
import json

import bottle
from bottle import route, request

if not os.environ.has_key('MOABASE'):
    raise Exception("MOABASE is undefined")

MOABASE = os.environ['MOABASE']
site.addsitedir(os.path.join(os.environ['MOABASE'], 'lib', 'python'))

form = cgi.FieldStorage()
req = os.environ['PATH_INFO'][1:]
    
import moa.info
import moa.conf
import moa.lock
from moa.exceptions import *

def error(message, rv={}):
    rv['message'] = message
    rv['success'] = False
    return rv

def success(message, rv={}):
    rv['message'] = message
    rv['success'] = True
    return rv

def moaRun(form, data):
    wd = form['wd'].value
    template = form.get('target', "")
    job = moa.job.MOAMAKE(
        wd = wd, bg = True, target = target)
    return "Started job %s in %s" % (target, wd)

@route('/status')
def lock():
    wd = form['wd'].value
    rv = {'status' : moa.info.status(wd)}
    return success('Status is %s' % rv['status'], rv)

@route('/lock')
def lock():
    wd = form['wd'].value
    rv = {'wd' : wd }
    moa.lock.lockJob(wd)
    return success('Successfully locked this job', rv)

@route('/unlock')
def unlock():
    wd = request.GET['wd']
    moa.lock.unlockJob(wd)
    return success('Successfully unlocked this job')

@route('/set')
def moaSet():
    """ set a variable """
    rv = { 'success' : False }
    #return ("%s" % str(request.GET))
    wd = request.GET['wd']
    k = request.GET['key']
    v = request.GET['val']
    
    try:
        moa.conf.setVar(wd, k, v)
    except NotAMoaDirectory:
        return error('attempted to set a variable outside a Moa directory', rv)
    
    return success('Successfully set "%s" to "%s"' % (k,v), rv)
    
if __name__ == "__main__":

    bottle.run(server=bottle.CGIServer)
    

    # try:
    #     func = 'moa%s' % req.capitalize()
    #     try:
    #         data['message'] = eval('%s(form, data)' % func)
    #         data['success'] = True
    #     except NameError:
    #         data['message'] = "unknown method: %s - %s" % (req, func)
    #     except Exception as e:
    #         data['message'] = "error executing! (%s)"  % e
    # except MoaPermissionDenied:
    #     data['message'] = 'Permission denied'

    # print "Content-type: application/json"
    # print
    # print json.dumps(data)



    

