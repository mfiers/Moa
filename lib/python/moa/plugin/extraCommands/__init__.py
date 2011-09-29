# Copyright 2009-2011 Mark Fiers
# The New Zealand Institute for Plant & Food Research
# 
# This file is part of Moa - http://github.com/mfiers/Moa
# 
# Licensed under the GPL license (see 'COPYING')
# 
"""
**extraCommands** - Pre & Post commands
---------------------------------------

Allow execution of a bash oneline before & after job completion
"""

import os
import moa.logger as l
import moa.ui
import jinja2

from moa.sysConf import sysConf

def hook_defineCommands():
    sysConf['commands']['postcommand'] = { 
        'desc' : 'Run the postcommand',
        'call' : runPostCommand,
        'needsJob' : True,
        'usage' : 'moa postcommand'
        }
    sysConf['commands']['precommand'] = { 
        'desc' : 'Run the precommand',
        'call' : runPreCommand,
        'needsJob' : True,
        'usage' : 'moa pprecommand'
        }

def hook_prepare_3():
    job = sysConf['job']

    job.template.parameters.precommand = {
        'category' : 'advanced',
        'optional' : True,
        'help' : 'A single command to be executed before the main run' + \
                 'starts',
        'recursive' : False,
        'type' : 'string'
        }
    
    job.template.parameters.postcommand = {
        'category' : 'advanced',
        'optional' : True,
        'help' : 'A single command to be executed after the main run ' + \
                 'starts',
        'recursive' : False,
        'type' : 'string'
        }

def runPostCommand(d):
    """
    Execute the `postcommand`
    """
    job = sysConf.job
    renderedConf = job.conf.render()

    postcommand = renderedConf.get('postcommand', '')
    if postcommand:
        moa.ui.message("Executing postcommand")
        moa.ui.message("%s" % postcommand)
        executeExtraCommand(postcommand, job)

def runPreCommand(d):
    """
    Execute the `precommand`
    """
    job = sysConf.job
    renderedConf = job.conf.render() 
    precommand = renderedConf.get('precommand', '')
    if precommand:
        moa.ui.message("Executing precommand")
        moa.ui.message("%s" % precommand)
        executeExtraCommand(precommand, job)


def executeExtraCommand(command, job):
    jobData = job.conf
    for k in job.conf.keys():
        v = job.conf[k]
        if isinstance(v, list):
            os.putenv(k, " ".join(v))
        elif isinstance(v, dict):
            continue
        else:
            os.putenv(k, str(v))            
    template = jinja2.Template(command)
    os.system(template.render(jobData))

def hook_preRun():
    """
    If defined, execute the precommand
    """
    job = sysConf['job']
    precommand = str(job.conf['precommand'])
    if precommand:
        l.debug("Executing precommand %s" % precommand)
        executeExtraCommand(precommand, job)

def hook_postRun():
    """
    If defined, execute the postCommand
    """
    job = sysConf['job']
    postcommand = str(job.conf['postcommand'])
    if postcommand:
        l.debug("Executing postcommand %s" % postcommand)
        executeExtraCommand(postcommand, job)
