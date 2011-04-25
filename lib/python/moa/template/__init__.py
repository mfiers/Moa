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
import datetime

import Yaco

import moa.ui
import moa.utils
import moa.logger as l

import moa.template.provider
from moa.template.template import Template

class InvalidTemplate(Exception):
    """ Invalid Template """
    pass

def getMoaFile(name):
    return moa.template.provider.getMoaFile(name)
    
def templateList():
    return moa.template.provider.templateList()

def installTemplate(wd, name, fromProvider=None):
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
    moa.template.provider.installTemplate(wd, name, fromProvider)
            
 
def initTemplate(*args, **kwargs):
    """
    
    """
    l.warning("Deprecated call")
    installTemplate(*args, **kwargs)

def refresh(wd):
    """
    Refresh the template - try to find out what the template is from 
    {{wd}}/.moa/template.d/source. If that doesn't work, revert to the 
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
    try:
        meta.load(os.path.join(wd, '.moa', 'template.d', 'source'))
    except (IOError):
        l.critical("no template to refresh found in %s" % wd)
        pass

    if not meta.source:
        moa.ui.exitError("Cannot refresh this job")

    provider = meta.get('provider', None)
    installTemplate(wd, name = meta.source,
                    fromProvider=provider)
    