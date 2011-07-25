# Copyright 2009-2011 Mark Fiers
# The New Zealand Institute for Plant & Food Research
# 
# This file is part of Moa - http://github.com/mfiers/Moa
# 
# Licensed under the GPL license (see 'COPYING')
# 
"""
moa.template
------------

Store information on a template. This module is also responsible for
retrieving template information.

"""

import os
import shutil
import datetime

import Yaco

import moa.ui
import moa.utils
import moa.logger as l

from moa.template import provider
from moa.template.template import Template

PROVIDERS = provider.Providers()


def getMoaFile(name):
    return PROVIDERS.getTemplate(name)
    
def templateList():
    x = PROVIDERS.templateList()
    return x

def installTemplate(wd, tName, provider=None):
    """
    Initialize the template - this means - try to figure out where the
    template came from & copy the template files into
    `job/.moa/template` & `job/.moa/template.d/extra`.

    Currently all templates come from the moa repository. In the
    future, multiple sources must be possible

    >>> import tempfile
    >>> wd = tempfile.mkdtemp()
    >>> installTemplate(wd, 'adhoc')
    >>> templateFile = os.path.join(wd, '.moa', 'template')
    >>> adhocFile = os.path.join(wd, '.moa', 'template.d', 'adhoc.mk')
    >>> assert(os.path.exists(templateFile))
    >>> assert(os.path.exists(adhocFile))
    """
    PROVIDERS.installTemplate(wd, tName, provider)
        
             
def initTemplate(*args, **kwargs):
    """
    
    """
    l.warning("Deprecated call")
    installTemplate(*args, **kwargs)

def refresh(wd):
    """
    Refresh the template - try to find out what the template is from 
    {{wd}}/.moa/template.d/meta. If that doesn't work, revert to the 
    default template. If default is not specified - exit with an error

    >>> import tempfile
    >>> wd = tempfile.mkdtemp()
    >>> installTemplate(wd, 'adhoc')
    >>> templateFile = os.path.join(wd, '.moa', 'template')
    >>> adhocFile = os.path.join(wd, '.moa', 'template.d', 'adhoc.mk')
    >>> os.unlink(adhocFile)    
    >>> os.unlink(templateFile)
    >>> assert(not os.path.exists(templateFile))
    >>> assert(not os.path.exists(adhocFile))
    >>> refresh(wd)
    >>> assert(os.path.exists(templateFile))
    >>> assert(os.path.exists(adhocFile))
    
    """
    meta = Yaco.Yaco()
    metaFile = os.path.join(wd, '.moa', 'template.d', 'meta')
    l.debug("loading metafile from %s" % metaFile)
    try:
        meta.load(metaFile)
    except (IOError):
        oldMetaFile = os.path.join(wd, '.moa', 'template.d', 'source')
        if os.path.exists(oldMetaFile):
            shutil.move(oldMetaFile, metaFile)
            meta.load(metaFile)
        else:
            l.critical("no template to refresh found in %s" % wd)
            pass

    if not meta.name and meta.source:
        #old style 
        meta.name = meta.source
        
    if not meta.name:        
        moa.ui.exitError("Cannot refresh this job")

    l.debug("install template in %s" % wd)
    l.debug("template name  %s" % meta.name)
    l.debug("from provider %s" % provider)
    
    installTemplate(wd,
                    tName = meta.name,
                    provider=meta.get('provider', None))
    
