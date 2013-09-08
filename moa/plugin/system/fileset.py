# Copyright 2009-2011 Mark Fiers
# The New Zealand Institute for Plant & Food Research
#
# This file is part of Moa - http://github.com/mfiers/Moa
#
# Licensed under the GPL license (see 'COPYING')
#
"""
**fileset** - define sets of in&output files
--------------------------------------------
"""

import os
import sys

import fist

import moa.ui
import moa.args
import moa.api

import moa.utils
import moa.logger
l = moa.logger.getLogger(__name__)


from moa.sysConf import sysConf

def _prepFileList(fileList, basepath, jobpath):
    """
    Prepare a list of files for display
    """
    ## perform some file magic
    dar = os.path.abspath(basepath)
    wer = '/'
    #l.critical(dar +  ' -- ' + wer)
    rv = []

    for f in fileList:
        fup = os.path.join(jobpath, f)
        dirurl = os.path.dirname(fup).replace(dar, wer)
        dirurl.replace('//', '/')
        fullurl = fup.replace(dar, wer)
        fullurl.replace('//', '/')

        l.critical(fup)

        if os.path.exists(fup):
            #file exists
            rv.append([f, os.path.basename(f), os.path.dirname(f), True, fullurl, dirurl])
        else:
            l.critical('konijn' + fup)
            rv.append([f, os.path.basename(f), os.path.dirname(f), False, fullurl, dirurl])

    return rv


@moa.api.api
def fileset_prepare_display(job, basepath, jobpath):
    """
    prepare this job's filesets for display

    """
    mappedSets = {}
    fss = job.data.filesets
    #first find the 'sets & singletons'
    for fsid in fss.keys():
        fs = fss[fsid]
        if fs.type == 'set':
            mappedSets[fsid] = {
                'type': 'group',
                'fs' : fs,
                'lifs': _prepFileList(fs.files, basepath, jobpath),
                'maps' : {}}
        elif fs.type == 'single':
            mappedSets[fsid] = {
                'type': 'single',
                'lifs': _prepFileList(fs.files, basepath, jobpath),
                'fs' : fs }


    #now find the maps that map to the other sets
    for fsid in fss.keys():
        fs = fss[fsid]
        if fs.type == 'map':
            source = fs.source
            fs['lifs'] = _prepFileList(fs.files, basepath, jobpath)
            mappedSets[source]['maps'][fsid] = fs
    return mappedSets

def _preformatFile(f):
    """
    Check if a file exists
    """
    if os.path.isfile(f):
        return "{{green}}%s{{reset}}" % f
    else:
        return "{{red}}%s{{reset}}" % f


@moa.args.doNotLog
@moa.args.needsJob
@moa.args.argument('-n', '--no_files', type=int, help="No filesets to show (default 10)", default=10)
@moa.args.addFlag('-a', '--all', help="Show all filesets")
@moa.args.command
def files(job, args):
    """
    Show in and output files for this job

    Display a list of all files discovered (for input & prerequisite
    type filesets) and inferred from these for map type filesets.

    """

    filesets = job.template.filesets.keys()
    filesets.sort()
    #first print singletons
    fsets = []
    fmaps = []
    for fsid in filesets:
        templateInfo = job.template.filesets[fsid]
        files = job.data.filesets[fsid].files

        if templateInfo.type == 'set':
            fsets.append(fsid)
            continue
        elif templateInfo.type == 'map':
            fmaps.append(fsid)
            continue
        if len(files) == 0:
            moa.ui.fprint(
                ('* Fileset: %%(bold)s%-20s%%(reset)s (single): ' +
                 '%%(bold)s%%(red)sNo file found%%(reset)s') % fsid )
        elif len(files) == 1:
            moa.ui.fprint(
                '* Fileset: {{bold}}%-20s{{reset}} (single)\n' % fsid,
                f='jinja')
            moa.ui.fprint('   ' + _preformatFile(files[0]), f='jinja')

    if len(fsets + fmaps) == 0:
        return

    #rearrange the files into logical sets
    nofiles = len(job.data.filesets[(fsets + fmaps)[0]].files)
    moa.ui.fprint("")

    if args.all:
        toprint = nofiles
    else:
        toprint = min(args.no_files, nofiles)

    for i in range(toprint):
        thisSet = []
        for j, fsid in enumerate((fsets + fmaps)):
            files = job.data.filesets[fsid].files
            templateInfo = job.template.filesets[fsid]
            thisSet.append((templateInfo.category,
                            templateInfo.type,
                            fsid,
                            files[i]))
            if j == 0:
                moa.ui.fprint("  {{bold}}%3d{{reset}}:" % i, f='jinja', newline=False)
            else:
                moa.ui.fprint("      ", f='jinja', newline=False)
            cat = templateInfo.category
            if cat == 'input':
                moa.ui.fprint("{{green}}inp{{reset}}", f='jinja', newline=False)
            elif cat == 'output':
                moa.ui.fprint("{{blue}}out{{reset}}", f='jinja', newline=False)
            else:
                moa.ui.fprint("{{red}}%s{{reset}}" % cat[:3], f='jinja', newline=False)
            moa.ui.fprint(" {{gray}}%-5s{{reset}}" % templateInfo.type, f='jinja', newline=False)
            moa.ui.fprint(" {{bold}}%-20s{{reset}} " % fsid, f='jinja', newline=False)
            moa.ui.fprint(_preformatFile(files[i]), f='jinja', newline=False)
            moa.ui.fprint("")
        moa.ui.fprint("")
    if toprint < nofiles:
        moa.ui.fprint("... and %d more" % (nofiles - toprint))
