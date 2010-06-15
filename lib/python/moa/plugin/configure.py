# 
# Copyright 2009 Mark Fiers, Plant & Food Research
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

import os
import sys
import shlex
import optparse
import moa.conf
from moa.logger import l

def defineCommands(data):
    data['commands']['set'] = {
        'desc' : 'Set, append, change or remove variables from the ' +
        'configuration of a Moa job.',
        'call' : configSet,
        }

def configSet(data):
    """
    parse the command line and save the arguments into moa.mk
    """
    wd = data['wd']
    optons = data['options']
    args = data['args']

    #call the preset hooks
    job = moa.runMake.MOAMAKE(wd = wd,
                              target='moa_pre_set',
                              captureOut = False,
                              captureErr = False,
                              verbose=False)
    
    job.run()
    job.finish()

    params = []
    for arg in data['args']:
        if not '=' in arg: continue
        l.debug("setting %s" % arg)
        params.append(arg)

    moa.conf.writeToConf(wd, moa.conf.parseClArgs(params))

    #call the postset hooks
    job = moa.runMake.MOAMAKE(wd = wd,
                              target='moa_post_set',
                              captureOut = False,
                              captureErr = False,
                              verbose=False)
    job.run()
    job.finish()
