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
from moa.logger import setSilent, setWarning, setInfo, setVerbose

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

commandFailures = 0
commandTests = 0


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
                             verbose = options.verbose,
                             silent = not options.verbose)
            err = moa.actor.getLastStderr(job)
            if 'No rule to make target' in err:
                l.warning("job %s has no unittest defined" % tname)
                continue
        else:                        
            if not job.hasCommand('unittest'):
                l.warning("job %s has no unittest defined" % tname)
                continue
            rc = job.execute('unittest',
                             verbose = options.verbose,
                             silent = not options.verbose)
            
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


def testCommands(data):
    global commandTests
    global commandFailures
    
    args = data.args
    args.pop(0)

    for c in data.commands:
        if (len(args) > 0) and (not c in args):
            l.debug("skipping command test %s" % c)
            continue
        cinfo = data.commands[c]
        if not cinfo.has_key('unittest'):
            l.warning("No unittest for command %s" % c)
            continue
        cut = cinfo['unittest']
        rc = _testScript('command %s' % c, cut, len(args) > 0)
        commandTests += 1
        if rc != 0:
            commandFailures += 1

def _testScript(name, script, output_warning=False):
    testDir = tempfile.mkdtemp()
    testScript = os.path.join(testDir, 'test.sh')
    with open(testScript, 'w') as F:
        F.write(TESTSCRIPTHEADER)
        F.write(script)
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
        l.critical("Error testing %s (rc %d)" % (name, rc))
        if out: l.critical("Stdout:\n" + out)
        if err: l.critical("Stderr:\n" + err)
    elif output_warning:
        l.critical("Success testing %s" % name)
        if out: l.warning("Stdout:\n" + out)
        if err: l.warning("Stderr:\n" + err)
    else:
        l.warning("Success testing %s" % name)
        if out: l.info("Stdout:\n" + out)
        if err: l.info("Stderr:\n" + err)           
    return rc
    
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

def runDocTests():
    testModule(moa.utils)
    testModule(moa.template)
    testModule(moa.job)
    testModule(moa.ui)
    testModule(moa.sysConf)
    testModule(moa.jobConf)

def runTests(data):

    options = data['options']
    args = data['args']

    args.pop(0)

    os.putenv('MOA_UNITTESTS', "yes")
    os.putenv('MOA_NOLOGO', "1")
    if args:
        l.info("Testing '%s'" % " ".join(args))

    if not args:
        l.info("Start running python doctests")
        
        setWarning()        
        runDocTests()
        if options.verbose: setVerbose()
        else: setInfo()
        
        l.info("Ran %d test, %d failed" % (tests, failures))

        l.info("Start running command tests")
        testCommands(data)
        l.info("Ran %d command tests, %d failed" % (
                commandTests, commandFailures))

        
        l.info("Start running plugin tests")
        testPlugins()
        l.info("Ran %d plugin test, %d failed" % (
                pluginTests, pluginFailures))

        l.info("start running template tests")
        testTemplates(options)
        sys.exit()

    elif args[0][:3] == 'com':
        setWarning()
        testCommands(data)
        if options.verbose: setVerbose()
        else: setInfo()
        l.info("Finished running of python command tests")
        l.info("Tested %d commands, %d failed" % (commandTests, commandFailures))

    elif args[0] == 'doctests':

        setWarning()        
        runDocTests()
        if options.verbose: setVerbose()
        else: setInfo()

        l.info("Finished running of python unittests")
        l.info("Ran %d doctests, %d failed" % (tests, failures))
        
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
        setWarning()
        eval("testModule(%s)" % args[0])
        if options.verbose: setVerbose()
        else: setInfo()
        l.info("Finished running unittests for %s" % args[0])
        l.info("Ran %d test, %d failed" % (tests, failures))
    else:
        l.error("sorry - cannot parse the command line")

        
    
