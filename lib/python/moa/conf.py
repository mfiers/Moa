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
import moa.info
from moa.exceptions import *


class ConfigItem:
    reString = re.compile((r'(?P<key>[^\s=+]+)\s*'+
                           r'(?P<operator>\+?=)\s*' +
                           r'(?P<value>.*?)\s*$'))
    
    def __init__(self,
                 key = None,
                 value = None,
                 fromString=None,
                 fromTemplate=None):
        
        self.key = key
        self.value = value
        self.type = 'string'
        self.allowed = []
        self.category = ''
        self.mandatory = False
        self.help = ''
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
        return "%s %s" % (
            self.key, self.getVal())

class Config(dict):
    """
    Configuration of a job - currently mostly boilerplate code - later
    this will be a more universal configuration store
    """
    
    def __init__(self, *args, **kwargs):
        """
        Do nothing, just initialize an empty configuration
        """
        job = args[0]

        self.job = job
        self.processTemplate()
        
        self.jobConfigFile = os.path.join(self.job.confDir, 'config')
        super(Config, self).__init__()

    def processTemplate(self):
        for p in self.job.template['parameters']:
            self[p] = ConfigItem(
                key = p, fromTemplate = self.job.template['parameters'][p])
        
    def load(self):
        """ Load configuration from disk """
        data = {}
        if os.path.exists(self.jobConfigFile):
            with open(self.jobConfigFile) as F:
                data = yaml.load(F)
        for k in data.keys():
            if not self.has_key(k):
                self[k] = ConfigItem(key = k)
            self[k].value = data[k]

    def save(self):
        #save a shadow yaml configuration file
        data = dict([(k, self[k].getVal()) for k in self.keys() if self[k].changed()])
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
                          value = val)
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

@moa.utils.deprecated
def parseClArgs(args):
    """
    Parse the arguments defined on a commandline.

    @param args: command line arguments, as passed on by sys.argv or
        optparse. It is expected to be a list of strings of the
        following format; 'param=value' or 'param+=value' No spaces
        are allowed between the parameter name, value and operator.
    @type args: String of List of Strings
    

    >>> r = parseClArgs(['aap=1', 'noot=2', 'noot=3',
    ...                  'mies=test', 'mies+=roos'])
    >>> type(r) == type([])
    True
    >>> type(r[0]) == type({})
    True
    >>> r[0]['key'] == 'aap'
    True
    >>> r[1]['operator'] == '='
    True
    >>> r[2]['value'] == '3'
    True
    >>> r[4]['operator'] == '+='
    True
    >>> len(r) == 5
    True
        
    """
    rv = []
    for a in args:
        if not '=' in a:
            l.error("Invalid key/value pair %s" % a)
        if '+=' in a:
            k, v = [x.strip() for x in a.split('+=', 1)]
            o = '+='            
        else:
            o = '='
            k, v = [x.strip() for x in a.split('=', 1)]
            
        rv.append({ 'key' : k,
                    'operator' : o,
                    'value' : v })
    return rv

@moa.utils.deprecated    
def setVar(wd, key, value, relPathCorrection = None):
    """
    Convenience function - set the variable 'key' to a value in directory wd

        >>> import random
        >>> testTitle = 'title %d' % random.randint(0,10000)
        >>> import moa.job
        >>> jobdir = moa.job.newTestJob('traverse')
        >>> setVar(jobdir, 'title', testTitle)
        >>> title = getVar(jobdir, 'title')
        >>> title == testTitle
        True
        >>> try: setVar('/tmp', 'title', 'test setvar in a non-moa dir')
        ... except NotAMoaDirectory:
        ...   'Fine'
        'Fine'


    """

    # See if we can correct for relative paths
    # experimental!!
    if relPathCorrection \
       and relPathCorrection != '.' \
       and value \
       and value[0] != '/':
        
        jobInfo = moa.info.info(wd)
        dataType = jobInfo['parameters'][key]['type']
        if dataType in ['directory', 'file']:
            l.info("Attempting a relative path correction for %s" % key)
            l.info(" correcting %s" % value)
            l.info(" with %s" % relPathCorrection)
            newVal = os.sep.join([relPathCorrection, value])
            l.info(" new value %s" % newVal)
            value = newVal
        
    writeToConf(wd, [{'key' : key,
                  'operator' : '=',
                  'value' : value}])

