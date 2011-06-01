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
import optparse
import doctest
import tempfile
import subprocess

import Queue
import threading

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

#sysConf = None
sysConf = moa.sysConf.sysConf

def hook_defineCommands():
    sysConf['commands']['unittest'] = {
        'desc' : 'Run Moa unittests',
        'call' : runTests,
        'needsJob' : False,
        'loglevel' : 1
        }

def hook_defineOptions():
    try:
        parserN = optparse.OptionGroup(sysConf['parser'], "moa unittest")
        parserN.add_option("-j", dest="threads",
                           help="No threads to use", default=1,
                           type="int")
        parserN.add_option("--uv", dest="showOutput",
                           help="Show test output", default=False,
                           action='store_true')
        sysConf['parser'].add_option_group(parserN)
    except optparse.OptionConflictError:
        pass

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
templateRawTests = 0
templateTests = 0

pluginFailures = 0
pluginTests = 0

templateq = Queue.Queue()

def _templateTester():
    global templateTests
    global templateFailures
    while True:
        job = templateq.get()
        rc = 0
        template = job.template
        options = sysConf.options
        tname = template.name
        testDefined = True
        job.prepare()
        l.debug('Testing template %s' % tname)            
        if template.backend == 'gnumake':
            setSilent()
            rc = job.execute(
                '%s_unittest' % tname,
                verbose = options.verbose,
                silent = not options.verbose)
            resetSilent()
            err = moa.actor.getLastStderr(job)
            if 'No rule to make target' in err:
                testDefined = False
                rc = -1
            else:                
                templateTests += 1
                
        elif template.backend == 'ruff':
            if job.hasCommand('unittest'):
                setSilent()
                rc = job.execute('unittest',
                                 verbose = options.verbose,
                                 silent = not options.verbose)
                resetSilent()
                script = job.backend.commands.unittest.script
                templateTests += len([x for x in script.strip().split("\n") if x])
            else:
                testDefined = False
        else:
            l.warning("job %s has no backend (%s)" % (tname, template.backend))
            rc = -1

        if not testDefined:
            l.warning("template %s has no unittest defined" % tname)
        elif rc != 0:
            l.warning("Error testing template %s (rc %d)" % (tname, rc))
            templateFailures += 1
        else:
            l.info("Success testing template %s" % tname)
            
        if sysConf.options.showOutput:
            out = moa.actor.getLastStdout(job)
            err = moa.actor.getLastStderr(job)
            if out:
                l.warning("Stdout\n" + out)
            if err:
                l.warning("Stderr\n" + err)
        templateq.task_done()
    
def testTemplates(options, args=[]):

    l.info("Start running template tests")

    failures, tests, tcount = 0, 0, 0

    for i in range(sysConf.options.threads):
        t = threading.Thread(target=_templateTester)
        t.daemon = True
        t.start()
        
    for tname in moa.template.templateList():
        if args and not tname in args:
            continue
        job = moa.job.newTestJob(tname)
        templateq.put(job)

    templateq.join()
    #l.info("Ran %d test for %d template(s), %d failed" % (
    #    templateTests, tcount, failures))
        


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

        
    
