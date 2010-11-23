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
Moa script - get and set variables to the moa.mk file
"""

import re
import os
import sys
import yaml
import shlex

import Yaco
 
import moa.logger as l
from moa.logger import exitError
import moa.utils
from moa.exceptions import *

MOABASE = moa.utils.getMoaBase()

class ConfigItem:
    reString = re.compile((r'(?P<key>[^\s=+]+)\s*'+
                           r'(?P<operator>\+?=)\s*' +
                           r'(?P<value>.*?)\s*$'))
    
    def __init__(self,
                 key = None,
                 value = None,
                 fromString=None,
                 configFile = None,
                 fromTemplate=None):
        
        self.key = key
        self.value = value
        self.type = 'string'
        self.allowed = []
        self.category = ''
        self.mandatory = False
        self.help = ''
        self.configFile = configFile
        self.default = ''
        self.cardinality = 'one'
        self.fromTemplate = False
        
        if fromTemplate:
            self._parseTemplateParam(key, fromTemplate)

    def _parseTemplateParam(self, key, par):
        """
        Initialize config item from a parameter entry
        """
        self.fromTemplate = True
        for k in par.keylist:
            setattr(self, k, getattr(par, k))

    def changed(self):
        """
        Is this parameter different from what is specified in
        the template definition?
        """
        if not self.fromTemplate:
            #if not specified in the template, make it talway, always True
            return True
        elif self.value == None:
            #not set, not changed
            return False        
        elif self.value == self.default:
            return False
        else:
            return True
        
    def getVal(self):
        if self.value: return self.value
        return self.default
    
    def __str__(self):
        return str(self.getVal())

class Config(Yaco.Yaco):
    """
    Configuration of a job - currently mostly boilerplate code - later
    this will be a more universal configuration store
    """
    
    def __init__(self, job):
        """
        Do nothing, just initialize an empty configuration
        """
        
        super(Config, self).__init__()
        self.meta.job = job        
        self.meta.jobConfigFile = os.path.join(
            self.meta.job.confDir, 'config')        
        self.meta.configFiles = {
            "system" : os.path.join(MOABASE, 'etc', 'config'),
            "user" : os.path.join(os.path.expanduser('~'),
                                  '.config', 'moa', 'config'),
            "job" : self.meta.jobConfigFile 
                } 
        self.moa_plugins = []
        self.moa_plugins.data_type = 'set'
        self.processTemplate()

    def processTemplate(self):

        template = getattr(self.meta.job, 'template', None)

        if not template:
            return
        
        for parname in template.parameters.keys():
            par = template.parameters[parname]
            self[parname] = None
            self[parname].configure_from(par)
    
    def load(self):
        """ Load configuration from disk """        
        for f in self.meta.configFiles.keys():
            fileName = self.meta.configFiles[f]
            l.debug("Considering config file %s / %s" % (f, fileName))                        
            if os.path.exists(fileName):            
                super(Config, self).load(fileName, set_name=f)

    def save(self):
        """
        Save local configuration 
        """
        self.meta.job.checkConfDir()
        super(Config, self).save(self.meta.jobConfigFile,
                                 set_names=['job', None])
        
    def getPlugins(self):
        """
        Return a list of all plugins
        """
        rv = set(self.moa_plugins.value)
        for x in self.get('moa_plugins_local', []):
            rv.add(x)
        return list(rv)        
