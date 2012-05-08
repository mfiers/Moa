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
import datetime
import subprocess
import pkg_resources

import jinja2
import mwclient

import moa.ui
import moa.args
import moa.utils
import moa.logger as l
from moa.sysConf import sysConf

SITE = None
                  
def _getProjectJobid():
    job = sysConf.job
    project = job.conf.project
    if not project:
        project = 'moa'        
    jobid = job.conf.jobid
    return project, jobid

def _getRandomId(ln=5):
    RANDCHARS=list('0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ')
    return "".join([random.choice(RANDCHARS) for x in range(ln)])


def _getMwSite():
    global SITE
    if SITE != None:
        return SITE

    smwi = sysConf.plugins.system.smw
    SITE = mwclient.client.Site(host=smwi.host, path=smwi.path)
    SITE.login(username=smwi.user, password=smwi.passwd)    
    return SITE

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
        page.save(text, summary='auto generation of a number of core smw/moa pages')
        print pagename
    pass

def hook_prepare_3():
    """
    """

    job = sysConf.job
    job.template.parameters.smwjobid = {
        'optional' : True,
        'help' : 'The random id used for this job in smw',
        'recursive' : False,
        'type' : 'string'
        }
    job = sysConf['job']
    message = sysConf.args.changeMessage
    if _checkJobInSmw():
        print 'saved!'
    else:
        saveJobToSmw(job)
    if message: 
        _saveChangeMessage(message)

def saveJobToSmw():

    job = sysConf.job
    
def _saveChangeMessage(message):
    
    sysConf.smw.message = message
    sysConf.smw.commandline = " ".join(sys.argv)
    site = _getMwSite()
    project, jobid = _getProjectJobid()
    sysConf.smw.project = project
    sysConf.smw.jobid = jobid
    while True:
        changename = '%s/%s/change/%s' % (project, jobid, _getRandomId())
        page = site.Pages[changename]
        if not page.exists:
            break

    template = pkg_resources.resource_string(__name__, "templates/changemessage.jinja2")
    jtemplate = jinja2.Template(template)
    txt = jtemplate.render(sysConf)
    page.save(txt)
    
    
    #try a random identifier
    


def hook_postReadme():
    print 'hi'
    print _getJobPageName()

#def p
# @moa.args.command
# def readme(job, args):
#     """
#     Edit the README.md file for this job

#     You could, obviously, also edit the file yourself - this is a mere
#     shortcut to try to stimulate you in maintaining one
#     """
    
#     subprocess.call([os.environ.get('EDITOR','nano'), 'README.md'])



# def _update_git(filename):
#     """
#     Check if a file is under version control & commit changes    
#     """
#     job = sysConf.job
#     if not sysConf.git.repo:
#         #repo is not initalized..(not in a repository?)
#         return
    
#     if os.path.exists(filename):    
#         sysConf.git.repo.index.add([filename])
#         sysConf.git.commitJob(job, 'Worked on %s in  %s' % (filename, job.wd))
        
    
# def hook_git_finish_readme():
#     """
#     Execute just after setting running moa readme
#     """
#     _update_git('README.md')

# def hook_git_finish_blog():
#     """
#     Execute just after setting running moa blog
#     """
#     _update_git('Blog.md')


# def hook_git_finish_change():
#     """
#     Execute just after setting running moa blog
#     """
#     _update_git('CHANGELOG.md')
