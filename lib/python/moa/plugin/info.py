# Copyright 2009-2011 Mark Fiers
# The New Zealand Institute for Plant & Food Research
# 
# This file is part of Moa - http://github.com/mfiers/Moa
# 
# Licensed under the GPL license (see 'COPYING')
# 
"""
**info** - Job information
---------------------------

Print info on Moa jobs and Moa
"""

import moa.ui
import moa.utils
import moa.actor
import moa.template

def defineCommands(data):
    """
    Set the moa commands for this plugin
    """

    data['commands']['raw_commands'] = {
        'private' : True,
        'log' : False,
        'needsJob' : True,
        'call' : rawCommands,
        }
    
    data['commands']['raw_parameters'] = {
        'private' : True,
        'log' : False,
        'needsJob' : True,
        'call' : rawParameters,
        }
    data['commands']['version'] = {
        'desc' : 'Print the moa version',
        'call' : version,
        'log' : False,
        'needsJob' : False
        }
    data['commands']['out'] = {
        'desc' : 'Returns stdout of the last moa run',
        'call' : getOut,
        'needsJob' : True,
        'log' : False
        }
    data['commands']['err'] = {
        'desc' : 'Returns stderr of the last moa run',
        'call' : getErr,
        'needsJob' : True,
        'log' : False
        }


def getOut(data):
    out = moa.actor.getLastStdout(data.job)
    if out == None:
        moa.ui.exitError("No stdout found")
    else:
        print out

def getErr(data):
    err = moa.actor.getLastStderr(data.job)
    if err == None:
        moa.ui.exitError("No stderr found")
    else:
        print err

def version(data):
    """
    **moa version** - Print the moa version number
    """
    print data.sysConf.getVersion()

def status(data):
    """
    **moa status** - print out a short status status message

    Usage::

       moa status
       
    """
    job = data['job']
    if job.template.name == 'nojob':
        moa.ui.fprint("%(bold)s%(red)sNot a Moa job%(reset)s")
        return
    moa.ui.fprint("%(bold)s%(green)sThis is a Moa job%(reset)s")
    moa.ui.fprint("%%(blue)s%%(bold)sTemplate name: %%(reset)s%s" %
                  job.template.name)
   
def rawCommands(data):
    """
    *(private)* **moa raw_commands** - Print a list of all known commands
    
    Usage::

        moa raw_commands

    Print a list of known Moa commands, both global, plugin defined
    commands as template specified ones. This command is mainly used
    by software interacting with Moa.
    """
    job = data['job']
    commands = data['commands']
    c = commands.keys()
    if job.template.name != 'nojob':
        c.extend(job.template.commands)
    print ' '.join(c)


def rawParameters(data):
    """
    *(private)* **moa raw_parameters** - Print out a list of all known parameters

    Usage::

        moa raw_parameters
        
    print a list of all defined or known parameters
    """
    job = data['job']
    if job.template.name == 'nojob':
        return
    print " ".join(job.conf.keys())


TESTSCRIPT = """
moa new adhoc -t 'something'
moa set mode=simple
moa set process='echo "ERR" >&2; echo "OUT"'
moa run
moa out | grep OUT
moa err | grep ERR
moa version
"""
