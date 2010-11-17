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
moa system config
"""

import os
import sys

import Yaco
 
import moa.logger as l
import moa.utils

MOABASE = moa.utils.getMoaBase()

sysConf = None

SYSCONFIGFILE = os.path.join(MOABASE, 'etc', 'config')
USERCONFIGFILE = os.path.join(os.path.expanduser('~'),
                          '.config', 'moa', 'config')

class SysConf(Yaco.Yaco):
    
    def __init__(self):
        super(SysConf, self).__init__()
        l.debug("Loading system config: %s" % SYSCONFIGFILE)
        self.load(SYSCONFIGFILE)
        l.debug("Loading system config: %s" % USERCONFIGFILE)
        self.load(USERCONFIGFILE)

    def getPlugins(self):
        
        rv = set(sysConf.get('plugins', []))
        
        for p in sysConf.get('plugins_extra', []):
            rv.add(p)
        return list(rv)

def getPlugins():
    return sysConf.getPlugins()

sysConf = SysConf()
