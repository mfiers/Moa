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

import fist

import moa.ui
import moa.utils
import moa.logger as l

from moa.sysConf import sysConf

def defineCommands(data):
    """
    Set the moa commands for this plugin
    """
    data['commands']['files'] = {
        'desc' : 'Show an overview of the files for this job',
        'call' : showFiles,
        }
    
def showFiles(job):
    """
    **moa files** - Display discovered & inferred files for this job

    Usage::

       moa files

    Display a list of all files discovered (for input & prerequisite
    type filesets) and inferred from these for map type filesets.
    
    """
    filesets = job.template.filesets.keys()
    filesets.sort()
    for fsid in filesets:
        files = job.data.filesets[fsid].files
        if len(files) == 0:
            moa.ui.fprint('* Fileset: %%(bold)s%-20s%%(reset)s: %%(bold)s%%(red)sNo files found%%(reset)s' % 
                          fsid)
        else:
            moa.ui.fprint(('* Fileset: %%(bold)s%-20s%%(reset)s '
                           '(%-6s: '
                           '%%(green)s%%(bold)s%d%%(reset)s file(s) found'
                           ' (%s)') % 
                          (fsid, job.template.filesets[fsid].type + ')', len(files), str(job.template.filesets[fsid].pattern)))
            for f in files[:3]:
                moa.ui.fprint('    %(blue)s' + f + '%(reset)s')
            if len(files) > 3:
                moa.ui.fprint('       ... and %d more' % (len(files)-3))
    
    
def prepare_3(data):

    job = sysConf.job

    if not job.template.has_key('filesets'):
        return

    if len(job.template.filesets.keys()) > 0:
        job.conf['moa_filesets'] = []
        job.conf.doNotSave.append('moa_filesets')

    for fsid in job.template.filesets.keys():
        job.conf['moa_filesets'].append(fsid)
        fs = job.template.filesets[fsid]
            
        if fs.type == 'map':            
            job.template.parameters[fsid] = {
                'category' : fs.get('category', 'input'),
                'optional' : fs.get('optional', True),
                'help' : 'map pattern for the %s file set',
                'default' : fs.get('pattern', '*'),
                'type' : 'string'
                }
            
        elif fs.type in ['set']:
            
            job.template.parameters[fsid] = {
                'category' : fs.get('category', 'input'),
                'default' : fs.get('pattern', ''),
                'optional' : fs.get('optional', False),
                'help' : fs.help,
                }
            
        elif fs.type == 'single':
            job.template.parameters[fsid] = {
                'category' : fs.get('category', 'input'),
                'default' : fs.get('pattern', ''),
                'optional' : fs.get('optional', True),
                'help' : fs.help,
                'type' : 'file'
                }


        #unless it is an input file, do not check for this
        #file to exists! (since it might not exist yet)
        if not fs.category in ['input', 'prerequisite']:
            job.conf.doNotCheck.append('%s' % fsid)

def preFiles(data):
    """
    Run before execution of any command (backend or plugin)
    """
    l.debug("preparing input files")
    preparefilesets(data)


def pre_command(data):
    """
    Run before execution of any command (backend or plugin)
    """
    l.debug("preparing input files")
    preparefilesets(data)

def preparefilesets(data):
    """
    prepare all filesets 
    """
    job = data['job']
    job.data.filesets = {}

    if not job.template.has_key('filesets'):
        return

    fileSets = job.template.filesets.keys()

    import copy
    allSets = copy.copy(fileSets)
    allSets.sort()
    while True:
            
        if len(fileSets) == 0: break
        fsid = fileSets.pop(0)

        fs = job.template.filesets[fsid]
                
        job.data.filesets[fsid] = fs

        #Resolve filesets - first the NON-map sets
        if fs.type == 'set':
            files = fist.fistFileset(job.conf[fsid])
            files.resolve()
        elif fs.type == 'single':
            files = fist.fistSingle(job.conf[fsid])
        elif fs.type == 'map':
            if not fs.source:
                moa.ui.exitError("Map fileset must have a source!")
            
            if not job.data.filesets.has_key(fs.source) or \
                    not job.data.filesets[fs.source].has_key('files') or \
                    not job.data.filesets[fs.source].files.resolved:
                fileSets.append(fsid)
                continue
            source = job.data.filesets[fs.source].files
            files = fist.fistMapset(job.conf[fsid])
            files.resolve(source)
        else:
            moa.ui.exitError("Invalid data set type %s for data set %s" % (
                    fs.type, fsid))
            
        l.debug("Recovered %d files for fileset %s" % (len(files), fsid))

        job.data.filesets[fsid].files = files
        with open(os.path.join(job.wd, '.moa', '%s.fof' % fsid), 'w') as F:
            F.write("\n".join(files) + "\n")
            
            
    #rearrange the files for use by the job
    job.data.inputs = []
    job.data.outputs = []
    job.data.prerequisites = []
    job.data.others = []
    
    for fsid in job.template.filesets.keys():
        fs = job.template.filesets[fsid]
        if fs.category == 'input':
            job.data.inputs.append(fsid)
        if fs.category == 'output':
            job.data.outputs.append(fsid)
        if fs.category == 'prerequisite':
            job.data.prerequisites.append(fsid)
        if fs.category == 'other':
            job.data.others.append(fsid)

    for fsid in job.data.filesets.keys():
        fs = job.data.filesets[fsid]
        l.debug('Found fileset %s (%s) with %d files' % (
                fsid, fs.type, len(fs.files)))

    
TESTSCRIPT = """
moa new adhoc -t 'something'
"""
