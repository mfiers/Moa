# Copyright 2009-2011 Mark Fiers
# The New Zealand Institute for Plant & Food Research
# 
# This file is part of Moa - http://github.com/mfiers/Moa
# 
# Licensed under the GPL license (see 'COPYING')
# 
"""
**parameterCheck** - check parameters
-------------------------------------
"""

import os
import sys
import moa.ui
from moa.sysConf import sysConf

def hook_defineCommands():
    """
    Define the parameters test commands
    """
    sysConf['commands']['test'] = {
        'desc' : 'Test the currennt configuration',
        'call' : test_ui
        }

    
def errorMessage(message, details):
    moa.ui.fprint("%%(bold)s%%(red)sError%%(reset)s: %%(bold)s%s%%(reset)s: %s" % (
        message, details))


def _isInteger(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

def _isFloat(s):
    try:
        float(s)
        return True
    except ValueError:
        return False
    
def hook_preRun():
    test_ui()

def hook_promptSnippet():
    """
    Function used by the prompt plugin to generate snippets for inlusion 
    in the prompt
    """  
    m = test()
    if m: 
        return "{{red}}X{{reset}}"
    else:
        return "{{green}}o{{reset}}"
    
    
def test_ui():
    
    options = sysConf['options']
    messages = test()
    
    for message, detail in messages:
        errorMessage(message, detail)
    
    if messages and not options.force:
        sysConf.pluginHandler.run('postError')
        moa.ui.exitError("exitting")
    
def test():
    job = sysConf['job']
    if not job.isMoa():
        moa.utils.moaDirOrExit(job)
        
    messages = []
    for p in job.conf.keys():
        if p in job.conf.doNotCheck:
            continue
        
        if not p in job.template.parameters:
            continue
        
        pt = job.template.parameters[p]
        if not pt.optional and not job.conf[p]:
            messages.append(("Undefined variable", p))
        elif pt.type == 'file' \
               and job.conf[p] \
               and not os.path.isfile(job.conf[p]):
            messages.append(("Not a file",
                             "%s=%s " % (p, job.conf[p])))
        elif pt.type == 'directory' \
               and job.conf[p] \
               and not os.path.isdir(job.conf[p]):
            messages.append(("Not a directory",
                             "%s=%s " % ( p, job.conf[p])))
        elif pt.type == 'integer' \
               and job.conf[p] \
               and not _isInteger(job.conf[p]):
            messages.append(("Not an integer",
                             "%s=%s " % (p, job.conf[p])))
        elif pt.type == 'float' \
               and job.conf[p] \
               and not _isFloat(job.conf[p]):
            messages.append(("Not a float",
                             "%s=%s " % (p, job.conf[p])))
            
    return messages
