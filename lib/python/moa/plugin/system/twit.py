# Copyright 2009-2011 Mark Fiers
# The New Zealand Institute for Plant & Food Research
# 
# This file is part of Moa - http://github.com/mfiers/Moa
# 
# Licensed under the GPL license (see 'COPYING')
# 
"""
**twit** - Tweet results
------------------------

Use twitter to send a message upon job completion

Depends on an configured TTYter installation in the path.
see: http://www.floodgap.com/software/ttytter/

"""

import os
import time
import socket
from datetime import datetime, timedelta
import subprocess as sp

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
    if timedelta(seconds=sysConf.plugins.system.twit.mintime) > runtime:
        # do not return anythin unless it ran for at least a certain
        # amount of time
        return 

    message = '\dm %s moa job in %s:%s finished in %s' % (
        sysConf.plugins.system.twit.username,
        socket.gethostname().split('.')[0],
        sysConf.job.wd,
        niceRunTime(runtime))
    
    #start TTYter process
    P = sp.Popen(['ttytter', '-script'], stdin=sp.PIPE)
    P.communicate(message)

