#
# Copyright 2009, 2010 Mark Fiers, Plant & Food Research
# 
# This file is part of Moa - http://github.com/mfiers/Moa
# 
# Moa is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your
# option) any later version.
# 
# Moa is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
# or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public
# License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with Moa.  If not, see <http://www.gnu.org/licenses/>.
# 
"""
Job information
---------------

Print info on Moa jobs and Moa
"""

import optparse

import moa.ui
import moa.utils
import moa.actor
import moa.logger as l
import moa.template

def defineCommands(data):
    """
    Set the moa commands for this plugin
    """
    data['commands']['status'] = {
        'desc' : 'Show the state of the current job',
        'log' : False,
        'needsJob' : True,
        'call' : status,
        }
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
    print data.sysConf.__class__.__name__
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
