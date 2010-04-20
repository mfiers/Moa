#!/usr/local/bin/python2.6

import os
import sys
import site

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

def linkify(cwd):
    """
    Create a html path with links to the respective directories

    """
    dataRoot = getDataRoot()
    webRoot = getWebRoot()

    if cwd.find(dataRoot) != 0:
        return cwd

    ls = []
    ls.append("<div class='moaBreadCrumb'><a href='%s'>%s</a></div>" % (webRoot, dataRoot))
    
    pathUntilNow = webRoot
    steps =  cwd[len(dataRoot)+1:].split('/')
    if len(steps) > 2:
        for r in steps[:-2]:
            pathUntilNow += '/' + r
            ls.append("<div class='moaBreadCrumb'><a href='%s'>%s</a></div>" % (pathUntilNow, r))
    if len(steps) > 1:
        ls.append("<div class='moaActiveBreadCrumb'>%s</div>" % steps[-2])
    return "".join(ls)

print "Content-type: text/html"
print

moacwd = getLocalDir()
linkcwd = linkify(moacwd)

HEADERTEMPLATE = \
"""
<html>
  <head><title>Index of %(moacwd)s</title></head>
  <link rel=stylesheet href="/moa/moa.css" type="text/css" media=screen>
  <body>
    <div class='moaHeader'>
      <div class='moaLogo'>
        <img src='/moa/images/moa_logo_smaller.png'>
      </div>
	  <div class='moaBreadCrumbs'>
          %(linkcwd)s
	  </div>
      <div class='moaInfo'>
        %(moaInfo)s
      </div>
      <div style='clear: both;'></div>
    </div>
"""

if not moa.info.isMoaDir(moacwd):
    moaInfo = """
    <b>This directory does not contain a Moa job</b>
	""" % locals()
    print HEADERTEMPLATE % locals()
    sys.exit()

status = moa.info.status(moacwd)
template = moa.info.template(moacwd)
jobTitle = moa.info.getTitle(moacwd)

moaInfo = """
  <table>
    <tr><td colspan='2'><b>%(jobTitle)s</b></td> </tr>
    <tr><td colspan='2'>template: %(template)s, status: %(status)s</td> </tr>
  </table>
""" % locals()
 
print HEADERTEMPLATE % locals()

