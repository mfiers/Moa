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
import getpass
import socket
from datetime import datetime, timedelta

import moa.logger
l = moa.logger.getLogger(__name__)
import moa.ui
import moa.utils

from moa.sysConf import sysConf


def get_core_message(job):

    template = sysConf.job.template.get('name', "")
    title = sysConf.job.conf.getRendered('title')

    content = ['Moa job finished\n']
    content.append("    Run time: %(runtime)s")
    content.append("    Template: %s" % template)
    content.append("      Status: %(status)s")
    content.append("        User: %s" % getpass.getuser())
    content.append("       Title: %s" % title)
    content.append("          Wd: %s" % job.wd)
    content.append("        Host: %s" % (socket.gethostname()))
    content.append("     Command: %s" % sysConf.logger.moa_command)
    content.append("    Full Cmd: %s" % sysConf.logger.full_command)
    content.append("   Job start: %s" %
                   sysConf.logger.start_time.strftime("%Y-%m-%d %H:%M:%S"))
    content.append("     Job end: %%(jobend)s")

    # Add configuration
    content.append("\nConfiguration:\n")

    conf = job.conf.render()
    ckeys = sorted(conf.keys())

    for p in ckeys:
        if p[0] == '_':
            continue
        if p[:4] == 'moa_': continue
        if job.conf.isPrivate(p):
            continue
        content.append("%12s: %s" % (p, conf[p]))

    content = "\n".join(content)
    return content


def hook_async_exit():
    print 'async'
    pass


def hook_logMessage():
    """
    Send a mail out upon completing the default run
    """
    runtime = datetime.today() - sysConf.logger.start_time
    status =  sysConf.logger.status
    if status == 'start':
        #no messages when startin!
        return

    recipient = sysConf.plugins.system.mail.recipient
    sender = sysConf.plugins.system.mail.sender
    smtp = sysConf.plugins.system.mail.smtp

    if timedelta(seconds=sysConf.plugins.system.mail.mintime) > runtime:
        # do not return anythin unless it ran for at least a certain
        # amount of time
        return

    # fork - don't wait for this!
    pid = os.fork()

    if pid != 0:
        moa.ui.message("Sending email", store=False)
        return

    content = get_core_message(sysConf.job)
    content = content % {
        'status': sysConf.logger.status,
        'runtime': moa.utils.niceRunTime(runtime),
        'jobend': sysConf.logger.end_time.strftime("%Y-%m-%d %H:%M:%S"),
    }

    subject = 'Moa job %s in %s|%s (%s)' % (
        sysConf.logger.status,
        socket.gethostname().split('.')[0],
        sysConf.job.wd.rsplit('/', 1)[-1],
        moa.utils.niceRunTime(runtime))

    # start mail process
    moa.utils.sendmail(sysConf.plugins.system.mail.smtp, sender,
                       recipient, subject, content)

    sys.exit(0)  # this was a fork, remember!

    # P = sp.Popen(cl, stdin=sp.PIPE, stdout=sp.PIPE, stderr=sp.PIPE,
    # shell=True)

    # moa.ui.message('Subject ' + subject)
    # o, e = P.communicate(content)

    # with open('.moa/mailto.log', 'a') as F:
    #     F.write("\n%s\n%s\n" % ('-' * 90, subject))
    #     F.write(content + "\n")
    #     if o.strip():
    #         F.write('\noutput:\n')
    #         F.write(o)
    #     if e.strip():
    #         F.write('\n\nerror:\n')
    #         F.write(e)
    #     F.write("%s\n" % ("=" * 90))
    # sys.exit(0)
