# Copyright 2009-2011 Mark Fiers
# The New Zealand Institute for Plant & Food Research
# 
# This file is part of Moa - http://github.com/mfiers/Moa
# 
# Licensed under the GPL license (see 'COPYING')
# 
"""
**evernote** - Use evernote to store job results
------------------------------------------------

Use evernote to store a small message on job completion

Depends on an authenticated geeknote installation in the path. Moa
expects it to be aliased as `geeknote`

see:
http://www.geeknote.me/

"""

import os
import sys
import time
import socket
from datetime import datetime, timedelta
import subprocess as sp

import moa.logger 
l = moa.logger.getLogger(__name__)
import moa.ui

from moa.sysConf import sysConf

def niceRunTime(d):
    """
    Nice representation of the run time
    d is time duration string    
    """
    d = str(d)
    if ',' in d:
        days, time = d.split(',')
    else:
        days = 0
        time = d

    hours, minutes, seconds = time.split(':')
    hours, minutes = int(hours), int(minutes)
    seconds, miliseconds = seconds.split('.')
    seconds = int(seconds)
    miliseconds = int(miliseconds)
    
    if days > 0:
        if days == 1:            
            return "1 day, %d hrs" % hours
        else:
            return "%d days, %d hrs" % (days, hours)
        
    if hours == 0 and minutes == 0 and seconds == 0:
        return "<1 sec"
    if hours > 0:
        return "%d:%02d hrs" % (hours, minutes)
    elif minutes > 0:
        return "%d:%02d min" % (minutes, seconds)
    else:
        return "%d sec" % seconds

def hook_postRun():
    """
    Send a tweet out upon completing the default run
    """
    runtime =  datetime.today() - sysConf.logger.start_time    
    #print runtime
    #print timedelta(seconds=1)
    if timedelta(seconds=1) > runtime:
        # do not return anythin unless it ran for at least a certain
        # amount of time
        return 

    short_title = '%s/%s finished' % (
        socket.gethostname().split('.')[0],
        sysConf.job.wd.rsplit('/', 1)[-1])

    content = ['Moa job finished\n']
    content.append("    Run time: %s\n" % niceRunTime(runtime))
    content.append("    Host: %s\n" % socket.gethostname())
    content.append("    Wd: %s\n" % sysConf.job.wd)

    #fork - don't wait for this!
    pid = os.fork()
    if pid != 0: 
        return
    print short_title
    print "\n".join(content)
    #start geeknote process
    moa.ui.message('Sending message to evernote', store=False)
    cl = '%s create --title "%s" --content - --notebook Moa' % (
        sysConf.plugins.system.evernote.geeknote, short_title)
    print cl
    P = sp.Popen(cl, stdin=sp.PIPE, stdout=sp.PIPE, stderr=sp.PIPE, shell=True)

    o,e = P.communicate("\n".join(content))
    o = o.strip()
    e = e.strip()

    if o or e:
        with open('.moa/geeknote.log', 'a') as F:
            F.write("------\n%s\n%s\n" % (short_title, "\n".join(content)))
            if o:
                F.write('\n\nSTDOUT:\n')
                F.write(o)
            if e:
                F.write('\n\nSTDERR:\n')
                F.write(e)
    sys.exit(0)

