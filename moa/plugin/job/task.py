# Copyright 2009-2011 Mark Fiers
# The New Zealand Institute for Plant & Food Research
#
# This file is part of Moa - http://github.com/mfiers/Moa
#
# Licensed under the GPL license (see 'COPYING')
#
"""
**task** - integrate taskwarrior to track running tasks
-------------------------------------------------------

You will need to have taskwarrior installed.

"""

import re
import json
import socket
import subprocess as sp

import moa.ui
import moa.logger
from moa.sysConf import sysConf

l = moa.logger.getLogger(__name__)


def runTask(cl):
    l.warning("Executing task: %s" % cl)
    sp.call(cl.split(), stdout=sp.PIPE, stderr=sp.PIPE)


def _getTaskId(job):
    #find the task
    uid = '%s-%s' % (job.conf.ppud, job.conf.pud)
    cl = ['task', 'export']
    P = sp.Popen(cl, stdout=sp.PIPE, stderr=sp.PIPE)
    out, err = P.communicate()
    data = json.loads('[' + out + ']')
    import pprint
    for item in data:
        annotations = item.get('annotations', [])

        for anno in annotations:
            desc = anno.get('description', '')
            if not 'uid:' in desc:
                continue

            pprint.pprint(anno)
            print 'd', desc
            print

    import sys
    sys.exit()
    pidlist = out.strip().split()
    if len(pidlist) > 1:
        moa.ui.warn("multiple jobs with the warn")
        return pidlist[-1]

    if len(pidlist) == 1:
        return pidlist[0]

    project = job.conf.get('project', 'no_project')
    title = job.conf.get('title')

    cl = ['task', 'add',
          'project:"%s"' % project,
          '+moa', '--', title]

    P = sp.Popen(cl, stdout=sp.PIPE, stderr=sp.PIPE)
    out, err = P.communicate()
    taskid = re.search('Created task ([0-9]+)', out).groups()[0]
    moa.ui.message("new taskwarrior task %s" % taskid)

    runTask("task %s annotate uid:%s-%s" % (taskid, job.conf.ppud,
                                            job.conf.pud))

    sysConf.plugins.task.id = taskid
    return taskid


def hook_pre_run(job):

    taskid = _getTaskId(job)
    moa.ui.message("TaskId %s" % taskid)
    hostname = socket.gethostname()

    runTask("task %s modify +moa +%s" % (taskid, hostname))
    runTask("task %s start" % (taskid))


def hook_finish(job):
    """
    cache!!
    """
    #print job, job.isMoa()rm
    taskid = sysConf.plugins.task.id
    runTask("task %s done" % (taskid))


def hook_post_error(job):
    """
    post error - problem!
    """
    #print job, job.isMoa()rm
    taskid = sysConf.plugins.task.id
    runTask("task %s stop" % (taskid))
    runTask("task %s modify +error Error executing this job" % (taskid))
    runTask("task %s modify priority:H" % (taskid))
