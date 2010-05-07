#!/usr/bin/env python2.6

import os
import sys
import cgi
import site
import json

if not os.environ.has_key('MOABASE'):
    raise Exception("MOABASE is undefined")

MOABASE = os.environ['MOABASE']

site.addsitedir(os.path.join(os.environ['MOABASE'], 'lib', 'python'))

import moa.info
import moa.conf
import moa.lock
from moa.exceptions import *

def moaLock(form, data):
    wd = form['wd'].value
    moa.lock.lockJob(wd)
    return 'Successfully locked this job'

def moaUnlock(form, data):
    wd = form['wd'].value
    moa.lock.unlockJob(wd)
    return 'Successfully unlocked this job'
    
def moaSet(form, data):
    wd = form['wd'].value
    k = form['key'].value
    v = form['val'].value
    moa.conf.setVar(wd, k, v)
    return 'Successfully set %s to: %s' % (k,v)

def moaRun(form, data):
    wd = form['wd'].value
    template = form.get('target', "")
    job = moa.job.MOAMAKE(
        wd = wd, bg = True, target = target)
    return "Started job %s in %s" % (target, wd)
    
if __name__ == "__main__":

    form = cgi.FieldStorage()
    req = os.environ['PATH_INFO'][1:]
    wd = form['wd']
    
    data = { 'success': False,
             'req' : req }
    
    try:
        func = 'moa%s' % req.capitalize()
        try:
            data['message'] = eval('%s(form, data)' % func)
            data['success'] = True
        except NameError:
            data['message'] = "unknown method: %s - %s" % (req, func)
        except Exception as e:
            data['message'] = "error executing! (%s)"  % e
    except MoaPermissionDenied:
        data['message'] = 'Permission denied'

    print "Content-type: application/json"
    print
    print json.dumps(data)

