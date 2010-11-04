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
    newTemplateDir = os.path.join(MOABASE, 'template2')
    for job in moa.template.list():
        
        newTemplateConf = os.path.join(newTemplateDir, '%s.moa' % job)
        newTemplateFile = os.path.join(newTemplateDir, '%s.mk' % job)
        
        l.info("start conversion of %s" % job)
        
        wd = moa.job.newTestJob(template=job)
        inf = moa.info.info(wd)
        inf['template_type'] = 'gnumake'
        del inf['parameter_categories']
        inf['commands'] = inf['moa_targets']
        inf['commands'].remove('all')
        del inf['moa_targets']
        del inf['all_help']
        del inf['moa_files']
        inf['help'] = inf.get('help', {})
        for c in inf['commands']:
            inf['help'][c] = inf['%s_help' % c]
            del inf['%s_help' % c]
        inf['gnumake_makefile'] = newTemplateFile
        del inf['template_file']
        for p in inf.get('parameters', []):
            del inf['parameters'][p]['value']
            
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
        
