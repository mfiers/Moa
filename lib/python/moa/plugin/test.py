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
import logging

import os
import sys
import doctest
import tempfile
import subprocess

from moa.logger import setLevel

#import moa.lock
import moa.ui
import moa.job
import moa.utils
import moa.plugin
import moa.sysConf
import moa.jobConf
import moa.commands
import moa.template

import Yaco

sysConf = moa.sysConf.sysConf

def defineCommands(data):
    data['commands']['unittest'] = {
        'desc' : 'Run Moa unittests',
        'call' : runTests,
        'needsJob' : False,
        'loglevel' : 1
        }

#####
##### private functions
##### 

MOABASE = moa.utils.getMoaBase()

TESTSCRIPTHEADER = '''
set -e

function exer {
echo "PLUGIN TEST
ERROR: $*" 1>&2
exit -1
}

'''

def setSilent():
    global testLogLevel
    setLevel(testLogLevel)

def resetSilent():
    global globalLogLevel
    setLevel(globalLogLevel)


testdata = Yaco.Yaco()

globalLogLevel = logging.INFO
testLogLevel = logging.WARNING

failures = 0
tests = 0

templateFailures = 0
templateTests = 0

pluginFailures = 0
pluginTests = 0

def testTemplates(options, args=[]):

    l.info("Start running template tests")

    failures, tests, tcount = 0, 0, 0
    
    for tname in moa.template.templateList():
        if args and not tname in args:
            continue
        
        job = moa.job.newTestJob(tname)
        template = job.template
        job.options = options
        job.prepare()
        l.info('Testing template %s' % tname)            
        if template.backend == 'gnumake':
            
            setSilent()
            rc = job.execute('%s_unittest' % tname, 
                             verbose = options.verbose,
                             silent = not options.verbose)
            resetSilent()
            err = moa.actor.getLastStderr(job)
            if 'No rule to make target' in err:
                l.warning("job %s has no unittest defined" % tname)
                continue
            tests += 1
        elif template.backend == 'ruff':
            if not job.hasCommand('unittest'):
                l.warning("job %s has no unittest defined" % tname)
                continue
            setSilent()
            rc = job.execute('unittest',
                             verbose = options.verbose,
                             silent = not options.verbose)
            resetSilent()
            script = job.backend.commands.unittest.script
            tests += len([x for x in script.strip().split("\n") if x])
        else:
            l.warning("job %s as no known backend  %s" % (tname, template.backend))
            continue

            rc = -1
        tcount += 1
        
        if rc != 0:
            l.critical("error testing template %s (rc %d)" % (tname, rc))
            out = moa.actor.getLastStdout(job)
            err = moa.actor.getLastStderr(job)
            if out:
                l.critical("Stdout\n" + out)
            if err:
                l.critical("Stderr\n" + err)
            failures += 1
        elif args:
            out = moa.actor.getLastStdout(job)
            err = moa.actor.getLastStderr(job)
            if out:
                l.warning("Stdout\n    " +  "\n    ".join(out.split("\n")))
            if err:
                l.warning("Stderr\n    " +  "\n    ".join(err.split("\n")))
                
    l.info("Ran %d test for %d template(s), %d failed" % (
        tests, tcount, failures))
        


def testCommands(args=[]):

    l.info("Start running command tests")

    commandCount = 0
    testCount = 0
    failureCount = 0
    
    for c in sysConf.commands.getAll():
        if (len(args) > 0) and (not c in args):
            l.debug("skipping command test %s" % c)
            continue
        cinfo = sysConf.commands[c]
        if not cinfo.has_key('unittest'):
            l.warning("No unittest for command %s" % c)
            continue
        commandCount += 1
        cut = cinfo['unittest']
        rc = _testScript('command %s' % c, cut, len(args) > 0)
        testCount += len([x for x in cut.split("\n") if x])
        if rc != 0:
            failureCount += 1

    l.info("Ran %d test for %d command(s), %d commands failed" % (
        testCount, commandCount, failureCount))



def _testScript(name, script, showOutput):

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
    elif showOutput:
        l.info("Success testing %s" % name)
        if out: l.warning("Stdout:\n" + out)
        if err: l.warning("Stderr:\n" + err)
    else:
        l.info("Success testing %s" % name)
        if out: l.debug("Stdout:\n" + out)
        if err: l.debug("Stderr:\n" + err)

    return rc




def testModule(m):
    setSilent()
    f, t = doctest.testmod(m)
    resetSilent()
    return f, t
    
def runDocTests(args=[]):
    tests, failures = 0, 0

    l.info("Start running python doctests")
    for m in 'utils template job  ui sysConf jobConf'.split():
        if not args or 'moa.' + m in args:
            f, t = eval('testModule(moa.%s)' % m)
            tests += t; failures += f
    
    l.info("Finished running %d python doctests, %d failed" % (
        tests, failures))
    
    
def runTests(job):

    options = sysConf.options
    args = sysConf.newargs

    os.putenv('MOA_UNITTESTS', "yes")
    os.putenv('MOA_NOLOGO', "1")

    if options.verbose:
        testLogLevel = logging.DEBUG
        globalLogLevel = logging.DEBUG
    else:
        testLogLevel = logging.CRITICAL
        globalLogLevel = logging.INFO
        
    if not args:

        runDocTests()
        testCommands()
        testTemplates(options)

    elif args[0][:3] == 'com':
        testCommands(args[1:])

    elif args[0][:3] == 'doc':
        runDocTests(args[1:])

    elif args[0][:3] == 'tem':
        testTemplates(options, args[1:])        

    elif args[0][:4] == 'moa.':
        runDocTests(args[0:])
    else:
        moa.ui.exitError("Uncertain what to test - try `moa unittest`")

        
    
