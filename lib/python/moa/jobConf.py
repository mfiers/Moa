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
import copy

import Yaco

from jinja2 import Template as jTemplate
from jinja2 import Environment as jEnv
from jinja2 import StrictUndefined
import jinja2.exceptions

import moa.logger as l
import moa.ui
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
        self._rendered = {}
        
        #: these fields are not to be saved
        self.doNotSave = []
        
        #: these fields are not be type-checked
        self.doNotCheck = []
        
        #: these fields are private (i.e. not to be
        #: displayed by default)
        self.private = []

        #set a number of private variables to be used in variable expansion
        #MF: Moved this to a plugin
        #self.setMetavars()
        
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
            
        for delta, confFile in listToLoad:
            self.load(confFile, delta)

        #this is a temp addition - private was accidentaly
        #added to the jobconf in a number of jobs - shouldn't
        #be there..
        if self.jobConf.has_key('private'):
            del self.jobConf['private']

        self._checkJobId()


    def _checkJobId(self):
        """
        See if the job id is set - if not set it to a reasonable
        initial value
        """
        if not self.job.isMoa():
            return
        
        jobid = self['jobid']
        if jobid != 'unset': return
        name = os.path.basename(os.getcwd())
        name = re.sub("^[0-9]+\.+", "", name)
        l.debug("Setting job id to '%s'" % name)
        self['jobid'] = name
        self.save()

    def setRecursiveVar(self, k, v):
        """
        Register a recursive variable
        """
        pass
        
    def setPrivateVar(self, k, v):
        self.private.append(k)
        self.job.template.parameters[k].private = True
        self.job.template.parameters[k].mandatory = False
        #self.template.parameters[k].private = True
        self.jobConf[k] = v
        
    # def setMetavars(self):
    #     self.setPrivateVar('wd', self.job.wd)
    #     dirparts = self.job.wd.split(os.path.sep)
    #     self.setPrivateVar('dir', dirparts[-1])
    #     self.setPrivateVar('_', dirparts[-1])
    #     i = 1                
    #     while dirparts:
    #         cp = os.path.sep.join(dirparts)
    #         p = dirparts.pop()
    #         clean_p = re.sub("^[0-9]+\.+", "", p).replace('.', '_')
            
    #         #print i, clean_p, p, cp
    #         if not p: break
    #         self.setPrivateVar('dir%d' % i, p)
    #         self.setPrivateVar('_%d' % i, p)
    #         self.setPrivateVar('_%s' % clean_p, cp)

    #         if i <= 3:
    #             self.setPrivateVar('_' * i, p)

    #         i += 1

    def interpret(self, value):
        env = jEnv(undefined=StrictUndefined)
        renconf = self.render()
        templ = env.from_string(value)        
        try:
            rv = templ.render(renconf)
            return rv
        except jinja2.exceptions.UndefinedError:
            return value
        except jinja2.exceptions.TemplateSyntaxError:
            return value
        
    def render(self, force=False, showPrivate=True):

        rv = {}
        toExpand = []
                
        # first get the vars that do not need expanding and remember
        # vars that do need jinja2 rendering
        for k in self.keys():
            v = self[k]
            templateInfo = self.job.template.parameters[k]
            if templateInfo.get('prevent_expansion', False):                
                rv[k] = v
            elif isinstance(v, str) and \
               ('{{' in str(v) or '{%' in v):
                toExpand.append(k)
            else:
                rv[k] = v

        # expand the needed jinja vars
        env = jEnv(undefined=StrictUndefined)
        statesSeen = []
        iteration = 0
        while toExpand:
            iteration += 1
            if iteration > 10:
                l.debug("hard to solve -- too many iterations")
                l.debug("unsolved are %s" % str(toExpand))
                for i in toExpand:
                    l.debug("  - %s : %s" % (i, self[i]))
                break
            key = toExpand.pop(0)
            #create the template
            try:
                jt = env.from_string(self[key])
            except jinja2.exceptions.TemplateSyntaxError:
                rv[key] = self[key]
                continue

            try:
                nw = jt.render(rv)
            except jinja2.exceptions.UndefinedError:
                # not (yet?) possible
                if len(toExpand) == 0:
                    l.debug("unsolvable configuration - cannot expand '%s'" % key)
                    rv[key] = self[key]
                    break
                toExpand.append(key)
                continue
            except jinja2.exceptions.TemplateSyntaxError:
                #ignore this one - cannot be improved
                rv[key] = self[key]

            rv[key] = nw

        self._rendered = rv

        if showPrivate:
            return rv
        else:
            ov = {}
            for k in rv.keys():
                if not self.isPrivate(k):
                    ov[k] = rv[k]
            return ov

    def isPrivate(self, k):
        """
        Is this a private variable?
        can be locally defined or in the template definition

        """
        if k in self.private:
            return True
        
        if self.job.template.parameters[k].private:
            return True
        
        return False
        
    def pretty(self):
        return self.jobConf.pretty()

    def load(self, confFile, delta=None):
        """
        Load a configuration file

        :param delta: if a value appears to be a relative path,
           try to correct for this. Currently this only works
           for files that exist. i.e. 
        
        """

        
        if os.path.abspath(delta) == os.path.abspath(self.job.wd):
            loadingRecursive = False
        else:
            loadingRecursive = True

        y = Yaco.Yaco()
        y.load(confFile)

        if not delta:
            #loading the current directory - no fancy stuff... 
            self.jobConf.update(y)
            return
        
        normdelta = os.path.normpath(delta)

        if y.has_key('jobid'):
            self.setPrivateVar('_%s' % y['jobid'], normdelta)
        
        #print self.job.template.parameters.keys()
        #find relative links & see if they need to be adjusted
        if loadingRecursive:
            for k, v in y.items():

                #check if this needs to be adapted or not
                parType = self.job.template.parameters.get(k, {}).get('type')
                isFileSet = k in self.job.template.filesets.keys()

                if not (parType == 'file' or parType == 'directory' or isFileSet):
                    continue


                #find potential relative links
                if not isinstance(v, str): continue
                if not v: continue
                if not (v[:2] == './' or v[:3] == '../'):
                    continue

                moa.ui.error("Please, no recursive definition of relative paths!")
                moa.ui.error("This will surely end in tears!")
                moa.ui.error("%s %s=%s" % (os.path.abspath(delta), k, v))

                #correctedPath = os.path.normpath(delta + '/' + v)
                #relPath = os.path.relpath(correctedPath)

                #y[k] = relPath

        if y.has_key('jobid'):
            del y['jobid']
            
        self.jobConf.update(y)

    def isEmpty(self):
        """
        Check if the config is empty is empty
        """
        for k in self.keys():
            if self[k]: return False
        return True
    
    def save(self):
        """
        Save the conf to disk
        """
        if self.isEmpty():
            return            
        try:
            self.job.checkConfDir()
            self.localConf.save(self.jobConfFile, self.doNotSave)
        except OSError:
            moa.ui.error("Error saving config file")
        except IOError:
            moa.ui.error("Error saving config file")
            
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
        
    def get(self, key, default=None):
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
        if key[0] == '_' or \
               key in ['job', 'jobConf', 'jobConfFile', 'localConf',
                       'doNotCheck', 'doNotSave', 'private']:
            object.__setattr__(self, key, value)
        elif key[:4] == '_JC_':
            object.__setattr__(self, key, value)
        else:
            return self.__setitem__(key, value)
        
    def __getattr__(self, key):
        if key[0] == '_' or \
               key in ['job', 'jobConf', 'jobConfFile', 'localConf',
                       'doNotCheck', 'doNotSave', 'private']:
            object.__getattr__(self, key)
        elif key[:4] == '_JC_':
            object.__getattr__(self, key)
        else:
            return self.__getitem__(key)
