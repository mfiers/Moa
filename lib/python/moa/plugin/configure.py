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

import re
import os
import sys
import readline
import moa.conf
import moa.utils
import moa.logger as l

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
    wd = data['cwd']
    args = data['newargs']

    #call the preset hooks
    job = moa.runMake.MOAMAKE(wd = wd,
                              target='moa_pre_set',
                              captureOut = False,
                              captureErr = False,
                              verbose=False)
    
    job.run()
    job.finish()

    newArgs = []

    #see if we need to query the user for input somehwere
    for a in args:
        rea = re.match(r'([a-zA-Z0-9_]+)(\+?=)\?', a)
        if rea:
            ky = rea.groups()[0]
            op = rea.groups()[1]

            df = moa.conf.getVar(wd, ky)
            vl = moa.utils.askUser("%s="%ky,df)

            newArgs.append("%s%s%s" % (ky, op, vl))
        else:
            newArgs.append(a)

    parsedArgs = moa.conf.parseClArgs(newArgs)

    moa.conf.writeToConf(wd, parsedArgs)

    #call the postset hooks
    job = moa.runMake.MOAMAKE(wd = wd,
                              target='moa_post_set',
                              captureOut = False,
                              captureErr = False,
                              verbose=False)
    job.run()
    job.finish()
