# 
# Copyright 2009 Mark Fiers, Plant & Food Research
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
Help
"""
import re
import os
import sys
import yaml
import pprint
import optparse

import moa.conf
import moa.job
import moa.info
import moa.utils
import moa.plugin
import moa.logger as l
import textwrap

MAKEFILE_CONVERT_LINES = [
    ('include $(MOABASE)/template/moa/prepare.mk',
     'include $(MOABASE)/lib/gnumake/prepare.mk'),
    ('include $(MOABASE)/template/moa/core.mk',
     'include $(MOABASE)/lib/gnumake/core.mk'),
    ('include $(shell echo $$MOABASE)/template/moa/prepare.mk',
     'include $(MOABASE)/lib/gnumake/prepare.mk'),
    ('include $(shell echo $$MOABASE)/template/moa/core.mk',
     'include $(MOABASE)/lib/gnumake/core.mk'),
    ]

MOABASE = moa.utils.getMoaBase()

def defineCommands(data):
    data['commands']['template_convert'] = {
        'private' : True,
        'call' : templateConvert
        }

def templateConvert(data):
    args = data['newargs']
    if len(args) < 1:
        l.critical("need to specify a target directory")
    newTemplateDir = args[0]
    convert_only = args[1:]
        
    if not os.path.exists(newTemplateDir):
        l.warning("creating directory %s" % newTemplateDir)
        os.makedirs(newTemplateDir)
        
    for job in moa.job.list():
        if convert_only and not job in convert_only: continue
        newTemplateConf = os.path.join(newTemplateDir, '%s.moa' % job)
        newTemplateFile = os.path.join(newTemplateDir, '%s.mk' % job)
        
        l.info("start conversion of %s" % job)
        
        wd = moa.job.newTestJob(template=job, title='for conversion')

        inf = moa.info.info(wd)
        
        moaId = inf['moa_id']
        
        inf['backend'] = 'gnumake'
        del inf['parameter_categories']
        inf['commands'] = inf['moa_targets']
        inf['commands'].remove('all')
        del inf['moa_targets']
        del inf['all_help']
        if inf.has_key('title'): del inf['title']
        del inf['moa_files']
        if not inf['description'] and \
           inf['template_description']:
            inf['description'] = inf['template_description']

        del inf['template_file']
        for k in inf.keys():
            if 'template_' in k:
                v = inf[k]
                del inf[k]
                
                inf[k.replace('template_', '')] = v
        inf['help'] = inf.get('help', {})
        for c in inf['commands']:
            inf['help'][c] = inf['%s_help' % c]
            del inf['%s_help' % c]
        inf['gnumake_makefile'] = newTemplateFile
        #del inf['template_file']
        for p in inf.get('parameters', []):
            par = inf['parameters'][p]
            del inf['parameters'][p]
            newParName = p.replace('%s_' % moaId, '')
            if par.has_key('value'): del par['value']
            if par.has_key('cardinality'): del par['cardinality']
            #print p, newParName
            #for k in par:
            #    print ' -', k, par[k]
            inf['parameters'][newParName]= par

            
        #convert gnumake file
        oldTemplateFile = os.path.join(MOABASE, 'template', '%s.mk' % job)
        with open(oldTemplateFile) as F:
            lines = F.readlines()
        #first parse on a line by line basis
        for lineNo, line  in enumerate(lines):
            
            for m in MAKEFILE_CONVERT_LINES:
                if line.find(m[0]) == 0:
                    lines[lineNo] = m[1]
                    break

        text = "".join(lines)

        #print text
        #see if there are 'input filesets'
        #$(call moa_fileset_define_opt,$(moa_id)_input,,Input files for $(moa_id))
        rere = re.compile(r'\$\(call moa_fileset_define(.*),(.+),(.*),(.*)\)')
        for x in rere.finditer(text):
            fsid = x.groups()[1]
            fsid = fsid.replace('$(moa_id)', moaId).replace(moaId + '_','')
            fsdesc = x.groups()[3].replace('$(moa_id)', moaId)
            l.info("found fileset for %s" % fsid)
            if x.groups()[0] == '_opt':
                fsopt = True
            else:
                fsopt = False
            fs = { 'type' : 'input',
                   'description' : fsdesc,
                   'optional' : fsopt
                  }
            if not inf.has_key('filesets'):
                inf['filesets'] = {}
            inf['filesets'][fsid] = fs

            #and now remove all related parameters from the configuration
            for x in ['_extension', '_glob', '_limit', '_sort']:
                ky = fsid + x
                if inf['parameters'].has_key(ky):
                    del inf['parameters'][ky]

        text = rere.sub('', text)

        # see if there are 'remap' filesets
        rere = re.compile(r'\$\(call moa_fileset_remap(.*),(.+),(.*),(.*)\)')
        for x in rere.finditer(text):
            fsid = x.groups()[2].replace('$(moa_id)', moaId).replace(moaId + '_','')
            fssrc = x.groups()[1].replace('$(moa_id)', moaId).replace(moaId + '_','')
            fs_target_extension = x.groups()[3]
            l.info("found a remap fileset: %s to %s" % (fssrc, fsid))
            if x.groups()[0] == '_nodir':
                fs_target_dir = '.'
            else:
                fs_target_dir = os.path.join('.', fs_target_extension)
            fs = {'type' : 'map',
                  'source' : fssrc,
                  'dir' : fs_target_dir,
                  'extension' : fs_target_extension
                  }
            if not inf.has_key('filesets'):
                inf['filesets'] = {}
            inf['filesets'][fsid] = fs

        text = rere.sub('', text)
        #rere = re.compile(r'(\$\(call.*)')
        #for x in rere.finditer(text):
        #    l.warning("found $call")
        #    l.warning(x.groups()[0])

        
        for suffix in ['title', 'help', 'type', 'define', 'description',
                       'prerequisites', 'default', 'allowed', 'set', 'simple']:
            rere = re.compile(r'\S+'+suffix+r' ?\+?=.*?(?<!\\)\n', re.S)
            text = rere.sub('', text)

        rere = re.compile(r'([\t ]*\n){2,}', re.S)
        text = rere.sub("\n\n", text)

        #save & store the new files
        thisTargetDir = os.path.dirname(newTemplateConf)
        if not os.path.exists(thisTargetDir):
            os.makedirs(thisTargetDir)

        with open(newTemplateConf, 'w') as F:
            yaml.dump(inf, F)

        with open(newTemplateFile, 'w') as G:
            G.write(text)
        
