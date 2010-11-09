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
import tempfile
import subprocess

import moa.logger as l
from moa.logger import setSilent, setInfo, setVerbose

import moa.lock
import moa.conf
import moa.utils
import moa.job
import moa.plugin
import moa.project
import moa.template

MOABASE = moa.utils.getMoaBase()

TESTSCRIPTHEADER = """
set -e

function exer {
echo "PLUGIN TEST
ERROR: $*" 1>&2
exit -1
}

"""

failures = 0
tests = 0

templateFailures = 0
templateTests = 0

pluginFailures = 0
pluginTests = 0

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
    
def testPlugins(args=[]):
    global pluginFailures
    global pluginTests

    #new style plugin tests
    plugins = moa.plugins.Plugins()
    for plugin, testCode in plugins.getAttr('TESTSCRIPT'):

        #if asking for a single plugin, test only that plugin
        if args and plugin not in args: continue
        
        l.info("Starting new style test of %s" % plugin)
        testDir = tempfile.mkdtemp()
        testScript = os.path.join(testDir, 'test.sh')
        with open(testScript, 'w') as F:
            F.write(TESTSCRIPTHEADER)
            F.write(testCode)
        l.debug("executing test.sh in %s" % testScript)
        p = subprocess.Popen('bash %s' % testScript,
                             shell=True,
                             cwd = testDir,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE,
                             close_fds=True)
        out, err = p.communicate()
        rc = p.returncode
        if rc != 0:
            l.critical("Errors in plugin test %s (rc %d)" % (plugin, rc))
            if out: l.critical("Stdout:\n" + out)
            if err: l.critical("Stderr:\n" + err)
            pluginFailures += 1
        else: 
            if out: l.debug("Stdout:\n" + out)
            if err: l.info("Stderr:\n" + err)
           
        l.info("Success testing %s (%d lines)" % (
            plugin, len(testCode.strip().split("\n"))))
        pluginTests += 1
    
def run(options, args):

    #remove the first argument from args (should be 'test')
    args.pop(0)

    os.putenv('MOA_UNITTESTS', "yes")
    if args:
        l.info("Testing '%s'" % " ".join(args))

    if not args:
        l.info("Start running python doctests")
        setSilent()        
        testModule(moa.utils)
        testModule(moa.lock)
        testModule(moa.conf)
        testModule(moa.project)
        testModule(moa.template)
        testModule(moa.job)
        
        if options.verbose: setVerbose()
        else: setInfo()
        
        l.info("Finished running of python unittests")
        l.info("Ran %d test, %d failed" % (tests, failures))
        
        l.info("Start running basic template tests")
        testTemplates()
        l.info("Ran %d template test, %d failed" % (
                templateTests, templateFailures))

        l.info("Start running plugin tests")
        testPlugins()
        l.info("Ran %d plugin test, %d failed" % (
                pluginTests, pluginFailures))
        l.info("Finished running plugin tests")
        sys.exit()

    elif args[0] == 'plugins':
        l.info("Start running plugin tests")
        testPlugins(args[1:])
        l.info("Ran %d plugin test, %d failed" % (
                pluginTests, pluginFailures))
        l.info("Finished running plugin tests")
    elif args[0] == 'plugin':
        l.info("Start running plugin tests")
        testPlugins(args[1:])
    elif args[0] == 'templates':
        l.info("Start running basic template tests")
        testTemplates()
        l.info("Ran %d template test, %d failed" % (
            templateTests, templateFailures))
        l.info("Finished running basic template tests")
    elif args[0][:4] == 'moa.':            
        l.info("testing moa python module %s" % args[0])
        setSilent()
        eval("testModule(%s)" % args[0])
        if options.verbose: setVerbose()
        else: setInfo()
        l.info("Finished running unittests for %s" % args[0])
        l.info("Ran %d test, %d failed" % (tests, failures))
    else:
        #Assume it is a templat
        testTemplates(args[0], verbose=options.verbose)
        testTemplateExtensive(args[0], verbose=options.verbose)

        
    
