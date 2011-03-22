# Copyright 2009-2011 Mark Fiers
# The New Zealand Institute for Plant & Food Research
# 
# This file is part of Moa - http://github.com/mfiers/Moa
# 
# Licensed under the GPL license (see 'COPYING')
# 
"""
**test** - Run unittests
------------------------
"""

import os
import sys

import moa.logger as l


import os
import sys
import doctest
import tempfile
import subprocess

import moa.logger as l
from moa.logger import setSilent, setInfo, setVerbose

#import moa.lock
import moa.utils
import moa.job
import moa.plugin
import moa.ui
import moa.sysConf
import moa.jobConf
import moa.template

def defineCommands(data):
    data['commands']['unittest'] = {
        'desc' : 'Run Moa unittests',
        'call' : runTests,
        'needsJob' : False
        }

def runTests(data):
    _run_test(data['options'], data['args'])


#####
##### private functions
##### 

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


def testModule(m):
    global failures
    global tests
    f, t = doctest.testmod(m)
    failures += f
    tests += t

def testTemplates(options, args=[]):
    global templateFailures
    global templateTests
    for tfile, tname in moa.template.listAll():
        if args and not tname in args:
            continue

        template = moa.template.Template(tfile)

        job = moa.job.newTestJob(tname)
        job.options = options
        job.prepare()
        l.info('testing template %s' % tname)

        if template.backend == 'gnumake':
            rc = job.execute('%s_unittest' % tname, 
                             verbose = options.verbose)
            err = moa.actor.getLastStderr(job)
            if 'No rule to make target' in err:
                l.warning("job %s has no unittest defined" % tname)
                continue
        else:                        
            if not job.hasCommand('unittest'):
                l.warning("job %s has no unittest defined" % tname)
                continue
            rc = job.execute('unittest', verbose = options.verbose)
            
        if rc != 0:
            l.critical("error testing template %s (rc %d)" % (tname, rc))
            out = moa.actor.getLastStdout(job)
            err = moa.actor.getLastStderr(job)
            if out:
                l.critical("Stdout\n" + out)
            if err:
                l.critical("Stderr\n" + err)
            templateFailures += 1
        elif args:
            out = moa.actor.getLastStdout(job)
            err = moa.actor.getLastStderr(job)
            if out:
                l.warning("Stdout\n    " +  "\n    ".join(out.split("\n")))
            if err:
                l.warning("Stderr\n    " +  "\n    ".join(err.split("\n")))
        templateTests += 1

            
    
def testPlugins(args=[]):
    global pluginFailures
    global pluginTests

    #new style plugin tests
    plugins = moa.plugin.PluginHandler(moa.sysConf.getPlugins())
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
        elif args:
            if out: l.info("Stdout:\n" + out)
            if err: l.info("Stderr:\n" + err)
           
        l.info("Success testing %s (%d lines)" % (
            plugin, len(testCode.strip().split("\n"))))
        pluginTests += 1
    
def _run_test(options, args):

    #remove the first argument from args (should be 'test')
    args.pop(0)

    os.putenv('MOA_UNITTESTS', "yes")
    os.putenv('MOA_NOLOGO', "1")
    if args:
        l.info("Testing '%s'" % " ".join(args))

    if not args:
        l.info("Start running python doctests")
        setSilent()        
        testModule(moa.utils)
        testModule(moa.template)
        testModule(moa.job)
        testModule(moa.ui)
        testModule(moa.sysConf)
        testModule(moa.jobConf)
        
        if options.verbose: setVerbose()
        else: setInfo()
        
        l.info("Finished running of python unittests")
        l.info("Ran %d test, %d failed" % (tests, failures))
        
        l.info("Start running plugin tests")
        testPlugins()
        l.info("Ran %d plugin test, %d failed" % (
                pluginTests, pluginFailures))
        l.info("Finished running plugin tests")

        l.info("start running template tests")
        testTemplates(options)
        l.info("Finished running template tests")
        sys.exit()

    elif args[0] == 'plugins':
        l.info("Start running plugin tests")
        testPlugins(args[1:])
        l.info("Ran %d plugin test, %d failed" % (
                pluginTests, pluginFailures))
        l.info("Finished running plugin tests")

    elif args[0] == 'templates' or args[0] == 'template':
        l.info("Start running template tests")
        testTemplates(options, args[1:])        
        l.info("Ran %d template test, %d failed" % (
                templateTests, templateFailures))
        l.info("Finished running template tests")

    elif args[0] == 'plugin':
        l.info("Start running plugin tests")
        testPlugins(args[1:])

    elif args[0][:4] == 'moa.':            
        l.info("testing moa python module %s" % args[0])
        setSilent()
        eval("testModule(%s)" % args[0])
        if options.verbose: setVerbose()
        else: setInfo()
        l.info("Finished running unittests for %s" % args[0])
        l.info("Ran %d test, %d failed" % (tests, failures))
    else:
        l.error("sorry - cannot parse the command line")

        
    
