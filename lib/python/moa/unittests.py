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

from moa.logger import l, setSilent, setInfo, setVerbose

import moa.lock
import moa.api
import moa.info
import moa.conf
import moa.utils
import moa.job

MOABASE = os.environ['MOABASE']

failures = 0
tests = 0

templateFailures = 0
templateTests = 0

TESTGLOB = {
    'MOABASE' : MOABASE,
    'P_TEST' : os.path.join(MOABASE, 'test', '00.base', '99.test'),
    'P_EMPTY' : os.path.join(MOABASE, 'test', '00.base', '00.empty'),
    'P_JOB' : os.path.join(MOABASE, 'test', '00.base', '10.moa.job'),
    'P_LOCKEDJOB' : os.path.join(MOABASE, 'test', '00.base', '20.moa.locked'),
    }

def testModule(m):
    global failures
    global tests
    f, t = doctest.testmod(m, extraglobs = TESTGLOB)
    failures += f
    tests += t
    
def testTemplates():
    global templateFailures
    global templateTests
    testDir = os.path.join(MOABASE, 'test', '00.base', '99.test')    
    for templateFile in os.listdir(os.path.join(MOABASE, 'template')):
        
        if not templateFile[-3:] == '.mk': continue
        if templateFile[:2] == '__': continue
        if templateFile[:7] == 'moaBase': continue
           
        template = templateFile[:-3]        
        l.debug("testing template %s" % template)
        templateTests  += 1
        
        moa.api.removeMoaFiles(testDir)
        moa.api.newJob(template = template, wd=testDir,
                       title='Testing template %s' % template)
        rc = moa.api.runMoa(wd=testDir, target='template_test', 
                            background=False)
        if rc != 0:
            templateFailures += 1
            err = moa.api.getMoaErr(wd=testDir)
            l.error("Error running template test for template %s" % template)
            l.error(err)
            
        result = moa.api.getMoaOut(wd=testDir).strip()
        if result:
            print result
        
def run(options, args):
    l.info("Start running python doctests")
    setSilent()
    testModule(moa.utils)
    testModule(moa.lock)
    testModule(moa.api)
    testModule(moa.info)
    testModule(moa.conf)
    testModule(moa.job)
    testModule(moa.runMake)
    if options.verbose:
        setVerbose()
    else:
        setInfo()
    l.info("Finished running of python unittests")
    l.info("Ran %d test, %d failed" % (tests, failures))
    l.info("Start running basic template tests")
    testTemplates()
    l.info("Finished running basic template tests")
    


