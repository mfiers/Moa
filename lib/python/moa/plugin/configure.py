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

SET_DESC = '''Set, append, change or remove variables from the configuration of a Moa job.'''

def defineCommands(commands):
    commands['set'] = {
        'desc' : SET_DESC,
        'call' : configSet,
        }

#    commands['__set'] = {
#        'private' : True,
#        'call' : configSet }


def configSet(wd, options, args):
    """
    parse the command line and save the arguments into moa.mk
    """
    
    #call the preset hooks
    moa.runMake.go(wd = wd,
                   target='moa_pre_set',
                   captureOut = False,
                   captureErr = False,
                   verbose=False)

    params = []
    for arg in args:
        if not '=' in arg: continue
        l.critical("setting %s" % arg)
        params.append(arg)

    moa.conf.writeToConf(wd, moa.conf.parseClArgs(params))

    #call the postset hooks
    moa.runMake.go(wd = wd,
                   target='moa_post_set',
                   captureOut = False,
                   captureErr = False,
                   verbose=False)



    
