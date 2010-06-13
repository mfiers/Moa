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
from moa.logger import l
import textwrap

class Info(moa.plugin.BasePlugin):

    def registerCommands(self):
        self.data['moaCommands']['rawinfo'] = {
            'private' : True,
            'call' : rawInfo
            }

        self.data['moaCommands']['status'] = {
            'private' : True,
            'call' : self.status
            }

        self.data['moaCommands']['show'] = {
            'desc' : 'Show the configured parameters and their values',
            }

        self.data['moaCommands']['list'] = {
            'desc' : 'List all known templates',
            'call' : self.listTemplates,
            }

        self.data['moaCommands']['listlong'] = {
            'desc' : 'List all known templates, showing a short description',
            'call' : self.listTemplatesLong,
            }


    def listTemplates(self, wd, options, args):
        for job in moa.job.list():
            print job

    def listTemplatesLong(self, wd, options, args):
        for job, info in moa.job.listLong():
            for line in textwrap.wrap(
                '%s: %s' % (job, info),
                initial_indent=' - ',
                subsequent_indent = '     '):
                print line

    def rawInfo(self, wd, options, args):
        pprint.pprint(moa.info.info(wd))

    def status(self, wd, options, args):
        print moa.info.status(wd)

def defineCommands(commands):
    commands['rawinfo'] = {
        'private' : True,
        'call' : rawInfo
        }

    commands['status'] = {
        'private' : True,
        'call' : status
        }

    commands['show'] = {
        'desc' : 'Show the configured parameters and their values',
        }

    commands['list'] = {
        'desc' : 'List all known templates',
        'call' : listTemplates,
        }

    commands['listlong'] = {
        'desc' : 'List all known templates, showing a short description',
        'call' : listTemplatesLong,
        }

def listTemplates(wd, options, args):
    for job in moa.job.list():
        print job

def listTemplatesLong(wd, options, args):
    for job, info in moa.job.listLong():
        for line in textwrap.wrap(
            '%s: %s' % (job, info),
            initial_indent=' - ',
            subsequent_indent = '     '):
            print line

def rawInfo(wd, options, args):
    pprint.pprint(moa.info.info(wd))

def status(wd, options, args):
    print moa.info.status(wd)
