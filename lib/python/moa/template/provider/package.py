# Copyright 2009-2011 Mark Fiers
# The New Zealand Institute for Plant & Food Research
# 
# This file is part of Moa - http://github.com/mfiers/Moa
# 
# Licensed under the GPL license (see 'COPYING')
# 
"""
moa.provider.package
---------------------

Provides templates from the Moa package.

"""
import os
import shutil

import Yaco

from moa.sysConf import sysConf
import moa.utils
import moa.logger as l

import pkg_resources

TEMPLATEBASE = 'template2'

def hasTemplate(name):
    fname = os.path.join(TEMPLATEBASE, '%s.moa' % name)
    return moa.utils.resourceExists(fname)

def getMoaFile(name):
    fname = os.path.join(TEMPLATEBASE, '%s.moa' % name)
    return Yaco.Yaco(moa.utils.getResource(fname))
    
def templateList():
    """
    List all Moa package provided templates.

        >>> result = listAll()
        >>> len(result) > 0
        True
        >>> type(result) == type([])
        True

    @returns: a list of all templates included in the Moa package
    @rtype: a list of strings
    """
    
    r = []
    for f in moa.utils.listResource(TEMPLATEBASE):
        if f[-4:] != '.moa':
            continue
        name = f.replace(".moa", "")
        r.append(f[:-4])
    return r

    
def installTemplate(wd, name):
    """
    Install a template in the directory `wd`
    """
    moaFile = getMoaFile(name)
    extraFileDir = os.path.join(wd, '.moa', 'template.d')
    
    if os.path.isdir(extraFileDir):
        shutil.rmtree(extraFileDir)
    os.makedirs(extraFileDir)

    #print type(moaFile)
    moaFile.save(os.path.join(wd, '.moa', 'template'))

    for f in moa.utils.listResource(TEMPLATEBASE):
        if not f.find(name) == 0: continue
        if f[-1] in ['~', '#']: continue
        if f[-4:] == '.moa': continue
        with open(os.path.join(wd, '.moa', 'template.d', f), 'w') as F:
            F.write(moa.utils.getResource(os.path.join(TEMPLATEBASE, f)))
    
