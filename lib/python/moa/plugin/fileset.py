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
                'default' : fs.dir,
                'type' : 'directory',
                }
            
            job.template.parameters['%s_extension' % fsid] = {
                'category' : fs.get('category', 'input'),
                'optional' : True,
                'help' : 'extension for the %s file set',
                'default' : fs.extension,
                'type' : 'string'
                }
            job.template.parameters['%s_glob' % fsid] = {
                'category' : fs.get('category', 'input'),
                'optional' : True,
                'default' : fs.get('glob', '*'),
                'help' : 'Output glob for the mapped file set "%s"' % fsid,
                'type' : 'string',
                }
        else:
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
    if not toglob == '*' and \
       toglob.count('*') == 1 and \
       frglob.count('*') == 1:
        frof = [re.sub('^' + frglob.replace('*', '(.*)'),
                          toglob.replace('*', r'\1'),
                          x) for x in frof]
        
    return frof

def preRun(data):
    
    job = data['job']
    moaId = job.template.name

    if not job.template.has_key('filesets'):
        return

    #First, collect input files
    for fsid in job.template.filesets.keys():
        fs = job.template.filesets[fsid]
        if not fs.type == 'input':
            continue
        files = _files_from_glob(
            job.conf['%s_dir' % fsid],
            job.conf['%s_glob' % fsid],
            job.conf['%s_extension' % fsid])
        with open(os.path.join(job.wd, '.moa', '%s.fof' % fsid), 'w') as F:
            for f in files:
                F.write('%s\n'% f)
                
    #Then, map files
    for fsid in job.template.filesets.keys():
        fs = job.template.filesets[fsid]
        if not fs.type == 'map':
            continue
        frfs = job.template.filesets[fs.source]
        files = _map_files(
            job.template.filesets,
            job.conf,
            fromId = fs.source,
            toId = fsid)

        with open(os.path.join(job.wd, '.moa', '%s.fof' % fsid), 'w') as F:
            for f in files:
                F.write('%s\n'% f)

    
TESTSCRIPT = """
moa new adhoc -t 'something'
"""
