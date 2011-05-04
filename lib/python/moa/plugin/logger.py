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
from moa.sysConf import sysConf

def defineCommands(data):
    data['commands']['log'] = { 
        'desc' : 'Show the logs for this job',
        'call' : showLog,
        'log' : False
        }

def prepareCommand(data):
    moa.ui.message('Start "%s"' % sysConf.originalCommand)
    
def prepare_background(data):
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
    _writeLog(data)

def postError(data):
    _writeLog(data)

def _writeLog(data=None):
    
    sysConf.logger.end_time = datetime.today()
    sysConf.logger.run_time = sysConf.logger.end_time - sysConf.logger.start_time
    runtime = sysConf.logger.end_time - sysConf.logger.start_time
    sysConf.runtime = str(runtime)
    logFile = os.path.join(sysConf.job.confDir, 'log')
    if not os.path.exists(sysConf.job.confDir):
        return
    commandInfo = {}
    if sysConf.originalCommand in sysConf.commands.keys():
        commandInfo = sysConf.commands[sysConf.originalCommand]

    l.debug("Logging %s" % sysConf.originalCommand)
    command = " ".join(" ".join(sys.argv).split())

    with open(logFile, 'a') as F:
        F.write("%s\n" % "\t".join([
            str(sysConf.rc),
            ",".join(sysConf.executeCommand),
            sysConf.logger.start_time.strftime("%Y-%m-%dT%H:%M:%S.%f"),
            sysConf.logger.end_time.strftime("%Y-%m-%dT%H:%M:%S.%f"),
            str(sysConf.runtime), command
            ]))

def finish(data):
    _writeLog(data)
    #and - probably not the location to do this, but print something to screen
    #as well
    if sysConf.options.background:
        return
    if sysConf.originalCommand == 'run':
        if sysConf.rc == 0:
            moa.ui.message('{{bold}}Success{{reset}} executing "%s" (%s)' % (
                sysConf.originalCommand,
                niceRunTime(str(sysConf.runtime))))
        else:
            moa.ui.message("{{red}}{{bold}}Error{{reset}} running %s  (%s)" % (
                sysConf.originalCommand,
                niceRunTime(str(sysConf.runtime))))
        
                      
def showLog(job):
    """
    **moa log** - show a log of the most recent moa calls

    Usage::

        moa log [LINES]

    Shows a log of moa commands executed. Only commands with an impact
    on the pipeline are logged, such as `moa run` & `moa set`. The
    number of log entries to display can be controlled with the
    optional LINES parameter.    
    """
    args = sysConf.args
    if len(args) > 1:
        noLines = int(args[1])
    else:
        noLines = 5
        
    logFile = os.path.join(job.confDir, 'log')
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
