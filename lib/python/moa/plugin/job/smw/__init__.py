# Copyright 2009-2011 Mark Fiers
# The New Zealand Institute for Plant & Food Research
# 
# This file is part of Moa - http://github.com/mfiers/Moa
# 
# Licensed under the GPL license (see 'COPYING')
# 
"""
**doc** - Manage job documentation
----------------------------------

Manage project / title / description for jobs

"""
import os
import sys
import random
import getpass
import socket
import datetime
import subprocess
import pkg_resources
import subprocess as sp

import jinja2

import mwclient
import mwclient.errors

import moa.ui
import moa.args
import moa.utils
import moa.logger as l
from moa.sysConf import sysConf

SITE = None
jenv = jinja2.Environment(loader=jinja2.PackageLoader('moa.plugin.job.smw'))
DEFAULT_PROJECT='No Project'

def _getRandomId(ln=5):
    RANDCHARS=list('0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ')
    return "".join([random.choice(RANDCHARS) for x in range(ln)])


def _getMwSite():
    global SITE
    if SITE != None:
        return SITE
    
    
    smwi = sysConf.plugins.job.smw
    SITE = mwclient.client.Site(host=smwi.host, path=smwi.path)
    SITE.login(username=smwi.user, password=smwi.password)    
    return SITE


def _savePage2(page, txt):
    try:
        l.debug("saving page to smw %s" % page)
        page.save(txt, 
                  summary='automatic save by the moa smw plugin',
                  minor=sysConf.plugins.job.smw.get('minor_saves', False))
        #moa.ui.message("saved change message to SMW")
    except mwclient.errors.LoginError:
        moa.ui.error("Invalid login for smw - cannot save change message")

def _savePage(page, txt):
    background = sysConf.plugins.job.smw.get('background', False)
    if background:
        try:
            fid = os.fork()
            if fid == 0:
                _savePage2(page, txt)
            else:
                del(page)
        except OSError:
            l.warning("Cannot fork for saving to SMW")
    else:
        _savePage2(page, txt)

@moa.args.forceable
@moa.args.command
def smw_prepare(job, args):
    """
    Prepare the smw instance
    """

    site = _getMwSite()
    
    for f in pkg_resources.resource_listdir(__name__, "templates/default"):
        if f[-4:] != '.smw':
            continue
        text = pkg_resources.resource_string(
            __name__, "templates/default/%s" % f)

        pagename = f[:-4]
        page = site.Pages[pagename]
        if page.exists and not sysConf.args.force:
            moa.ui.warn("'%s' exists - use -f to overwrite" % pagename)
            continue
        #moa.ui.message("saving %s" % pagename)

        try:
            page.save(text, summary='automatic save by the moa smw plugin')
        except mwclient.errors.LoginError:
            moa.ui.exitError("Invalid login for smw - cannot run smw_prepare")

@moa.args.forceable
@moa.args.needsJob
@moa.args.command
def smw_save_job(job, args):
    """
    save a job page to SMW
    """
    _saveJobToSmw(job)
    


def hook_prepare_3(job):
    """
    """
    job.template.parameters.smwjobid = {
        'optional' : True,
        'help' : 'The random id used for this job in smw',
        'recursive' : False,
        'type' : 'string',
        'private': True
        }
    job = sysConf['job']


def hook_finish(job):
    """
    """
    if not job.isMoa():
        #only save is this directory continas a moa job
        return

    pid = os.fork()
    if pid != 0:
        #parent process - return now
        return 

    message = moa.ui._textFormattedMessage(
        [sysConf.args.changeMessage,
         sysConf.doc.changeMessage] )
        
    if sysConf.commands[sysConf.args.command]['logJob']:
        if sysConf.args.command != 'smw_save_job':
            _saveJobToSmw(job)
        _saveChangeMessage(job, message)
    sys.exit(0)

def _checkJobInSmw(job):
    if not job.conf.get('smwjobid'):
        return False

    project = job.conf.get('project', DEFAULT_PROJECT)
    jobid = job.conf.get('smwjobid', _getRandomId())
    site = _getMwSite()
    pagename = 'moa/%s/job/%s' % (project, jobid)
    page = site.Pages[pagename]
    return page.exists

