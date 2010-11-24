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
Pre & Post commands
-------------------

Allow execution of a bash oneline before & after job completion
"""

import os

import moa.ui
import moa.utils
import moa.logger as l
import moa.template


def prepare(data):
    job = data['job']

    job.template.parameters.precommand = {
        'category' : 'advanced',
        'optional' : True,
        'help' : 'A single command to be executed before the main run' + \
                 'starts',
        'type' : 'string'
        }
    job.template.parameters.postcommand = {
        'category' : 'advanced',
        'optional' : True,
        'help' : 'A single command to be executed after the main run ' + \
                 'starts',
        'type' : 'string'
        }


def preRun(data):
    """
    If defined, execute the precommand
    """
    job = data['job']
    precommand = job.conf['precommand']
    if not precommand: return
    os.system(precommand)
