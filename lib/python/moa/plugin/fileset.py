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

"""

import re
import os
import sys
import readline
import moa.ui
import moa.conf
import moa.utils
import moa.logger as l


def prepare(data):
    l.debug("running fileset prepare")
    job = data['job']

TESTSCRIPT = """
moa new adhoc -t 'something'
moa set title='something else'
moa set undefvar='somewhat'
moa set adhoc_mode=par
moa show || exer moa show does not seem to work
moa show | grep -q 'title[[:space:]\+]else' || exer title is not set properly
moa set title+=test
moa show | grep -q 'title[[:space:]\+]else test' || exer title is not set properly
"""
