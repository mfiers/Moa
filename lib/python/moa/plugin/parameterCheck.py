import os
import sys
import moa.ui

import moa.logger as l

def defineCommands(data):
    """
    Define the parameters test commands
    """
    data['commands']['test'] = {
        'desc' : 'Test the currennt configuration',
        'call' : test_ui,
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
    
def preRun(data):
    test_ui(data)

def promptSnippet(data):
    """
    Function used by the prompt plugin to generate snippets for inlusion 
    in the prompt
    """  
    m = test(data)
    print m
    if m: 
        return "{{red}}X{{reset}}"
    else:
        return "{{green}}o{{reset}}"
    
    
def test_ui(data):
    
    options = data['options']
    messages = test(data)
    
    for message, detail in messages:
        errorMessage(message, detail)
    
    if messages and not options.force:
        sys.exit(-1)
    
    
def test(data):
    job = data['job']
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
