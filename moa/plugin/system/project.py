# Copyright 2009-2011 Mark Fiers
# The New Zealand Institute for Plant & Food Research
#
# This file is part of Moa - http://github.com/mfiers/Moa
#
# Licensed under the GPL license (see 'COPYING')
#
"""
**project** - Simple plugin to ease maintaining project data
------------------------------------------------------------

Have more plans for this plugin - but for now it defines the following
two variables to use in the job configuration

* _p : directory of the parent project
* project: the 'title' varialbe of the first parent project

"""
import os
import re

import lockfile
import random

import Yaco
from moa.sysConf import sysConf
import moa.logger
l = moa.logger.getLogger(__name__)


def baseN(num, b, numerals="0123456789abcdefghijklmnopqrstuvwxyz"):
    """see: http://code.activestate.com/recipes/65212/
    """
    return ((num == 0) and numerals[0]) or \
        (baseN(num // b, b, numerals).lstrip(numerals[0])
         + numerals[num % b])


def _generateCandidatePud():
    return baseN(random.randint(36 ** 4, 36 ** 5 - 1), 36)


def _getUniqueId(project_dir):
    pud_file = os.path.join(project_dir, '.moa', 'project_uid')
    puds = []

    if not os.path.exists(pud_file):
        #touch a new file - if necessary
        with open(pud_file, 'w') as F:
            pass

    with lockfile.FileLock(pud_file):
        if os.path.exists(pud_file):
            with open(pud_file) as F:
                puds = F.read().strip().split()

        pud_candidate = _generateCandidatePud()
        while pud_candidate in puds:
            pud_candidate = _generateCandidatePud()

        puds.append(pud_candidate)
        with open(pud_file, 'w') as F:
            F.write("\n".join(puds))
    return pud_candidate


def hook_postNew():
    """Handle all git changes post New - if this is a project - add a pud
    """

    # was a 'project' created? If not return
    if sysConf.job.template.name != 'project':
        return

    if not sysConf.job.conf.get('pud'):
        sysConf.job.conf['pud'] = _getUniqueId(sysConf.job.wd)
        sysConf.job.conf.save()


def hook_prepare_3():

    #see if we can find a project directory -
    job = sysConf.job

    job.template.parameters.pud = {
        'optional': True,
        'help': 'A unique job identifier - only unique in ' +
                'the context of this job',
        'recursive': False,
        'private': True,
        'type': 'string'
    }

    job.template.parameters.ppud = {
        'optional': True,
        'help': 'A unique project job identifier - only unique in ' +
                'the context of this job',
        'recursive': False,
        'private': True,
        'type': 'string'
    }

    lookat = os.path.abspath(sysConf.job.wd)
    while True:

        if lookat == '/':
            moa.ui.warn("No project found")
            break

        templateFile = os.path.join(lookat, '.moa', 'template')
        if not os.path.exists(templateFile):
            lookat = os.path.dirname(lookat)
            continue

        td = Yaco.Yaco()
        td.load(templateFile)

        if td.moa_id != 'project':
            lookat = os.path.dirname(lookat)
            continue

        #found project!
        project_dir = lookat
        l.debug("found project at %s" % project_dir)

        job.conf.setPrivateVar('__project', project_dir)
        job.conf.setPrivateVar(
            '_project',
            re.sub("^[0-9]+\.+", "", os.path.basename(project_dir)))

        #get this wd's job conf
        projectConf = os.path.join(project_dir, '.moa', 'config')
        if os.path.exists(projectConf):
            pc = Yaco.Yaco()
            pc.load(projectConf)

            if pc.title:
                job.conf['project'] = pc.title
            job.conf['ppud'] = pc.get('pud', '')

        if not job.conf.get('pud', ''):
            job.conf['pud'] = _getUniqueId(project_dir)
            job.conf.save()

        return
