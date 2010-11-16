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
Help
"""

import re
import os
import sys
import readline
import moa.ui
import moa.conf
import moa.utils
import moa.logger as l

def defineCommands(data):
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
    Print the configuration (from moa.mk) to stdout
    """
    job = data['job']
    moa.utils.moaDirOrExit(job)
    
    keys = job.conf.keys()
    keys.sort()
    
    for p in keys:
        if job.conf.setInJobConf(p):
            moa.ui.fprint("%%(bold)s%s\t%s%%(reset)s" % (
                p, job.conf[p]))
        else:
            moa.ui.fprint("%%(blue)s%s\t%s%%(reset)s" % (
                p, job.conf[p]))


def configUnset(data):
    """
    remove variables from the configuration
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
    parse the command line and save the arguments into moa.mk
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
moa show | grep -q 'title[[:space:]\+]else' || exer title is not set properly
moa set title+=test
moa show | grep -q 'title[[:space:]\+]else test' || exer title is not set properly
"""
