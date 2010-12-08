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
filesets
--------

Define sets of files for Moa

"""

import re
import os
import sys
import readline
import glob

import fist

import moa.ui
import moa.utils
import moa.logger as l



def defineCommands(data):
    """
    Set the moa commands for this plugin
    """
    data['commands']['files'] = {
        'desc' : 'Show an overview of the files for this job',
        'call' : showFiles,
        }
    
def showFiles(data):
    """
    files
    -----
    
    Show an overview of the files found for this job
    """
    job = data['job']
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
                           '%%(green)s%%(bold)s%d%%(reset)s files found'
                           '') % 
                          (fsid, job.template.filesets[fsid].type + ')', len(files)))
            for f in files[:3]:
                moa.ui.fprint('    %(blue)s' + f + '%(reset)s')
            if len(files) > 3:
                moa.ui.fprint('       ... and %d more' % (len(files)-3))
    
    
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
                'default' : fs.get('default', ''),
                'optional' : fs.get('optional', True),
                'help' : fs.help,
                'type' : 'file'
                }
            
            #unless it is an input file, do not check for this
            #file to exists! (since it might not exist yet)
            if not fs.category == 'input':
                job.conf.doNotCheck.append('%s_file' % fsid)
                

#def _files_from_glob(dir, pat, ext):
#    """
#    Return a set of files from a glob
#    """
#    rv = []
#    if ext:
#        rv = glob.glob(os.path.join(
#            dir, '%s.%s' % (pat, ext)))
#    else:
#        rv = glob.glob(os.path.join(dir, pat))
#    
#    l.debug("from glob %s // %s // %s" % (dir, pat, ext))
#    l.debug("found %d files" % len(rv))
#    return rv
#
#def _map_files(job, fromId, toId):
#    """
#    Map files from one set to another
#    """
#    allSets = job.template.filesets
#    fos = allSets[fromId]
#    tos = allSets[toId]
#    conf = job.conf
#
#    frof = [os.path.basename(x) for x in job.data.filesets[fromId]['files']]
#
#    #no input files - no output files
#    if len(frof) == 0: 
#        return []
#
#    todir = conf['%s_dir' % toId]
#    toext = conf['%s_extension' % toId]
#    toglob = conf['%s_glob' % toId]
#
#    if fos.type == 'single':
#        frglob = '*'
#        infile = os.path.basename(frof[0])
#        if '.' in infile:
#            frext = infile.rsplit('.',1)[-1]
#        else: frex = ''
#    else:
#        frext = conf.get('%s_extension' % fromId, '')
#        frglob = conf.get('%s_glob' % fromId, '*')
#    
#    #map directory
#    if todir:
#        frof = [os.path.join(todir, x) for x in frof]
#
#    #map extensions
#    if frext and toext:
#        rere = re.compile('%s$' % frext)
#        frof = [rere.sub(toext, x) for x in frof]
#    elif toext:
#        frof = ['%s.%s' % (x, toext) for x in frof]    
#
#    #map glob
#    if toglob.count('*') > 1:
#        l.critical("Cannot handle more than one '*' in the %s_glob" % toId)
#        sys.exit(-1)
#    elif toglob == '*':
#        pass
#    elif toglob.count('*') == 1:
#        if not frglob.count('*') == 1:
#            l.critical(("Input glob needs to have a '*' "
#                        "(mapping %s->%s / %s->%s)") % 
#                       (fromId, toId, frglob, toglob))
#            sys.exit(-1)
#        frof = [re.sub('^' + frglob.replace('*', '(.*)'),
#                       toglob.replace('*', r'\1'),
#                       x) for x in frof]
#    else:
#        if len(frof) != 1:
#            l.critical(("With no wildcard in the  %s_glob, the input "
#                        "may not consist of more than one file") % toId)
#        if toext:
#            frof = [os.path.join(todir, '%s.%s' % (toglob, toext))]
#            print 'mappig to ', frof            
#        else:
#            frof = [toglob]
#                
#    return frof
#
#def readfileset(job, fsid):
#    fof = os.path.join('.moa', '%s.fof' % fsid)
#    if os.path.exists(fof):
#        with open(fof) as F:
#            return F.read().split()
#    else:
#        return []


def preCommand(data):
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
    moaId = job.template.name

    job.data.filesets = {}

    if not job.template.has_key('filesets'):
        return

    #First, collect 'input'/'set' files
    #create a list of all sets & order them - MAPS GO LAST!!
    
    fileSets = job.template.filesets.keys()
    
#    for fsid in job.template.filesets.keys():
#        fs = job.template.filesets[fsid]
#        if not fs.has_key('order'):
#            if fs.type == 'map':
#                fs.order = 100
#            else:
#                fs.order = 50
#
#    filesetList = [(job.template.filesets[x].order, x)
#                   for x in job.template.filesets.keys()]
#    filesetList.sort()

    while True:
        if len(fileSets) == 0: break
        fsid = fileSets.pop(0)        
        fs = job.template.filesets[fsid]
        job.data.filesets[fsid] = fs
        oriPat = job.template.filesets[fsid].get('pattern', './*')
        
        if fs.type == 'set':
            files = fist.fistFileset(job.conf[fsid], oriPat)
            files.resolve()
        elif fs.type == 'single':
            files = files.fistSingle(job.conf[fsid], oriPat)
        elif fs.type == 'map':
            if not fs.source:
                moa.ui.exitError("Map fileset must have a source!")
            if not job.data.filesets.has_key(fs.source) or \
                    not job.data.filesets[fs.source].has_key('files') or \
                    not job.data.filesets[fs.source].files.resolved:
                fileSets.append(fsid)
                continue
            source = job.data.filesets[fs.source].files
            files = fist.fistMapset(job.conf[fsid], oriPat)
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
    
    for fsid in job.template.filesets.keys():
        fs = job.template.filesets[fsid]
        if fs.category == 'input':
            job.data.inputs.append(fsid)
        if fs.category == 'output':
            job.data.outputs.append(fsid)
        if fs.category == 'prerequisite':
            job.data.prerequisites.append(fsid)

    for fsid in job.data.filesets.keys():
        fs = job.data.filesets[fsid]
        l.debug('Found fileset %s (%s) with %d files' % (
                fsid, fs.type, len(fs.files)))

    
TESTSCRIPT = """
moa new adhoc -t 'something'
"""
