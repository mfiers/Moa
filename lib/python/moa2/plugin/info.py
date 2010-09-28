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
import pprint
import optparse
import moa.conf
import moa.job
import moa.info
import moa.plugin
import moa.logger as l
import textwrap

def defineCommands(data):
    data['commands']['rawinfo'] = {
        'private' : True,
        'call' : rawInfo
        }

    data['commands']['status'] = {
        'private' : True,
        'call' : status
        }

    data['commands']['template'] = {
        'private' : False,
        'call' : template,
        'desc' : 'Show the template of this moa job'
        }

    data['commands']['show'] = {
        'desc' : 'Show the configured parameters and their values',
        }

    data['commands']['list'] = {
        'desc' : 'List all known templates',
        'call' : listTemplates,
        }

    data['commands']['listlong'] = {
        'desc' : 'List all known templates, showing a short description',
        'call' : listTemplatesLong,
        }

def listTemplates(data):
    for job in moa.job.list():
        print job

def listTemplatesLong(data):
    for job, info in moa.job.listLong():
        for line in textwrap.wrap(
            '%s: %s' % (job, info),
            initial_indent=' - ',
            subsequent_indent = '     '):
            print line

def rawInfo(data):
    pprint.pprint(moa.info.info(data['cwd']))

def status(data):
    print moa.info.status(data['cwd'])

def template(data):
    print moa.info.getTemplateName(data['cwd'])
