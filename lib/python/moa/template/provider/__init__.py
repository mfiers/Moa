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

from moa.sysConf import sysConf

PROVIDERS = {}

def _getProviders():
    global PROVIDERS
    if PROVIDERS:
        return PROVIDERS
    
    for p in sysConf.template_providers:
        mod = 'moa.template.provider.%s' % p
        m =  __import__( mod, globals(), locals(), [p], -1)
        
        PROVIDERS[p] = m
        
    return PROVIDERS

def _getProvider(name, fromProvider):
    """
    Get the proper provider given the system configuration, template
    name and the fromProvider request

    TOM
    
    """
    providers = _getProviders()
    if fromProvider:
        return providers[fromProvider]
    else:
        for pn in sysConf.template_providers:
            p = providers[pn]
            if p.hasTemplate(name):
                return p
    return None

def getMoaFile(name, fromProvider = None):
    p = _getProvider(name, fromProvider)
    if not p:
        l.critical("cannot find provider for template %s.%s" % (
            fromProvider, name))
        sys.exit(-1)
    return p.getMoaFile(name)

def templateList():
    rv = set()
    for p in _getProviders().values():
        rv.update(set(p.templateList()))
    rv = list(rv)
    rv.sort()
    return rv

def installTemplate(wd, name, fromProvider=None):
    p = _getProvider(name, fromProvider)

    p.installTemplate(wd, name)
    
    meta = Yaco.Yaco()
    meta.source = name
    meta.provider = p.__name__.split('.')[-1]
    meta.installed = datetime.datetime.now().isoformat()
    meta.save(os.path.join(wd, '.moa', 'template.d', 'source'))

