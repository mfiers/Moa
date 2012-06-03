# Copyright 2009-2011 Mark Fiers
# The New Zealand Institute for Plant & Food Research
# 
# This file is part of Moa - http://github.com/mfiers/Moa
# 
# Licensed under the GPL license (see 'COPYING')
# 
"""
**newjob** - Instantiate new jobs
---------------------------------
"""

import os

import optparse
import moa.job
import moa.logger

l = moa.logger.getLogger(__name__)
#l.setLevel(moa.logger.DEBUG)

import moa.plugin
import moa.ui
import moa.args

from moa.sysConf import sysConf

#@moa.args.argument('-d', '--directory', help='directory to create the job in',
#                   default='.')
@moa.args.argument('parameter', nargs='*', help='arguments for this job, specify' +
                   'as KEY=VALUE without spaces')
@moa.args.argument('template', help='name of the template to use for this moa job ')
@moa.args.argument('-t', '--title', help='mandatory job title', default='')
@moa.args.forceable
@moa.args.command
def new(job, args):
    """
    Create a new job.

    This command creates a new job with the specified template in the
    current directory. If the directory already contains a job it
    needs to be forced using '-f'. It is possible to define arguments
    for the job on the commandline using KEY=VALUE after the
    template. Note: do not use spaces around the '=' sign. Use quotes
    if you need spaces in variables (KEY='two values')
        
    """

    wd = job.wd
    #targetdir = args.directory
    title = ""
    if job.conf.title:
        title = job.conf.title
    if args.title:
        title = args.title

    template = args.template
    
    params = []
    for a in args.parameter:
        if not '=' in a:
            moa.ui.exitError("Need an '=' in parameter definition (problem was: '%s')" % a)
        k,v = a.split('=', 1)
        if k == 'title':
            if title:
                moa.ui.warn('Duplicate title defintions, using "%s"' % v)
            title = v
        else:
            params.append(a)

    # if targetdir != '.':
    #     fulltarget = os.path.abspath(targetdir)
    #     if not os.path.exists(fulltarget):
    #         moa.ui.message("Creating directory %s" % targetdir)
    #         os.makedirs(fulltarget)
            
    #     os.chdir(fulltarget)
    #     #create a new job for the target dir
    #     job = moa.job.Job(fulltarget)

    wd = job.wd

    if os.path.exists(os.path.join(wd, '.moa', 'template')) and not args.force:
        moa.ui.exitError("This directory already contains a moa job\nUse -f to override")

    if not title:
        moa.ui.warn("Please define a title for this job")

    originaltemplate = template
    provider = None
    if ':' in template:
        provider, template = template.split(':')

    try:
        l.debug("instantiating new job")
        job = moa.job.newJob(job, template=template, title = title,
                             provider=provider)
    except moa.exceptions.InvalidTemplate:
        moa.ui.exitError("Invalid template: %s" % template)
        
    job.conf['title'] = title

    for p in params:
        k,v = p.split('=', 1)
        job.conf[k] = v

    #if no title is set - see if there is one set in the template
    if not job.conf.title and job.template.parameters.title.default:
        job.conf.title = job.template.parameters.title.default

    job.conf.save()

    moa.ui.message('Created a "%s" job' % originaltemplate)
    if title:
        moa.ui.message('with title "%s"' % title)
        

def hook_git_finish_new():
    l.debug('running git add for newjob')
    job = sysConf.job
    sysConf.git.commitJob(job, "Created job %s in %s" % (job.template.name, job.wd))

    
