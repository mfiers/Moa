# Copyright 2009-2011 Mark Fiers
# The New Zealand Institute for Plant & Food Research
# 
# This file is part of Moa - http://github.com/mfiers/Moa
# 
# Licensed under the GPL license (see 'COPYING')
# 
"""
moa.jobConf
-----------

moa job configuration
"""

import re
import os
import sys
import glob

import Yaco
 
import moa.logger as l
import moa.utils

class JobConf(object):
    """
    
    to distinguish between attributes of this object & proper job
    configuration parameters
    """
    
    def __init__(self, job):
        """
        Initialize the conf from the parent job
        """
        
        self.job = job
        self.jobConf = Yaco.Yaco()
        self.localConf = Yaco.Yaco()
        self.jobConfFile = os.path.join(self.job.confDir, 'config')

        #: these fields are not to be saved
        self.doNotSave = []
        
        #: these fields are not be type-checked
        self.doNotCheck = []
        
        #: these fields are private (i.e. not to be
        #: displayed by default)
        self.private = []

        #load the local conf separately - 
        if os.path.exists(self.jobConfFile):
            self.localConf.load(self.jobConfFile)

        #create a list of conf files to load:
        listToLoad = []        
        parsePath = self.job.wd
        if not parsePath[-1] == '/':
            parsePath += '/'
        lookAt = parsePath

        while True:

            abspath = os.path.abspath(lookAt)

            # not expecting a .moa in the root and don't need to go
            # higher up
            if abspath == '/': break 

            #see if there is a moa job & config file - if so, add it to the list
            thisConfig = os.path.join(abspath, '.moa', 'config')
            if os.path.isfile(thisConfig):
                listToLoad.insert(0,  (lookAt, thisConfig))

            #look at: one directory up
            lookAt = lookAt + '../'
            
        #sys.stderr.write("%s" % listToLoad)
        for delta, confFile in listToLoad:
            #sys.stderr.write("loading %s %s" % (delta, confFile))
            self.load(confFile, delta)

        #this is a temp addition - private was accidentaly
        #added to the jobconf in a number of jobs - shouldn't
        #be there..
        if self.jobConf.has_key('private'):
            del self.jobConf['private']


    def pretty(self):
        return self.jobConf.pretty()

    def load(self, confFile, delta=None):
        """
        Load a configuration file

        :param delta: if a value appears to be a relative path,
           try to correct for this. Currently this only works
           for files that exist. i.e. 
        
        """
        y = Yaco.Yaco()
        y.load(confFile)

        #find relative links & see if they need to be adjusted
        #
        for k, v in y.items():
            #find potential relative links
            if not isinstance(v, str): continue
            if not v: continue
            if not (v[:2] == './' or v[:3] == '../'):
                continue
            correctedPath = os.path.normpath(delta + '/' + v)
            if os.path.exists(correctedPath):
                y[k] = correctedPath
            elif glob.glob(correctedPath):
                y[k] = correctedPath

        self.jobConf.update(y)

    def save(self):
        self.job.checkConfDir()
        self.localConf.save(self.jobConfFile, self.doNotSave)

    def setInJobConf(self, key):
        c = self._get_conf(key)
        if c.has_key(key):
            return True
        else:
            return False

    def keys(self):
        """
        return a dict with all known parameters and values, either
        defined in the job configuration of the template
        """
        rvt = set(self.job.template.parameters.keys())
        rvj = set(self.jobConf.keys())
        return list(rvt.union(rvj))

    def _is_recursive(self, key):
        keyInfo = self.job.template.parameters.get(key, {})
        return keyInfo.get('recursive', True)
    
    def _get_conf(self, key):
        if self._is_recursive(key):
            return self.jobConf
        else:
            return self.localConf

    def is_local(self, key):
        if self.localConf.has_key(key):
            return True
        else:
            return False

    def has_key(self, key):
        c = self._get_conf(key)
        if c.has_key(key):
            return True
        if self.job.template.parameters.has_key(key):
            return True
        return False

    def update(self, data):
        self.localConf.update(data)
        
    def get(self, key, default):
        c = self._get_conf(key)
        v = c.__getitem__(key)
        if v: 
            return v
        else:
            return default
        
    def __getitem__(self, key):
        v = ''
        c = self._get_conf(key)
        if c.has_key(key):
            v = c[key]
        elif key in self.job.template.parameters.keys() and \
                 self.job.template.parameters[key].has_key('default'):
            v = self.job.template.parameters[key].default

        if key in self.job.template.parameters.keys() and \
               self.job.template.parameters[key].has_key('callback'):
            v = self.job.template.parameters[key].callback(key, v)
        return v
    
    def __delitem__(self, key):
        del(self.localConf[key])

    def __setitem__(self, key, value):
        if key in self.job.template.parameters.keys():
            pd = self.job.template.parameters[key]
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
        self.localConf[key] = value

    def __setattr__(self, key, value):
        if key in ['job', 'jobConf', 'jobConfFile', 'localConf',
                   'doNotCheck', 'doNotSave', 'private']:
            object.__setattr__(self, key, value)
        elif key[:4] == '_JC_':
            object.__setattr__(self, key, value)
        else:
            return self.__setitem__(key, value)
        
    def __getattr__(self, key):
        if key in ['job', 'jobConf', 'jobConfFile', 'localConf',
                   'doNotCheck', 'doNotSave', 'private']:
            object.__getattr__(self, key)
        elif key[:4] == '_JC_':
            object.__getattr__(self, key)
        else:
            return self.__getitem__(key)
