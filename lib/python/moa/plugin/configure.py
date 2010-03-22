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
import optparse
import moa.conf
from moa.logger import l

def defineCommands(commands):
    commands['set'] = {
        'desc' : 'Set or append to a configuration value. Variables ' + \
            'should be defined as "KEY=VALUE" pairs on the command-line.' + \
            'Variables can be unset using "KEY=", and in certain cases it ' +\
            'is possible to append variables to a value using "KEY+=VALUE"',
        }

    commands['__set'] = {
        'private' : True,
        'call' : configSet }

def configSet(wd, options, args):
    """
    parse the command line and save the arguments into moa.mk
    """
    command = args[0]
    newArgs = args[1:]

    params = []
    for arg in newArgs:
        if not '=' in arg: continue
        params.append(arg)

    moa.conf.writeToConf(wd, moa.conf.parseClArgs(params))


    
