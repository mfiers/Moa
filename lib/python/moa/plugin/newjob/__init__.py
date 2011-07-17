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
    try:
        sysConf.parser.add_option("-t", dest="title", help="Job title")
    except optparse.OptionConflictError:
        pass

def newJob(job):
    """
    **moa new**

    Usage::

        moa new TEMPLATE_NAME -t 'a descriptive title'
        
    """
    wd = job.wd
    options = sysConf['options']
    args = sysConf['newargs']
    if not args:
        moa.ui.exitError("No template specified. Try `moa new TEMPLATENAME`")
    
    params = []
    template = 'empty'

    title = job.conf.title
    if options.title:
        title = options.title
        
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
            template = a

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

    job.conf.save()

    if provider:
        moa.ui.fprint("Created a Moa {{bold}}%s{{reset}}:{{green}}%s{{reset}} job" %
                      (provider, template),
                      f='jinja')
    else:
        moa.ui.fprint("Created a Moa {{green}}{{bold}}%s{{reset}} job" % template,
                      f='jinja')
