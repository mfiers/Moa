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
        'call' : test,
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

#def postSet(data):
#    test(data)
    
def preRun(data):
    return test(data)

def test(data):
    job = data['job']
    if not job.isMoa():
        moa.utils.moaDirOrExit(job)
        
    options = data['options']
    error = False
    for p in job.conf.keys():
        if p in job.conf.doNotCheck:
            continue
        if not p in job.template.parameters:
            continue
        pt = job.template.parameters[p]
        if not pt.optional and not job.conf[p]:
            errorMessage("Undefined variable", p)
            error = True
        elif pt.type == 'file' \
               and job.conf[p] \
               and not os.path.isfile(job.conf[p]):
            errorMessage("Not a file",
                         "%s=%s " % (
                p, job.conf[p]))
            error = True
        elif pt.type == 'directory' \
               and job.conf[p] \
               and not os.path.isdir(job.conf[p]):
            errorMessage("Not a directory",
                         "%s=%s " % (
                p, job.conf[p]))
            error = True
        elif pt.type == 'integer' \
               and job.conf[p] \
               and not _isInteger(job.conf[p]):
            errorMessage("Not an integer",
                         "%s=%s " % (
                p, job.conf[p]))
            error = True
        elif pt.type == 'float' \
               and job.conf[p] \
               and not _isFloat(job.conf[p]):
            errorMessage("Not a float",
                         "%s=%s " % (
                p, job.conf[p]))
            error = True

    if not options.force and error:
        sys.exit(-1)
