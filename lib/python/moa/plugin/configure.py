# Copyright 2009-2011 Mark Fiers
# The New Zealand Institute for Plant & Food Research
# 
# This file is part of Moa - http://github.com/mfiers/Moa
# 
# Licensed under the GPL license (see 'COPYING')
# 
"""
**configure** - Configure jobs
------------------------------

Control job configuration
"""
import os

import moa.ui
import moa.utils
import moa.logger as l
from moa.sysConf import sysConf

def defineCommands(data):
    """
    Set the moa commands for this plugin
    """
    data['commands']['set'] = {
        'desc' : 'Set, change or remove variables',
        'usage' : 'moa set [KEY] [KEY=VALUE]',
        'call' : configSet,
        'needsJob' : True,
        'recursive' : 'global',
        'log' : True,
        'unittest' : TESTSET
        }
    
    data['commands']['unset'] = {
        'desc' : 'Remove a variable',
        'call' : configUnset,
        'usage' : 'moa unset KEY',
        'recursive' : 'global',
        'needsJob' : True,
        'log' : True,
        'unittest' : TESTUNSET
        }

    data['commands']['show'] = {
        'desc' : 'Show configured variables',
        'call' : configShow,
        'usage' : 'moa show',
        'needsJob' : True,
        'log' : False
        }

def configShow(job):
    """
    Show all parameters know to this job. Parameters in **bold** are
    specifically configured for this job (as opposed to those
    parameters that are set to their default value). Parameters in red
    are not configured, but need to be for the template to
    operate. Parameters in blue are not configured either, but are
    optional.
    """
    job = sysConf['job']
    moa.utils.moaDirOrExit(job)
    
    keys = job.conf.keys()
    keys.sort()

    for p in keys:
        if p[:4] == 'moa_': continue
        
        if job.template.parameters[p].private == True:
            continue
        
        if job.conf.setInJobConf(p):
            moa.ui.fprint("{{bold}}%s\t%s{{reset}}" % (
                p, job.conf[p]), f='jinja')
        else:
            if job.template.parameters[p].optional:
                moa.ui.fprint("{{blue}}%s\t%s{{reset}}" % (
                    p, job.conf[p]), f='jinja')
            else:
                moa.ui.fprint("{{red}}%s\t%s{{reset}}" % (
                    p, job.conf[p]), f='jinja')

def _unsetCallback(wd, vars):
    """
    Does the actual unset of variables `vars` in folder `wd`:
    """
    job = moa.job.Job(wd)
    #print "unsetting", " ".join(data.unset), "in", wd
    for u in vars:
        try:
            del job.conf[u]
        except KeyError:
            pass        
    job.conf.save()
    
def configUnset(job):
    """
    Remove a configured parameter from this job. In the parameter was
    defined by the job template, it reverts back to the default
    value. If it was an ad-hoc parameter, it is lost from the
    configuration.
    """
    options = sysConf.options

    for a in sysConf.newargs:
        if '=' in a:
            moa.ui.exitError("Invalid argument to unset %s" % a)
        try:
            del job.conf[a]
        except KeyError:
            #probably a non existsing key - ignore
            pass
        
    job.conf.save()
    
def configSet(job):
    """
    This command can be used in a number of ways::

        moa set PARAMETER_NAME=PARAMETER_VALUE
        moa set PARAMETER_NAME='PARAMETER VALUE WITH SPACES'
        moa set PARAMETER_NAME

    In the first two forms, moa sets the parameter `PARAMETER_NAME` to
    the `PARAMETER_VALUE`. In the latter form, Moa will present the
    user with a prompt to enter a value. Note that the first two forms
    the full command lines will be processed by bash, which can either
    create complications or prove very useful. Take care to escape
    variables that you do not want to be expandend and use single quotes
    where you can. 
    """
    args = sysConf['newargs']

    #see if we need to query the user for input somehwere
    for a in args:
        if not '=' in a:
            old = job.conf[a]
            val = moa.ui.askUser("%s:\n$ " % a, old)
            job.conf[a] = val
        else:
            key,val = a.split('=',1)
            job.conf[key] = val
    job.conf.save()


##### TESTSCRIPTS

TESTUNSET = """
moa simple -t test -- echo
moa show | grep -Pq 'title\ttest'
moa unset title
moa show | grep -Pqv 'title\ttest'
# recursive unset
moa set aaa=bbb
moa show | grep -Pq 'aaa\tbbb'
mkdir 10.sub
cd 10.sub
moa simple -t sub -- echo
moa set aaa=bbb
moa show | grep -Pq 'aaa\tbbb'
cd ..
moa unset -r aaa
moa show | grep -Pqv 'aaa\tbbb'
cd 10.sub
moa show | grep -Pqv 'aaa\tbbb'
"""

TESTSET = """
moa simple -t test -- echo
moa show | grep -Pq 'title\ttest'
moa show | grep -Pqv 'title\totherwise'
moa set title=otherwise
moa show | grep -Pqv 'title\ttest'
moa show | grep -Pq 'title\totherwise'
moa set dummy=bla
moa show | grep -Pq 'dummy\tbla'
#now try recursive loading of variables
mkdir 10.subdir
cd 10.subdir
moa simple -t subtest -- echo
moa show | grep -Pq 'dummy\tbla'
moa show | grep -Pqv 'title\ttest'
"""
