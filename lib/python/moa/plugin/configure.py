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
Configure jobs
--------------

Control job configuration
"""

import optparse

import moa.ui
import moa.utils
import moa.logger as l

def defineCommands(data):
    """
    Set the moa commands for this plugin
    """
    data['commands']['set'] = {
        'desc' : 'Set, append, change or remove variables from the ' +
        'configuration of a Moa job.',
        'call' : configSet,
        }
    data['commands']['unset'] = {
        'desc' : 'Remove (the value of) a variable',
        'call' : configUnset,
        }

    data['commands']['show'] = {
        'desc' : 'Show the current configured variables',
        'call' : configShow,
        }


def configShow(data):
    """
    **moa show** - show the value of all parameters

    Usage::

       moa show


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
        if job.conf.setInJobConf(p):
            moa.ui.fprint("%%(bold)s%s\t%s%%(reset)s" % (
                p, job.conf[p]))
        else:
            if job.template.parameters[p].optional:
                moa.ui.fprint("%%(blue)s%s\t%s%%(reset)s" % (
                    p, job.conf[p]))
            else:
                moa.ui.fprint("%%(red)s%s\t%s%%(reset)s" % (
                    p, job.conf[p]))


def configUnset(data):
    """
    **moa unset** - remove variables from the configuration

    Usage::

       moa unset PARAMETER_NAME

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
    **moa set** - set the value of one or more parameters

    Usage::

        moa set PARAMETER_NAME=PARAMETER_VALUE
        moa set PARAMETER_NAME='PARAMETER VALUE WITH SPACES'
        moa set PARAMETER_NAME

    In the first two forms, moa set set the parameter 'PARAMETER_NAME'
    to the described value. In the latter form, Moa will present the
    user with a prompt to enter the value. Note that these command
    lines will first be processed by bash, and care needs to be taken
    that bash does not expand or interpret special characters. To
    prevent this, the third form can be used.
    """
    job = data['job']
    args = data['newargs']

    newArgs = []

    #see if we need to query the user for input somehwere
    for a in args:
        if not '=' in a:
            old = job.conf[a]
            val = moa.utils.askUser("%s:\n$ " % a, old)
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