@moa.utils.deprecated    
def appendVar(wd, key, value):
    """
    Convenience function - set the variable 'key' to a value in directory wd
    

        >>> import moa.job
        >>> jobdir = moa.job.newTestJob('traverse')
        >>> setVar(jobdir, 'title', 'one')
        >>> getVar(jobdir, 'title')
        'one'
        >>> appendVar(jobdir, 'title', 'two')
        >>> appendVar(jobdir, 'title', 'three')
        >>> getVar(jobdir, 'title')
        'one two three'
        >>> import tempfile
        >>> emptyDir = tempfile.mkdtemp()
        >>> moa.utils.removeMoaFiles(emptyDir)
        >>> try: appendVar(emptyDir, 'title', 'test setvar in a non-moa dir')
        ... except NotAMoaDirectory:
        ...   'Fine'
        'Fine'

    """    
    writeToConf(wd, [{'key' : key,
                      'operator' : '+=',
                      'value' : value}])


@moa.utils.deprecated    
def getVar(wd, key):
    """
    Get a single parameter from a moa directory

     >>> import moa.job
     >>> jobdir = moa.job.newTestJob('traverse')
    >>> setVar(jobdir, 'title', 'test getVar')
    >>> getVar(jobdir, 'title')
    'test getVar'

    :param wd: Directory to retrieve the variable from
    :type wd: String
    :param key: The name of the parameter to retrieve
    :type key: String
    :returns: The value of the parameter
    :rtype: String
    """

    if not moa.info.isMoaDir(wd):
        raise NotAMoaDirectory(wd)
    if not os.path.exists(wd):
        return False
    moamk = os.path.join(wd, 'moa.mk')
    if not os.path.exists(moamk):
        return False
    F = open(moamk, 'r')

    rv = []
    for line in F.readlines():
        line = line.strip()
        if not line: continue        
        if line.find(key) == 0:            
            #this also captures '+=' moa.mk lines!
            if '=' in line:
                value = line.split('=',1)[1]
                rv.append(value)
    F.close()
    return " ".join(rv)    

@moa.utils.deprecated    
def writeToConf(wd, data):
    """
    writeToConf - actually write something to moa.mk
    
    """

    if not moa.info.isMoaDir(wd):
        raise NotAMoaDirectory(wd)

    moamk = os.path.join(wd, 'moa.mk')
    moamktmp = os.path.join(wd, 'moa.mk.tmp')
    moamklock = os.path.join(wd, 'moa.mk.lock')

    if os.path.exists(moamk):
        if not os.access(moamk, os.W_OK):
            raise MoaPermissionDenied(wd)
    else:
        if not os.access(wd, os.W_OK):
            raise MoaPermissionDenied(wd)
    

    #refd is a refactoring of data - allows easy checking
    refd = dict([(x['key'],x) for x in data])
    l.debug("Changing variable: %s" % ", ".join(refd.keys()))
    l.debug("starting to write a new moa.mk in %s" % wd)

    #get a lock on moa.mk
    with moa.utils.flock(moamklock):
        l.debug("got a lock on moa.mk in %s" % wd)
        if os.path.exists(moamktmp):
            l.debug("removing an older?? moa.mk.tmp")
            os.unlink(moamktmp)

        #move moa.mk to a new location
        if os.path.exists(moamk):
            os.rename(moamk, moamktmp)
        else:
            #create an empty dummy file
            open(moamktmp, 'w').close()
        
        #open filehandles to both files:
        F = open(moamktmp, 'r')
        G = open(moamk, 'w')
        
        #parse through the old file
        for line in F.readlines():
            line = line.strip()
            if not line: continue
            k,o,v = re.split(r'\s*(\+?=)\s*', line, maxsplit=1)
            l.debug("read %s %s %s" % (k,o,v))
            if refd.get(k, {}).get('operator') == '=':
                #do not rewrite this line - it is being replaced
                l.debug("ignoring %s" % k)
            else:
                #if the mode is not 'set', write 
                G.write(line+"\n")
                
        for v in data:
            if v['value']:
                G.write("%(key)s%(operator)s%(value)s\n" % v)
                l.debug("%(key)s%(operator)s%(value)s\n" % v)
            else:
                l.debug("removing %s" % k)

        F.close()
        G.close()
        os.unlink(moamktmp)
    
