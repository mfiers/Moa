#!/usr/bin/env python2.6

import os
import sys
import site

from mako.template import Template
from mako.lookup import TemplateLookup

import cgi
import cgitb; cgitb.enable()  # for troubleshooting

if not os.environ.has_key('MOABASE'):
    raise Exception("MOABASE is undefined")

MOABASE = os.environ['MOABASE']
site.addsitedir(os.path.join(os.environ['MOABASE'], 'lib', 'python'))

import moa.info

def getWebRoot():
    webRoot = os.environ.get('MOAWEBROOT')
    if webRoot[-1] == '/':
        webRoot = webRoot[:-1]
    return webRoot

def getDataRoot():
    dataRoot = os.environ.get('MOADATAROOT')
    if dataRoot[-1] == '/':
        dataRoot = dataRoot[:-1]
    return dataRoot

def getLocalDir():
    requestUri = os.environ.get('REQUEST_URI')
    dataRoot = getDataRoot()
    webRoot = getWebRoot()

    if requestUri.find(webRoot) != 0:
        return False
    moadir = dataRoot + requestUri[len(webRoot):]
    if '?' in moadir:
        moadir = moadir[:moadir.index('?')]
    return moadir

d = {'MOABASE' : MOABASE}
moacwd = getLocalDir()
d['requestUri'] = os.environ.get('REQUEST_URI')
d['moacwd'] = moacwd
d['status'] = 'notmoa'
d['dataRoot'] = getDataRoot()
d['webRoot'] = getWebRoot()

templateLookup = TemplateLookup(
    directories=['/'],
    module_directory='/tmp/mako_modules' )

#Fire off a generic page without any information if this is not a Moa dir
if not moa.info.isMoaDir(moacwd):
    pageTemplate =  Template(filename='%s/www/template/notMoa.html' % MOABASE,
                             lookup=templateLookup)
    print pageTemplate.render(**d)
    sys.exit()

#ok, this must be a moa directory: gather information

d['status'] = moa.info.status(moacwd)
d['template'] = moa.info.template(moacwd)
d['jobTitle'] = moa.info.getTitle(moacwd)
d['allinfo'] = moa.info.info(moacwd)
d['description'] = d['allinfo'].get('moa_description', '')

pageTemplate =  Template(
    filename='%s/www/template/Moa.html'% MOABASE,
    lookup=templateLookup)
print pageTemplate.render(**d)