def _saveJobToSmw(job):
    """
    gather data & save the job to SMW

    note - this is done in the background - hence - the 
    function forks & the master returns directly
    """

    templateName = job.template.name

    project = job.conf.get('project', 'No Project')
    jobid = job.conf.smwjobid
    doesNotExists = False

    if not jobid:
        jobid = _getRandomId()
        doesNotExists = True

    if templateName == 'project':
        pagename = 'moa/%s' % (project)
    else:
        pagename = 'moa/%s/job/%s' % (project, jobid)

    site = _getMwSite()
    page = site.Pages[pagename]

    if doesNotExists:        
        while True:
            if not page.exists:
                break
            jobid = _getRandomId()
            pagename = 'moa/%s/job/%s' % (project, jobid)
            page = site.Pages[pagename]

    sysConf.smw.project = project
    sysConf.smw.jobid = jobid
    sysConf.smw.host = socket.gethostname()

    job.conf.smwjobid = jobid
    job.conf.save()

    #get the README from disk
    readmefile = os.path.join(job.wd, 'README.md')
    if os.path.exists(readmefile):
        cl = 'pandoc %s --base-header-level 2 -f markdown -t mediawiki' % readmefile
        P = sp.Popen(cl.split(), stdout=sp.PIPE)
        o,e = P.communicate()    
        sysConf.smw.readme = o
    else:
        sysConf.smw.readme = ""

    jtemplate = jenv.select_template(
        ["job/%s.jinja2" % templateName,
        "job/default.jinja2"])
    
    txt = jtemplate.render(sysConf)
    _savePage(page, txt)
    
def _saveChangeMessage(job, message):

    project = job.conf.get('project', DEFAULT_PROJECT)

    simplemessage = message[0].strip()
    if len(simplemessage) > 50: 
        simplemessage = simplemessage[:47] + '...'

    sysConf.smw.message = "\n".join(message)
    sysConf.smw.simplemessage = simplemessage
    sysConf.smw.commandline = " ".join(sys.argv)
    site = _getMwSite()
    project = job.conf.get('project', 'No Project')
    jobid = job.conf.get('smwjobid')
    sysConf.smw.project = project
    sysConf.smw.jobid = jobid
    while True:
        if job.template.name == 'project':
            changename = '%s/change/%s' % (project, _getRandomId())
        else:
            changename = '%s/job/%s/change/%s' % (project, jobid, _getRandomId())
        page = site.Pages[changename]
        if not page.exists:
            break

    if job.template.name == 'project':
        smwjobid = 'moa/%s' % (project)
    else:
        smwjobid = 'moa/%s/job/%s' % (project, jobid)
        
    sysConf.smw.smwjobid = smwjobid

    jtemplate = jenv.select_template(["changemessage.jinja2"])
    txt = jtemplate.render(sysConf)
    _savePage(page, txt)


def _saveBlogToSmw(job):

    project = job.conf.get('project', DEFAULT_PROJECT)
    blog = sysConf.doc.blog

    if not "\n".join(blog).strip():
        #empty message - return
        return

    message = "\n".join(blog)
    teaser = " ".join(message.split())
    if len(teaser) > 50: 
        teaser = teaser[:47] + '...'
    sysConf.smw.teaser = teaser

    cl = 'pandoc --base-header-level 2 -f markdown -t mediawiki' 
    P = sp.Popen(cl.split(), stdout=sp.PIPE, stdin=sp.PIPE)
    o,e = P.communicate(message)
    sysConf.smw.message = o

    site = _getMwSite()
    project = job.conf.get('project', 'No Project')
    jobid = job.conf.get('smwjobid')
    sysConf.smw.project = project
    sysConf.smw.jobid = jobid
    while True:
        blogname = '%s/job/%s/blog/%s' % (project, jobid, _getRandomId())
        page = site.Pages[blogname]
        if not page.exists:
            break

    if job.template.name == 'project':
        smwjobid = 'moa/%s' % (project)
    else:
        smwjobid = 'moa/%s/job/%s' % (project, jobid)
        
    sysConf.smw.smwjobid = smwjobid

    jtemplate = jenv.select_template(["blogmessage.jinja2"])
    txt = jtemplate.render(sysConf)
    _savePage(page, txt)

def hook_postReadme(job):
    if not job.isMoa():
        #only save is this directory continas a moa job
        return
    _saveJobToSmw(job)

def hook_postBlog(job):
    if not job.isMoa():
        #only save is this directory continas a moa job
        return

    _saveBlogToSmw(job)

