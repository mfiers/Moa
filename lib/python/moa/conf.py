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
        for k,v in par.items():
            setattr(self, k, v)

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

class Config(dict):
    """
    Configuration of a job - currently mostly boilerplate code - later
    this will be a more universal configuration store
    """
    
    def __init__(self, job):
        """
        Do nothing, just initialize an empty configuration
        """
        
        self.job = job
        self.processTemplate()

        self.jobConfigFile = os.path.join(self.job.confDir, 'config')
        self.configFiles = [
            os.path.join(MOABASE, 'etc', 'config'),
            os.path.join(
                os.path.expanduser('~'), '.config', 'moa', 'config'),
            self.jobConfigFile]
        
        super(Config, self).__init__()

    def processTemplate(self):

        template = getattr(self.job, 'template', None)
        if not template:
            return
        
        for p in self.job.template['parameters']:
            self[p] = ConfigItem(
                key = p, fromTemplate = self.job.template['parameters'][p])
        
    def load(self):
        """ Load configuration from disk """
        for c in self.configFiles:
            l.debug("loading %s" % c)
            if os.path.exists(c):
                with open(c) as F:
                    data = yaml.load(F)
                for k in data.keys():
                    if not self.has_key(k):
                        self[k] = ConfigItem(key = k,
                                             value=data[k],
                                             configFile = c)
                    else:
                        self[k].value = data[k]
                        self[k].configFile = c

    def save(self):
        #save a shadow yaml configuration file
        data = dict([(k, self[k].getVal())
                     for k in self.keys()
                     if (self[k].changed() and
                         (self[k].configFile == self.jobConfigFile or
                          not self[k].configFile))
                     ])
        with open(self.jobConfigFile, 'w') as F:
            F.write(yaml.dump(data, default_flow_style=False))

    def unset(self, key):
        """
        remove a variable from the config -or, just set to to None
        if the variable is defined by the template
        """
        l.debug("unsetting %s %s" % (key, self.has_key(key)))
        if self.has_key(key):
            item = self[key]
            if item.fromTemplate: item.value=None
            else: del self[key]
            
    def set(self, key, val):
        """
        Set a configuration value from an ConfigItem
        """
        if self.has_key(key):
            self[key].value = val
            return

        item = ConfigItem(key = key,
                          value = val,
                          configFile = self.jobConfigFile)
        self[item.key] = item
        
    def has_key(self, key):
        return super(Config, self).has_key(key)
        
    def __setitem__(self, key, value):
        """
        Set an item
        """
        #see if the key already exists,
        if self.has_key(key):
            self[key].update(value)
        else:
            super(Config, self).__setitem__(key, value)

