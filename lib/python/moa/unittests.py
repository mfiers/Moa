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
Unit tests
"""

import os
import sys
import doctest

from moa.logger import l, setSilent, setInfo

import moa.lock
import moa.api
import moa.info
import moa.conf
import moa.utils
import moa.job

MOABASE = os.environ['MOABASE']

failures = 0
tests = 0

TESTGLOB = {
    'MOABASE' : MOABASE,
    'TESTPATH' : os.path.join(MOABASE, 'demo', 'test'),
    'NOTMOADIR' : os.path.join(MOABASE, 'demo', 'test', 'notmoa'),
    'LOCKEDMOADIR' : os.path.join(MOABASE, 'demo', 'test', '20.locked.job'),
    'EMPTYDIR' : os.path.join(MOABASE, 'demo', 'test', 'empty.dir'),
    }

def testModule(m):
    global failures
    global tests
    f, t = doctest.testmod(m, extraglobs = TESTGLOB)
    failures += f
    tests += t

def run():
    l.info("Start running python doctests")

    setSilent()
    testModule(moa.utils)
    testModule(moa.lock)
    testModule(moa.api)
    testModule(moa.info)
    testModule(moa.conf)
    testModule(moa.job)
    testModule(moa.dispatch)
    setInfo()
    
    l.info("Finished running of unittests")
    l.info("Ran %d test, %d failed" % (tests, failures))
