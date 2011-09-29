#!/usr/bin/env python2.6

import os
import sys
import site
import shutil
import subprocess
import markdown

from jinja2 import Environment, FileSystemLoader

import cgi
import cgitb; cgitb.enable()  # for troubleshooting

if not os.environ.has_key('MOABASE'):
    raise Exception("MOABASE is undefined")

MOABASE = os.environ['MOABASE']
site.addsitedir(os.path.join(os.environ['MOABASE'], 'lib', 'python'))

#load moa libs & plugins
import moa.job
import moa.plugin
from moa.sysConf import sysConf

sysConf.initialize()


#initialize the jinja environment
jenv = Environment(
    loader=FileSystemLoader(
        os.path.join(MOABASE, 'www', 'jinja2')))

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

def getDescription(cwd):
    dfile = os.path.join(cwd, 'moa.description')
    if os.path.exists(dfile):
        try:
            shutil.move(
                dfile,
                os.path.join(cwd, 'Readme.md'))
        except:
            pass

def getBreadCrumbs():
    ## Prepare breadcrumbs
    dataRoot = getDataRoot()
    if moacwd.find(dataRoot) != 0:
        blocks = [{'name' : moacwd,
                   'class' : 'moaBreadCrumb',
                   'link' : requestUri,
                   'notlast' : True}]
    else:
        webRoot = getWebRoot()
        pathUntilNow = webRoot
        steps = moacwd[len(dataRoot)+1:].split('/')

        blocks = [{'name' : webRoot,
                   'class' : 'moaBreadCrumb',
                   'link' : webRoot,
                   'notLast' : True }]

        if len(steps) > 1:        
            for r in steps[:-1]:
                pathUntilNow += '/' + r
                blocks.append({'name' : r,
                               'class' : 'moaBreadCrumb',
                               'link' : pathUntilNow,
                               'notLast' : True })

        blocks[-1]['class'] += ' moaBreadCrumbActive'
        blocks[-1]['notLast'] = False
    return blocks


sysConf.MOABASE = MOABASE
moacwd = getLocalDir()
os.chdir(moacwd)
sysConf.www.webRoot = getWebRoot()
sysConf.www.dataRoot = getDataRoot()
sysConf.requestUri = os.environ.get('REQUEST_URI')
sysConf.moacwd = moacwd
sysConf.status = 'notmoa'
sysConf.dataRoot = getDataRoot()
sysConf.webRoot = getWebRoot()
sysConf.blocks  = getBreadCrumbs()

## displayable files:
possible_files = [
    'readme', 'changelog', 'report',
    'Readme', 'Changelog', 'Report',
    'README', 'CHANGELOG', 'REPORT'
    ]

#see if there is a description if so - move it to Readme.md (if we have the rights)
getDescription(moacwd)

sysConf.files = {}

all_files = os.listdir(moacwd)
for name in possible_files:
    for ext in ['', '.txt', '.md']:
        fname = name + ext
        if fname in all_files:
            with open(os.path.join(moacwd, fname)) as F:
                fdata = F.read()
            if ext == '.md':
                sysConf.files[name.capitalize()] = markdown.markdown(
                    fdata, extensions=['mdGraph', 'tables', 'footnotes'])
            else:
                sysConf.files[name.capitalize()] = '<pre>%s</pre>' % fdata
    
#instantiate job
job = moa.job.Job(moacwd)
sysConf.job = job


#make sure that some preparatory calls are executed
sysConf.pluginHandler.run('prepare_3')
sysConf.pluginHandler.run('preFiles')
sysConf.pluginHandler.run('prepareWWW')

if job.template.name == 'nojob':
    pageTemplate = jenv.get_template('notMoa.html')
    print pageTemplate.render(sysConf)
    sys.exit()
else:
    sysConf.status = 'moa'
    pageTemplate = jenv.get_template('Moa.html')
    print pageTemplate.render(sysConf)
