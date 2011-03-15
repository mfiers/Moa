# 
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
**prompt** - Moa BASH prompt enhancer
-------------------------------------
"""
import os

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
    moacol  = '{{yellow}}'
    
    #set a signal to prevent this routine from running for more 
    # than 0.5 seconds
    signal.signal(signal.SIGALRM, timeOutHandler)
    signal.setitimer(signal.ITIMER_REAL, 0.5)
    
    prompt_snippet = ''    
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
    
    
    
    
