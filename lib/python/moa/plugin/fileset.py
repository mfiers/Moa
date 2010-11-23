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
    
    l.debug("running fileset prepare for template %s" % moaId)

    for fsid in job.template.filesets.keys():
        
        if not job.conf.has_key('moa_filesets'):
            job.conf['moa_filesets'] = []
        job.conf['moa_filesets'].append(fsid)

        fs = job.template.filesets[fsid]
        
        if not fs.type == 'input': continue
        
        job.template.parameters['%s_dir' % fsid] = {
            'category' : 'input',
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
            'default' : '*',
            'help' : 'File glob for the file set "%s"' % fsid,
            'type' : 'string',
            }

        # job.template.parameters['%s_limit' % fsid] = {
        #     'category' : 'input',
        #     'optional' : True,
        #     'help' : 'Mac number of files to use for file set "%s"' % fsid,
        #     'type' : 'integer',
        #     }
        # job.template.parameters['%s_sort' % fsid] = {
        #     'category' : 'input',
        #     'optional' : True,
        #     'default' : '*',
        #     'help' : 'File glob for the file set "%s"' % fsid,
        #     'type' : 'integer',
        #     }

        #add some info to the configuration - so that the template
        #knows that there are filesets


def _files_from_glob(dir, pat, ext):
    """
    Return a set of files from a glob
    """
    if ext:
        return glob.glob(os.path.join(
            dir, '%s.%s' % (pat, ext)))
    else:
        return glob.glob(os.path.join(dir, pat))

def _map_files(fr, frext, dir, ext):
    """
    Map files from one set to another
    """
    with open(os.path.join('.moa', '%s.fof' % fr)) as F:
        frof = map(os.path.basename, F.read().split())
    if dir:
        frof = [os.path.join(dir, x) for x in frof]
    if frext and ext:
        rere = re.compile('%s$' % frext)
        frof = [rere.sub(ext, x) for x in frof]
    elif ext:
        frof = ['%s.%s' (x, ext) for x in frof]
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
        files = _map_files(
            fr = fs.source,
            frext = job.conf['%s_extension' % fs.source],
            dir = fs.dir,
            
            ext = fs.extension)
        
        with open(os.path.join(job.wd, '.moa', '%s.fof' % fsid), 'w') as F:
            for f in files:
                F.write('%s\n'% f)

    
TESTSCRIPT = """
moa new adhoc -t 'something'
"""
