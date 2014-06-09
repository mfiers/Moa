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
import logging
from datetime import datetime

import moa.job
import moa.utils
import moa.logger as l
import moa.args
import moa.plugin
from moa.sysConf import sysConf


def hook_prepare_3():
    sysConf.logger.start_time = datetime.today()


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
            return "%s days, %d hrs" % (days, hours)

    if hours == 0 and minutes == 0 and seconds == 0:
        return "<1 sec"
    if hours > 0:
        return "%d:%02d hrs" % (hours, minutes)
    elif minutes > 0:
        return "%d:%02d min" % (minutes, seconds)
    else:
        return "%d sec" % seconds


def hook_post_interrupt():
    _writeLog('interrupted')


def hook_post_error():
    _writeLog('error')


def hook_postRun():
    _writeLog('ok')


def hook_postNew():
    _writeLog('new')


def hook_postCp():
    _writeLog('cp')


def hook_postMv():
    _writeLog('mv')


def hook_postLock():
    _writeLog('lock')


def hook_postUnlock():
    _writeLog('unlock')


def hook_preRun():
    _writeLog('start')


def _writeLog(status):

    #only save logs for moa jobs
    if (not sysConf) or \
       (not 'job' in sysConf) or \
       (not sysConf.job.isMoa()):
        return

    sysConf.logger.end_time = datetime.today()
    if sysConf.logger.start_time:
        sysConf.logger.run_time = \
            sysConf.logger.end_time - sysConf.logger.start_time
    else:
        sysConf.logger.start_time = 0

    runtime = sysConf.logger.end_time - sysConf.logger.start_time
    sysConf.logger.niceRunTime = niceRunTime(runtime)

    logFile = os.path.join(sysConf.job.confDir, 'log')
    #logFile2 = os.path.join(sysConf.job.confDir, 'log.d',
    #                        'log.%d' % sysConf.runId)

    commandInfo = {}
    logLevel = logging.INFO
    if sysConf.originalCommand in sysConf.commands.keys():
        commandInfo = sysConf.commands[sysConf.originalCommand]
        logLevel = commandInfo.get('logLevel', logging.DEBUG)
    l.debug("Logging %s" % sysConf.originalCommand)
    command = " ".join(" ".join(sys.argv).split())

    if sysConf.logger.run_time:
        runtime = sysConf.logger.run_time
    else:
        runtime = 0

    sysConf.logger.logLevel = logLevel
    sysConf.logger.status = status
    sysConf.logger.full_command = command
    sysConf.logger.moa_command = sysConf.originalCommand
    sysConf.pluginHandler.run('logMessage')

    #sysConf.logger.save(logFile2)
    with open(logFile, 'a') as F:
        F.write("%s\n" % "\t".join([
            status, str(sysConf.originalCommand),
            str(logLevel),
            sysConf.logger.start_time.strftime("%Y-%m-%dT%H:%M:%S.%f"),
            sysConf.logger.end_time.strftime("%Y-%m-%dT%H:%M:%S.%f"),
            str(runtime), command
        ]))


def hook_finish():
    #and - probably not the location to do this, but print something to screen
    #as well
    if sysConf.options.background:
        return
    if sysConf.originalCommand == 'run':
        if sysConf.rc == 0:
            moa.ui.exit('{{bold}}Success{{reset}} executing "%s" (%s)' % (
                sysConf.originalCommand,
                niceRunTime(str(sysConf.logger.run_time))))


def hook_pelican():
    l.debug("logger pelican hook")
    return
    l.debug("pelican versioning output")
    nov = 10
    last_run_id, vinfo = _get_last_versioninfo(nov)
    vrange = list(reversed(sorted(range(last_run_id, last_run_id - nov, -1))))
    if last_run_id == 0 or vinfo == {}:
        l.warning("cannot create version info page")
        return

    allkeys = set()
    for rid in vinfo:
        allkeys.update(set(vinfo[rid]))
    allkeys = sorted(list(allkeys))

    jenv = sysConf.plugins.pelican.jenv
    jtemplate = jenv.select_template(['versioning.page.jinja2'])
    with open('./doc/pages/version.md', 'w') as F:
        F.write(jtemplate.render({
            'last_run_id': last_run_id,
            'vrange': vrange,
            'allkeys': allkeys,
            'vinfo': vinfo}))


def _getLog(job, noLines=10):
    """
    Retrieve the last noLines of the log file

    :param noLines: no of lines to retrieve
    :type noLines: int
    """

    logFile = os.path.join(job.confDir, 'log')

    moa.utils.moaDirOrExit(job)
    if not os.path.exists(logFile):
        moa.ui.exit("No logs found")

    rv = []
    with open(logFile) as F:
        #read the last 2k - prevent reading the whole file
        try:
            F.seek(-1 * noLines * 250, 2)
        except IOError:
            F.seek(0)
        F.readline()
        lines = F.readlines()[-1 * noLines:]
        for line in lines:
            ls = line.split("\t")

            def _isInteger(_s):
                try:
                    int(_s)
                    return True
                except:
                    return False

            if (len(ls) != 7) or \
               (_isInteger(ls[0])) or \
               (not _isInteger(ls[2])):

                continue

            rv.append(line.split("\t"))
    return rv

@moa.args.needsJob
@moa.args.command
def log(job, args):
    """
    Show activity log

    Shows a log of moa commands executed. Only commands with an impact
    on the pipeline are logged, such as `moa run` & `moa set`.
    """
    for logRec in _getLog(job, 10):
        status, command, logLevel, start, stop, delta, command = logRec

        logLevel = int(logLevel)
        if status == 'ok':
            lc = '{{bold}}{{green}}Success {{reset}}'
        elif status == 'error':
            lc = "{{bold}}{{red}}Error   {{reset}}"
        else:
            lc = "{{blue}}%-8s{{reset}}" % status[:7].capitalize()

        lc += "%s " % start.rsplit(':', 1)[0]
        lc += "%10s " % niceRunTime(delta)
        lc += command
        moa.ui.fprint(lc, f='jinja')
