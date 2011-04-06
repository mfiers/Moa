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

def defineCommands(data):
    data['commands']['new'] = {
        'desc' : "Create a new Moa job",
        'call' : newJob,
        'needsJob' : False
        }
    

def defineOptions(data):
    try:
        parserN = optparse.OptionGroup(data['parser'], "moa new")
        data['parser'].set_defaults(title="")
        parserN.add_option("-t", "--title", dest="title", help="Job title")
        data['parser'].add_option_group(parserN)
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

    params = []
    template = 'traverse'
    
    for a in args:
        if '=' in a:
            params.append(a)
        else:
            template = a


    if os.path.exists(os.path.join(
        wd, '.moa', 'template')) and \
        not options.force:
        l.error("Seems that there is already a Moa job in")
        l.error(wd)
        l.error("use -f to override")

    if not options.title:
        moa.ui.exitError("Must define a title for this job")
        
    job = moa.job.newJob(wd, template=template, title = options.title)
    job.conf['title'] = options.title
    
    for p in params:
        k,v = p.split('=', 1)
        job.conf[k] = v

    job.conf.save()

    moa.ui.fprint("Created a Moa {{green}}{{bold}}%s{{reset}} job" % template,
                  f='jinja')
    #moa.ui.fprint('With title "%%(bold)s%s%%(reset)s"' % job.conf.title)



TESTSCRIPT = """
moa new adhoc -t 'testJob' adhoc_mode=par dummy=nonsense
[[ -d ./.moa ]] || exer 'No job was created'
"""
