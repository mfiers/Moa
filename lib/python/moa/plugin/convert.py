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
    if len(args) > 1:
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
            print p, newParName
            for k in par:
                print ' -', k, par[k]
            inf['parameters'][newParName]= par

            
        for k in  inf.keys():
            print '.%s.' % k, "\t", str(inf[k])[:60]

        with open(newTemplateConf, 'w') as F:
            yaml.dump(inf, F)

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
        for suffix in ['title', 'help', 'type', 'define', 'description',
                       'prerequisites', 'default', 'allowed', 'set', 'simple']:
            rere = re.compile(r'\S+'+suffix+r' ?\+?=.*?(?<!\\)\n', re.S)
            text = rere.sub('', text)
            #for x in rere.finditer(text):
            #    print x.group(0)
            #    print

        rere = re.compile(r'([\t ]*\n){2,}', re.S)
        text = rere.sub("\n\n", text)

        with open(newTemplateFile, 'w') as G:
            G.write(text)
        
