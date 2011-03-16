# Copyright 2009-2011 Mark Fiers
# The New Zealand Institute for Plant & Food Research
# 
# This file is part of Moa - http://github.com/mfiers/Moa
# 
# Licensed under the GPL license (see 'COPYING')
# 
"""
**prompt** - Moa BASH prompt enhancer
-------------------------------------
"""

import signal

import moa.utils    
import moa.ui

order = 10

def defineCommands(data):
    """
    Set the moa commands for this plugin
    """
    data['commands']['prompt'] = {
        'desc' : 'Show the state of the current job',
        'private' : True,
        'call' : prompt,
        }
    

class TimeOutException(Exception):
    pass

def timeOutHandler(signum, frame):
    raise TimeOutException()


        
def prompt(data):
    job = data['job']
    template = job.template.name

    #set a signal to prevent this routine from running for more 
    # than 0.5 seconds
    signal.signal(signal.SIGALRM, timeOutHandler)
    signal.setitimer(signal.ITIMER_REAL, 0.5)
    
    #see if the parameter check is available & loaded
    rv = {}
    try:
        rv = data['plugins'].run('promptSnippet')
    except TimeOutException:
        pass
    signal.setitimer(signal.ITIMER_REAL, 0)
        

    message = "moa|{{green}}%s{{reset}}|" % ( template)
    if rv:
        snip = ''
        kys = rv.keys()
        kys.sort()
        for k in kys:
            snip += (rv[k])
        message += snip + "|"
    moa.ui.fprint(message, f='jinja', newline=False, ansi=True)
    
    
    
    
