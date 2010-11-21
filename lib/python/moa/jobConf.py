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
moa.jobConf
-----------

moa job configuration
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

class JobConf(object):
    
    def __init__(self, job):
        """
        Initialize the conf from the parent job
        """
        
        self.job = job
        self.template = self.job.template
        self.jobConfFile = os.path.join(self.job.confDir, 'config')
        self.jobConf = Yaco.Yaco()
        if os.path.exists(self.jobConfFile):
            self.jobConf.load(self.jobConfFile)

    def save(self):
        self.job.checkConfDir()
        self.jobConf.save(self.jobConfFile)

    def setInJobConf(self, key):
        if self.jobConf.has_key(key):
            return True
        else:
            return False

    def keys(self):
        """
        return a dict with all known parameters and values, either
        defined in the job configuration of the template
        """
        rvt = set(self.template.parameters.keys())
        rvj = set(self.jobConf.keys())
        return list(rvt.union(rvj))

    def has_key(self, key):
        if self.jobConf.has_key(key):
            return True
        if self.template.parameters.has_key(key):
            return True
        return False
        
    def __getitem__(self, key):
        if self.jobConf.has_key(key):
            return self.jobConf[key]
        elif key in self.template.parameters.keys():
            if self.template.parameters[key].has_key('default'):
                return self.template.parameters[key].default
            else:
                return ''

    def __delitem__(self, key):
        del(self.jobConf[key])

    def __setitem__(self, key,value):
        self.jobConf[key] = value

