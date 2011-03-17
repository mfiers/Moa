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

import moa.ui
import moa.utils
import moa.logger as l

def defineCommands(data):
    """
    Set the moa commands for this plugin
    """
    data['commands']['set'] = {
        'desc' : 'Set, change or remove variables',
        'usage' : 'moa set [KEY] [KEY=VALUE]',
        'call' : configSet,
        'needsJob' : True,
        'log' : True
        }
    data['commands']['unset'] = {
        'desc' : 'Remove a variable',
        'call' : configUnset,
        'usage' : 'moa unset KEY',
        'needsJob' : True,
        'log' : True
        }

    data['commands']['show'] = {
        'desc' : 'Show configured variables',
        'call' : configShow,
        'usage' : 'moa show',
        'needsJob' : True,
        'log' : False
        }

def configShow(data):
    """
    Show all parameters know to this job. Parameters in **bold** are
    specifically configured for this job (as opposed to those
    parameters that are set to their default value). Parameters in red
    are not configured, but need to be for the template to
    operate. Parameters in blue are not configured either, but are
    optional.
    """
    job = data['job']
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

def configUnset(data):
    """
    Remove a configured parameter from this job. In the parameter was
    defined by the job template, it reverts back to the default
    value. If it was an ad-hoc parameter, it is lost from the
    configuration.
    """

    job = data['job']
    for a in data['newargs']:
        if '=' in a:
            l.error("Invalid argument to unset %s" % a)
        else:
            l.debug("Unsetting %s" % a)
            del job.conf[a]
    job.conf.save()

    
def configSet(data):
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
    job = data['job']
    args = data['newargs']

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

TESTSCRIPT = """
moa new adhoc -t 'something'
moa set title='something else'
moa set undefvar='somewhat'
moa set adhoc_mode=par
moa show || exer moa show does not seem to work
moa show | grep -q 'title[[:space:]\+]something else' || exer title is not set properly
"""
