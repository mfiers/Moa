#!/usr/bin/env python2.6

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

    pathUntilNow = webRoot
    steps =  cwd[len(dataRoot)+1:].split('/')

    if len(steps) == 1:
        firstCrumbClass = 'moaBreadCrumb moaBreadCrumbActive'
    else:
        firstCrumbClass = 'moaBreadCrumb'

    ls.append("<div class='%s' onclick='window.location.replace(\"%s\");'>%s</div>" % (
        firstCrumbClass, webRoot, 'root'))
        
    
    if len(steps) > 2:
        for r in steps[:-2]:
            pathUntilNow += '/' + r
            onclick = 'window.location.replace("%s")' % pathUntilNow
            ls.append("<div class='moaBreadCrumb' onclick='%s'>%s</div>" % (onclick, r))
    if len(steps) > 1:
        ls.append("<div class='moaBreadCrumb moaBreadCrumbActive'>%s</div>" % steps[-2])
    return "".join(ls)

print "Content-type: text/html"
print

moacwd = getLocalDir()
linkcwd = linkify(moacwd)


HEADERTEMPLATE = open('headerTemplate.html').read()

if not moa.info.isMoaDir(moacwd):
    status = 'notmoa'
    moaInfo = """
    <b>This directory does not contain a Moa job</b>
	""" % locals()
    print HEADERTEMPLATE % locals()
    sys.exit()

status = moa.info.status(moacwd)
template = moa.info.template(moacwd)
jobTitle = moa.info.getTitle(moacwd)
allinfo = moa.info.info(moacwd)

moaInfo = """
<div class='moaTitleBar'>
 <div class='moaTemplate'>%(template)s</div>
 <div class='moaTitle'>
    %(jobTitle)s
  </div>
  <div class='moaStatus'>job is: %(status)s</div>
</div>
<pre>
%(allinfo)s
</pre>
""" % locals()
 
print HEADERTEMPLATE % locals()

