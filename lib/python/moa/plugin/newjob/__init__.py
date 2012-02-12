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
import moa.logger as l
import moa.plugin
import moa.ui
from moa.sysConf import sysConf

def hook_defineCommands():
    sysConf['commands']['new'] = {
        'desc' : "Create a new Moa job",
        'call' : newJob,
        'needsJob' : False,
        }
    

def hook_defineOptions():

    parserG = sysConf.parser.get_option_group('-t')
    if parserG == None:
        parserG = optparse.OptionGroup(sysConf.parser, 'moa new')
        sysConf.parser.add_option_group(parserG)    
    
    try:
        parserG.parser.add_option("-t", dest="title", help='define job title ' +
        '(when creating a job)')
    except optparse.OptionConflictError:
        pass

    
def newJob(job):
    """
    **moa new**

    Usage::

        moa new TEMPLATE_NAME [TARGET_DIR] -t 'a descriptive title'
        
    """
    wd = job.wd
    options = sysConf['options']
    args = sysConf['newargs']

    if not args:
        moa.ui.exitError("No template specified. Try `moa new TEMPLATENAME`")
    
    params = []
    template = 'empty'
    targetdir = '.'
    
    title = job.conf.title

    if options.title:
        title = options.title
        
    args2 = []
    for a in args:
        if '=' in a:
            k,v = a.split('=', 1)
            if k == 'title':
                if options.title:
                    moa.ui.warn("duplicate title defintions, using %s" % v)
                title = v
            else:
                params.append(a)
        else:
            args2.append(a)

    if len(args2) > 0:
        template = args2[0]
    if len(args2) > 1:
        targetdir = args2[1]

    fulltarget = os.path.abspath(targetdir)
    if targetdir != '.':
        if not os.path.exists(fulltarget):
            moa.ui.message("Creating directory %s" % targetdir)
            os.makedirs(fulltarget)

        os.chdir(fulltarget)
        job = moa.job.Job(fulltarget)

    wd = job.wd

    if os.path.exists(os.path.join(
        wd, '.moa', 'template')) and \
        not options.force:
        l.error("Seems that there is already a Moa job in")
        l.error(wd)
        l.error("use -f to override")
        
    if not title:
        moa.ui.warn("Please define a title for this job")

    provider = None
    if ':' in template:
        provider, template = template.split(':')

    try:
        job = moa.job.newJob(wd, template=template, title = options.title,
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

    if provider:
        moa.ui.fprint("Created a Moa {{bold}}%s{{reset}}:{{green}}%s{{reset}} job" %
                      (provider, template),
                      f='jinja')
    else:
        moa.ui.fprint("Created a Moa {{green}}{{bold}}%s{{reset}} job" % template,
                      f='jinja')

def hook_git_finish_new():
    l.debug('running git add for newjob')
    job = sysConf.job
    sysConf.git.commitJob(job, "Created job %s in %s" % (job.template.name, job.wd))

    
