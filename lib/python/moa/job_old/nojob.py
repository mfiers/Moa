#!/usr/bin/env python
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
Job
"""

import os
import re
import sys
import tempfile

import moa.utils
import moa.logger as l
import moa.conf
import moa.template
import moa.utils
import moa.runMake

from moa.job.base import BaseJob

MOABASE = moa.utils.getMoaBase()

class NoJob(BaseJob):

    """
    No job in this directory class :)
    """
    
    def __init__(self, wd):
        super(NoJob, self).__init__(wd)

    def isMoa(self):        
        """
        Is the job directory a Moa directory

        >>> job = Job('/')
        >>> job.isMoa()
        False
        >>> import moa.job
        >>> jobdir = moa.job.newTestJob('traverse')

        """
        return False
