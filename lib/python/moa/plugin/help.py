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

import os
import sys
import pydoc
import pprint
import optparse
from subprocess import Popen, PIPE

from jinja2 import Environment, FileSystemLoader

import moa.runMake
import moa.info
import moa.logger
l = moa.logger.l

MOABASE=os.environ['MOABASE']

def defineCommands(commands):
    commands['help'] = {
        'desc' : 'Display help on the current job (not this help!)',
        'call' : showHelp
        }

def showHelp(wd, options, args):
    if not moa.info.isMoaDir(wd):
        l.error("This is not a moa directory - `moa help` should be executed in")
        l.error("the context of a Moa directory. Try `moa --help`")
        sys.exit(-1)
    #moa.runMake.go(wd, target = 'help', verbose = options.verbose)

    data = moa.info.info(wd)
    #see if there is a manual in $MOABASE/doc/markdown/templates
    moaId = data['moa_id']
    templateDoc = os.path.join(MOABASE, 'doc', 'markdown',
                               'templates', '%s.md' % moaId)

    #load & render the jinja2 template
    if os.path.exists(templateDoc):
        templateDoc = open(templateDoc).read()
    else:
        templateDoc = ""
    data['template_manual'] = templateDoc
    jenv = Environment(loader=FileSystemLoader('%s/doc/templates' % MOABASE))
    manTemplate = jenv.get_template('template.help.md')

    markdown = manTemplate.render(d = data)
    
    #convert jinja2 to 
    p = Popen("pandoc -s -f markdown -t man".split(),
              stdin=PIPE, stdout=PIPE)    
    p.stdin.write(markdown)
    man,err = p.communicate()


    p2 = Popen("nroff -c -mandoc".split(),
               stdin=PIPE, stdout=PIPE, stderr=PIPE)
    p2.stdin.write(man)
    doc, err = p2.communicate()
    

    pydoc.pager(doc)
