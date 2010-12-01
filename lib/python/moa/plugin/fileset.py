#
# Copyright 2009, 2010 Mark Fiers, Plant & Food Research
# 
# This file is part of Moa - http://github.com/mfiers/Moa
# 
# Moa is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your
# option) any later version.
# 
# Moa is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
# or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public
# License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with Moa.  If not, see <http://www.gnu.org/licenses/>.
# 
"""
Filesets
--------

Define sets of files for Moa

"""

import re
import os
import sys
import readline
import moa.ui
import glob
import moa.utils
import moa.logger as l

def prepare(data):
    job = data['job']
    moaId = job.template.name

    if not job.template.has_key('filesets'):
        return
    
    if len(job.template.filesets.keys()) > 0:
        job.conf['moa_filesets'] = []
        job.conf.doNotSave.append('moa_filesets')

    for fsid in job.template.filesets.keys():
        
        job.conf['moa_filesets'].append(fsid)

        fs = job.template.filesets[fsid]

        if fs.type == 'map':

            job.template.parameters['%s_dir' % fsid] = {
                'category' : fs.get('category', 'input'),
                'optional' : fs.get('optional', True),
                'help' : 'directory for the %s file set',
                'default' : fs.get('dir', '.'),
                'type' : 'directory',
                }
            
            job.template.parameters['%s_extension' % fsid] = {
                'category' : fs.get('category', 'input'),
                'optional' : True,
                'help' : 'extension for the %s file set',
                'default' : fs.get('extension', ''),
                'type' : 'string'
                }
            job.template.parameters['%s_glob' % fsid] = {
                'category' : fs.get('category', 'input'),
                'optional' : True,
                'default' : fs.get('glob', '*'),
                'help' : 'Output glob for the mapped file set "%s"' % fsid,
                'type' : 'string',
                }
        elif fs.type in ['set']:
            job.template.parameters['%s_dir' % fsid] = {
                'category' : fs.get('category', 'input'),
                'optional' : fs.optional,
                'help' : fs.help,
                'type' : 'directory'
                }
            job.template.parameters['%s_extension' % fsid] = {
                'category' : 'input',
                'optional' : True,
                'default' : fs.extension,
                'help' : 'Extension for the file set "%s"' % fsid,
                'type' : 'string',
                }
            job.template.parameters['%s_glob' % fsid] = {
                'category' : 'input',
                'optional' : True,
                'default' : fs.get('glob', '*'),
                'help' : 'File glob for the file set "%s"' % fsid,
                'type' : 'string',
                }
        elif fs.type == 'single':
            job.template.parameters['%s' % fsid] = {
                'category' : fs.get('category', 'input'),
                'default' : fs.get('default', ''),
                'optional' : fs.optional,
                'help' : fs.help,
                'type' : 'file'
                }
            #unless it is an input file, do not check for this
            #file to exists! (since it might not yet)
            if not fs.category == 'input':
                job.conf.doNotCheck.append('%s_file' % fsid)


def _files_from_glob(dir, pat, ext):
    """
    Return a set of files from a glob
    """
    if ext:
        return glob.glob(os.path.join(
            dir, '%s.%s' % (pat, ext)))
    else:
        return glob.glob(os.path.join(dir, pat))

def _map_files(allSets, conf, fromId, toId):
    """
    Map files from one set to another
    """
    fos = allSets[fromId]
    tos = allSets[toId]
    
    frext = conf['%s_extension' % fromId]
    todir = conf['%s_dir' % toId]
    toext = conf['%s_extension' % toId]

    frglob = conf['%s_glob' % fromId]
    toglob = conf['%s_glob' % toId]
    
    with open(os.path.join('.moa', '%s.fof' % fromId)) as F:
        frof = map(os.path.basename, F.read().split())

    #map directory
    if todir:
        frof = [os.path.join(todir, x) for x in frof]

    #map extensions
    if frext and toext:
        rere = re.compile('%s$' % frext)
        frof = [rere.sub(toext, x) for x in frof]
    elif toext:
        frof = ['%s.%s' % (x, toext) for x in frof]    

    #map glob
    if toglob.count('*') > 1:
        l.critical("Cannot handle more than one '*' in the %s_glob" % toId)
        sys.exit(-1)
    elif toglob == '*':
        pass
    elif toglob.count('*') == 1:
        if not frglob.count('*') == 1:
            l.critical("Input glob needs to have a '*' (mapping %s->%s / %s->%s)" % 
                       (fromId, toId, frglob, toglob))
            sys.exit(-1)
        frof = [re.sub('^' + frglob.replace('*', '(.*)'),
                       toglob.replace('*', r'\1'),
                       x) for x in frof]
    else:
        if len(frof) != 1:
            l.critical(("With no wildcard in the  %s_glob, the input may not " % toId +
                        "consist of more than one file"))
        if toext:
            frof = [os.path.join(todir, '%s.%s' % (toglob, toext))]
            print 'mappig to ', frof            
        else:
            frof = [toglob]
                
    return frof



def readFileSet(job, fsid):
    fof = os.path.join('.moa', '%s.fof' % fsid)
    if os.path.exists(fof):
        with open(fof) as F:
            return F.read().split()
    else:
        return []

def preRun(data):
    
    job = data['job']
    moaId = job.template.name

    job.data.fileSets = {}

    if not job.template.has_key('filesets'):
        return

    #First, collect 'input'/'set' files
    #create a list of all sets & order them - MAPS GO LAST!!
    for fsid in job.template.filesets.keys():
        fs = job.template.filesets[fsid]
        if not fs.has_key('order'):
            if fs.type == 'map':
                fs.order = 100
            else:
                fs.order = 50

    fileSetList = [(job.template.filesets[x].order, x)
                   for x in job.template.filesets.keys()]
    fileSetList.sort()


    for order, fsid in fileSetList:
        fs = job.template.filesets[fsid]
        job.data.fileSets[fsid] = fs

        if fs.type == 'set':
            files = _files_from_glob(
                job.conf['%s_dir' % fsid],
                job.conf['%s_glob' % fsid],
                job.conf['%s_extension' % fsid])
        elif fs.type == 'single':
            files = [job.conf['%s' % fsid]]
        elif fs.type == 'map':
            if not fs.source:
                moa.ui.exitError("Map fileset must have a source!")
            frfs = job.template.filesets[fs.source]
            files = _map_files( job.template.filesets, job.conf, 
                                fromId = fs.source, toId = fsid)        
        else:
            moa.ui.exitError("Invalid data set type %s for data set %s" % (
                    fs.type, fsid))
        l.debug("Recovered %d files for fileset %s" % (len(files), fsid))
        job.data.fileSets[fsid].files = files
        with open(os.path.join(job.wd, '.moa', '%s.fof' % fsid), 'w') as F:
            F.write("\n".join(files))
            
    #rearrange the files for use by the job
    job.data.inputs = []
    job.data.outputs = []
    job.data.prerequisites = []

    for fsid in job.template.filesets.keys():
        fs = job.template.filesets[fsid]
        if fs.category == 'input':
            job.data.inputs.append(fsid)
        if fs.category == 'output':
            job.data.outputs.append(fsid)
        if fs.category == 'prerequisite':
            job.data.prerequisites.append(fsid)

    for fsid in job.data.fileSets.keys():
        fs = job.data.fileSets[fsid]
        l.info('Found fileset %s (%s) with %d files' % (
                fsid, fs.type, len(fs.files)))

    
TESTSCRIPT = """
moa new adhoc -t 'something'
"""
