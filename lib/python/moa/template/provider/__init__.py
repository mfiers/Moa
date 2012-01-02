# Copyright 2009-2011 Mark Fiers
# The New Zealand Institute for Plant & Food Research
# 
# This file is part of Moa - http://github.com/mfiers/Moa
# 
# Licensed under the GPL license (see 'COPYING')
# 
"""
moa.provider
-------------

Provides templates..


"""

import os
import datetime

import Yaco

import moa.ui
import moa.exceptions

from moa.sysConf import sysConf

class Providers(object):
    
    def __init__(self):
        self.providers = {}
        self.order = []

        _order = []
        for pName in sysConf.template.providers.keys():
            pInfo = sysConf.template.providers[pName]
            priority = pInfo.get('priority', 1)
            assert(isinstance(priority, int))
            
            #import the correct module
            mod = 'moa.template.provider.%s' % pInfo['class']
            pMod =  __import__( mod, globals(), locals(), [mod], -1)

            #instantiate the class (mod.Mod())
            self.providers[pName] = getattr(pMod, pInfo['class'].capitalize())(pName, pInfo)
            _order.append((priority, pName))
            
        _order.sort()
        self.order = [x[1] for x in _order]

    def findProvider(self, tName, pName):
        """
        Get the proper provider given the system configuration, template
        name and the fromProvider request

        Tom made me write this: TOM

        :returns: instantiated provider class
        """
        if pName:
            return self.providers[pName]

        for pName in self.order:
            provider = self.providers[pName]
            if provider.hasTemplate(tName):
                return provider

        #nothing found
        return None

    def getTemplate(self, tName, pName = None):
        """
        Return the (Yaco) template object

        :param tName: Template name
        :param pName: The provider to get the template from - if not provider
          find the first provider that recognizes a template with this name 
        :returns: Yaco template object
        """
        provider = self.findProvider(tName, pName)
        
        if not provider:
            moa.ui.exitError("Cannot find provider for template %s.%s" % (
                provider, tName))
        return provider.getTemplate(tName)

    def templateList(self):
        rv = set()
        for pName in self.order:
            #print self.providers[pName].templateList()
            rv.update(set(self.providers[pName].templateList()))
        rv = list(rv)
        rv.sort()
        return rv

    def installTemplate(self, wd, tName, pName=None):

        p = self.findProvider(tName, pName)
        
        if not p:
            raise moa.exceptions.InvalidTemplate()
        
        p.installTemplate(wd, tName)

        templateddir = os.path.join(wd, '.moa', 'template.d')        
                    
        meta = p.getMeta()
        meta.name = tName
        meta.installed = datetime.datetime.now().isoformat()
        p.saveMeta(meta, templateddir)


#base class for all providers
class ProviderBase(object):
    def __init__(self, name, data={}):
        self.name = name
        self.data = data

    def getMeta(self):
        meta = Yaco.Yaco(self.data)
        meta.provider_type = self.__class__.__name__.lower()
        meta.provider = self.name
        return meta

    def saveMeta(self, meta, dir):
        if not os.path.exists(dir):
            os.makedirs(dir)

        meta.save(os.path.join(dir, 'meta'))
