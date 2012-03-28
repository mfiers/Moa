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
import moa.args

from moa.sysConf import sysConf

# def hook_defineCommands():
#     sysConf['commands']['new'] = {
#         'desc' : "Create a new Moa job",
#         'call' : newJob,
#         'needsJob' : False,
#         }
    

# def hook_defineOptions():

#     parserG = sysConf.parser.get_option_group('-t')
#     if parserG == None:
#         parserG = optparse.OptionGroup(sysConf.parser, 'moa new')
#         sysConf.parser.add_option_group(parserG)    
    
#     try:
#         parserG.parser.add_option("-t", dest="title", help='define job title ' +
#         '(when creating a job)')
#     except optparse.OptionConflictError:
#         pass


@moa.args.argument('parameter', nargs='*', help='arguments for this job, specify' +
                   'as KEY=VALUE without spaces')
@moa.args.argument('template', help='name of the template to use for this moa job ')
@moa.args.argument('-t', '--title', help='mandatory job title', default='')

@moa.args.argument('-d', '--directory', help='directory to create the job in',
                   default='.')
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
    targetdir = args.directory
    title = args.title
    template = args.template
    
    params = []
    for a in args.parameter:
        if not '=' in a:
            moa.ui.exitError("Need an '=' in parameter definition (problem was: '%s')" % a)
        k,v = a.split('=', 1)
        if k == 'title':
            if title:
                moa.ui.warn("duplicate title defintions, using %s" % v)
            title = v
        else:
            params.append(a)

    if targetdir != '.':
        fulltarget = os.path.abspath(targetdir)
        if not os.path.exists(fulltarget):
            moa.ui.message("Creating directory %s" % targetdir)
            os.makedirs(fulltarget)
            
        os.chdir(fulltarget)
        #create a new job for the target dir
        job = moa.job.Job(fulltarget)

    wd = job.wd

    if os.path.exists(os.path.join(
        wd, '.moa', 'template')) and \
        not args.force:
        l.error("There is already a Moa job in")
        l.error(wd)
        l.error("use -f to override")
        
    if not title:
        moa.ui.warn("Please define a title for this job")

    provider = None
    if ':' in template:
        provider, template = template.split(':')

    try:
        job = moa.job.newJob(wd, template=template, title = title,
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

    
