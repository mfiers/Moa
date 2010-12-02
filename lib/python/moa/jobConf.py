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

import re
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

        #these fields are not to be saved
        self.doNotSave = []
        #these fields are not be by checked
        self.doNotCheck = []
        
        if os.path.exists(self.jobConfFile):
            self.jobConf.load(self.jobConfFile)

    def save(self):
        self.job.checkConfDir()
        self.jobConf.save(self.jobConfFile, self.doNotSave)

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

    def update(self, data):
        self.jobConf.update(data)
        
    def get(self, key, default):
        v = self.__getitem__(key)
        if v: 
            return v
        else:
            return default
        
    def __getitem__(self, key):
        v = ''
        if self.jobConf.has_key(key):
            v = self.jobConf[key]
        elif key in self.template.parameters.keys() and \
                 self.template.parameters[key].has_key('default'):
            v = self.template.parameters[key].default

        if isinstance(v, str) and '{{' in v:
            rere = re.compile('\{\{ *([^ \}]*) *\}\}')
            v = rere.sub(lambda x: self.__getitem__(x.groups()[0]), v)

        if key in self.template.parameters.keys() and \
               self.template.parameters[key].has_key('callback'):
            v = self.template.parameters[key].callback(v)
        return v
    
    def __delitem__(self, key):
        del(self.jobConf[key])

    def __setitem__(self, key,value):
        if key in self.template.parameters.keys():
            pd = self.template.parameters[key]
            if pd.type == 'boolean':
                if value.lower() in ["yes", "true", "1", 'y', 't']:
                    value = True
                else: value = False
            elif pd.type == 'integer':
                try:
                    value = int(value)
                except ValueError:
                    pass
            elif pd.type == 'float':
                try:
                    value = float(value)
                except ValueError:
                    pass
                
                    
        self.jobConf[key] = value

