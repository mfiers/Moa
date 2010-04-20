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

import moa.runMake
import moa.info
import moa.logger
l = moa.logger.l

def defineCommands(commands):
    commands['help'] = {
        'desc' : 'Display help on the current job (not this help!)',
        'call' : showHelp
        }

def showHelp(wd, options, args):
    if not moa.info.isMoaDir(wd):
        l.error("This is not a moa directory - you can run moa help only in")
        l.error("the context of a Moa directory. You could try: moa --help")
        sys.exit(-1)
    moa.runMake.go(wd, target = 'help', verbose = options.verbose)
    


