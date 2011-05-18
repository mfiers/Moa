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

#load moa libs
import moa.job
import moa.plugin
from moa.sysConf import sysConf
pluginHandler = moa.plugin.PluginHandler()
sysConf.pluginHandler = pluginHandler


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


d = {'MOABASE' : MOABASE}
moacwd = getLocalDir()
d['requestUri'] = os.environ.get('REQUEST_URI')
d['moacwd'] = moacwd
d['status'] = 'notmoa'
d['dataRoot'] = getDataRoot()
d['webRoot'] = getWebRoot()
d['blocks']  = getBreadCrumbs()

## displayable files:
possible_files = [
    'readme', 'changelog', 'report',
    'Readme', 'Changelog', 'Report',
    'README', 'CHANGELOG', 'REPORT'
    ]

#see if there is a description if so - move it to Readme.md (if we have the rights)
getDescription(moacwd)

d['files'] = {}

all_files = os.listdir(moacwd)
for name in possible_files:
    for ext in ['', '.txt', '.md']:
        fname = name + ext
        if fname in all_files:
            with open(os.path.join(moacwd, fname)) as F:
                fdata = F.read()
            if ext == '.md':
                d['files'][name.capitalize()] = markdown.markdown(fdata)
            else:
                d['files'][name.capitalize()] = '<pre>%s</pre>' % fdata

def prepFileList(fileList):
    ## perform some file magic
    dar = getDataRoot()
    wer = getWebRoot()
    rv = []
    for f in fileList:
        fup = os.path.abspath(f)
        if os.path.exists(fup):
            linkClass = 'moaFileExists'
        else:
            linkClass = 'moaFileAbsent'
            
        if fup.find(dar) == 0:
            fullurl = fup.replace(dar, wer)
            dirurl = os.path.dirname(fup).replace(dar,wer)
            link = '<a class="%s" href="%s#fileBrowser">%s</a>' % (
                linkClass, dirurl, os.path.basename(f))
            if linkClass == 'moaFileExists':
                link += ' <span style="font-size: 60%%;">(<a href="%s">dl</a>)</span>' % (fullurl)
            rv.append(link)
        else:
            rv.append("%s %s" % (fup, dar))
            
    return rv
    
def prepFilesets(job):
    fss = job.data.filesets
    job.data.mappedSets = {}
    
    #first find the 'sets & singletons'
    for fsid in fss.keys():
        fs = fss[fsid]
        if fs.type == 'set':
            job.data.mappedSets[fsid] = {
                'type': 'group',
                'fs' : fs,
                'lifs': prepFileList(fs.files),
                'maps' : {}}
        elif fs.type == 'single':
            job.data.mappedSets[fsid] = {
                'type': 'single',
                'lifs': prepFileList(fs.files),
                'fs' : fs }

            
    #now find the maps that map to the other sets
    for fsid in fss.keys():
        fs = fss[fsid]
        if fs.type == 'map':
            source = fs.source
            fs['lifs'] = prepFileList(fs.files)
            job.data.mappedSets[source]['maps'][fsid] = fs

#Fire off a generic page without any information if this is not a Moa dir
job = moa.job.Job(moacwd)
sysConf.job = job

#make sure that some preparatory functions are executed
pluginHandler.run('prepare_3')
pluginHandler.run('preFiles')

#prepare Filesets for display by the template
prepFilesets(job)

sys.stderr.write("found a job? %s %s" % (job, job.template.name))
sys.stderr.write(str(job.conf.pretty()))
if job.template.name == 'nojob':
    pageTemplate = jenv.get_template('notMoa.html')
    print pageTemplate.render(**d)
    sys.exit()

#ok, this must be a moa directory: gather information
d['job'] = job
d['status'] = 'moa'
pageTemplate = jenv.get_template('Moa.html')
print pageTemplate.render(**d)
