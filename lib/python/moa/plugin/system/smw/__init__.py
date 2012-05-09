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

import moa.ui
import moa.args
import moa.utils
import moa.logger as l
from moa.sysConf import sysConf

SITE = None
jenv = jinja2.Environment(loader=jinja2.PackageLoader('moa.plugin.system.smw'))

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

@moa.args.forceable
@moa.args.command
def smw_save_job(job, args):
    """
    save a job page to SMW
    """
    _saveJobToSmw(job)
    

def hook_prepare_3():
    """
    """
    job = sysConf.job
    job.template.parameters.smwjobid = {
        'optional' : True,
        'help' : 'The random id used for this job in smw',
        'recursive' : False,
        'type' : 'string',
        'private': True
        }
    job = sysConf['job']
    message = sysConf.args.changeMessage

    if message: 
        _saveJobToSmw(job)
        _saveChangeMessage(message)

def _checkJobInSmw(job):
    if not job.conf.get('smwjobid'):
        return False

    project = job.conf.get('project', 'No Project')
    jobid = job.conf.get('smwjobid', _getRandomId())
    site = _getMwSite()
    pagename = 'moa/%s/job/%s' % (project, jobid)
    page = site.Pages[pagename]
    return page.exists

def _saveJobToSmw(job):
    job = sysConf.job
    templateName = job.template.name



    project = job.conf.get('project', 'No Project')
    jobid = job.conf.smwjobid
    doesNotExists = False
    if not jobid:
        jobid = _getRandomId()
        doesNotExists = True
    site = _getMwSite()

    if templateName == 'project':
        pagename = 'moa/%s' % (project)
    else:
        pagename = 'moa/%s/job/%s' % (project, jobid)

    page = site.Pages[pagename]

    old_comments = str(page.edit()).split('<!-- you may edit below this marker -->')

    if len(old_comments) == 2:
        sysConf.smw.comments = old_comments[1].replace('<headertabs />', '').strip()
    else:
        sysConf.smw.comments = ""
        
    #print "\n".join([x[:20] for x in old_comments])

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
    #print txt
    page.save(txt)
    
    
            
    
def _saveChangeMessage(message):
    job = sysConf.job
    sysConf.smw.message = message
    sysConf.smw.commandline = " ".join(sys.argv)
    site = _getMwSite()
    project = job.conf.get('project', 'No Project')
    jobid = job.conf.get('smwjobid')
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
