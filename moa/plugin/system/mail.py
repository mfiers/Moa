# Copyright 2013 Mark Fiers
#
# This file is part of Moa - http://github.com/mfiers/Moa
#
# Licensed under the GPL license (see 'COPYING')
#
"""
**mail** - Tweet results
------------------------

Use mailer to send a message upon job completion

Depends on a working "mail" command in the path.
"""

import os
import sys
import time
import getpass
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

def hook_logMessage():
    """
    Send a mail out upon completing the default run
    """
    runtime =  datetime.today() - sysConf.logger.start_time

    recipient=sysConf.plugins.system.mail.recipient

    if timedelta(seconds=sysConf.plugins.system.mail.mintime) > runtime:
        # do not return anythin unless it ran for at least a certain
        # amount of time
        return

    #fork - don't wait for this!
    pid = os.fork()
    if pid != 0:
        moa.ui.message("Sending email", store=False)
        return

    template = sysConf.job.template.get('name', "")
    title = sysConf.job.conf.getRendered('title')

    content = ['Moa job finished\n']
    content.append("    Run time: %s" % niceRunTime(runtime))
    content.append("    Template: %s" % template)
    content.append("      Status: %s" % sysConf.logger.status)
    content.append("        User: %s" % getpass.getuser())
    content.append("       Title: %s" % title)
    content.append("          Wd: %s" % sysConf.job.wd)
    content.append("        Host: %s" % (socket.gethostname()))
    content.append("     Command: %s" % sysConf.logger.moa_command)
    content.append("    Full Cmd: %s" % sysConf.logger.full_command)
    content.append("   Job start: %s" %
            sysConf.logger.start_time.strftime("%Y-%m-%d %H:%M:%S"))
    content.append("     Job end: %s" %
            sysConf.logger.end_time.strftime("%Y-%m-%d %H:%M:%S"))

    # Add configuration
    content.append("\nConfiguration:\n")

    conf = sysConf.job.conf.render()
    ckeys = sorted(conf.keys())

    for p in ckeys:
        if p[0] == '_': continue
        if p[:4] == 'moa_': continue
        if sysConf.job.conf.isPrivate(p): continue
        content.append("%12s: %s" % (p, conf[p]))

    content = "\n".join(content)
    subject = 'Moa job %s in %s|%s (%s)' % (
        sysConf.logger.status,
        socket.gethostname().split('.')[0],
        sysConf.job.wd.rsplit('/',1)[-1],
        niceRunTime(runtime))

    #start mail process
    #moa.ui.message('Sending email message to %s' % recipient,
    #    store=False)

    cl = 'mail -s "%s" %s' % (subject, recipient)
    #moa.ui.message('cl: %s' % str(cl), store=False)

    P = sp.Popen(cl, stdin=sp.PIPE, stdout=sp.PIPE, stderr=sp.PIPE, shell=True)

    #moa.ui.message('Subject ' + subject)
    o,e = P.communicate(content)

    with open('.moa/mailto.log', 'a') as F:
        F.write("\n%s\n%s\n" % ('-'*90, subject))
        F.write(content + "\n")
        if o.strip():
            F.write('\noutput:\n')
            F.write(o)
        if e.strip():
            F.write('\n\nerror:\n')
            F.write(e)
        F.write("%s\n" % ("=" * 90))
    sys.exit(0)

