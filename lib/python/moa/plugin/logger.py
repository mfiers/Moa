# Copyright 2009-2011 Mark Fiers
# The New Zealand Institute for Plant & Food Research
# 
# This file is part of Moa - http://github.com/mfiers/Moa
# 
# Licensed under the GPL license (see 'COPYING')
# 
"""
**logger** - Log Moa activity
-----------------------------
"""

import os
import sys
from datetime import datetime

import moa.job
import moa.logger as l
import moa.plugin

def defineCommands(data):
    data['commands']['log'] = { 
        'desc' : 'Show the logs for this job',
        'call' : showLog,
        'log' : False
        }

def prepare(data):
    data.logger.start_time = datetime.today()

def niceRunTime(d):
    """
    Nice representation of the run time
    d is time duration string    
    """
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

def postInterrupt(data):
    return postCommand(data)
def postCommand(data):
    data.logger.end_time = datetime.today()
    data.logger.run_time = data.logger.end_time - data.logger.start_time
    runtime = data.logger.end_time - data.logger.start_time
    data.runtime = str(runtime)
    logFile = os.path.join(data.job.confDir, 'log')
    if not os.path.exists(data.job.confDir):
        return
    commandInfo = {}
    if data.originalCommand in data.commands.keys():
        commandInfo = data.commands[data.originalCommand]
    if commandInfo.get('log', True):
        l.debug("Logging %s" % data.originalCommand)
        with open(logFile, 'a') as F:
            F.write("%s\n" % "\t".join([
                str(data.rc),
                ",".join(data.executeCommand),
                data.logger.start_time.strftime("%Y-%m-%dT%H:%M:%S.%f"),
                data.logger.end_time.strftime("%Y-%m-%dT%H:%M:%S.%f"),
                str(data.runtime),
                " ".join(sys.argv)
                ]))

    #and - probably not the location to do this, but print something to screen
    #as well
    if data.options.background:
        return
    if data.originalCommand == 'run':
        if data.rc == 0:
            moa.ui.fprint("Moa {{green}}Success{{reset}} running %s  (%s)" % (
                data.originalCommand,
                niceRunTime(str(data.runtime))), f='jinja')
        else:
            moa.ui.fprint("Moa {{red}}Error{{reset}} running %s  (%s)" % (
                data.originalCommand,
                niceRunTime(str(data.runtime))), f='jinja')
        
                      
def showLog(data):
    """
    **moa log** - show a log of the most recent moa calls

    Usage::

        moa log [LINES]

    Shows a log of moa commands executed. Only commands with an impact
    on the pipeline are logged, such as `moa run` & `moa set`. The
    number of log entries to display can be controlled with the
    optional LINES parameter.    
    """
    args = data.args
    if len(args) > 1:
        noLines = int(args[1])
    else:
        noLines = 5
        
    logFile = os.path.join(data.job.confDir, 'log')
    with open(logFile) as F:
        #read the last 2k - prevent reading the whole file
        try:
            F.seek(-1 * noLines * 250, 2)
        except IOError:
            F.seek(0)
        F.readline()
        lines = F.readlines()[-1 * noLines:]
        for line in lines:
            rc, command, start, stop, delta, command = \
                line.split("\t")
            lc = "%s - " % start.rsplit(':',1)[0]
            if int(rc) == 0:
                lc += "{{bold}}{{green}}Success {{reset}}"
            else:
                lc += "{{bold}}{{red}}%-8s{{reset}}" % ("Err " + str(rc))

            lc += " - %10s" % niceRunTime(delta)
            lc += " - " + command
            moa.ui.fprint(lc, f='jinja')
