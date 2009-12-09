#!/usr/bin/env python

import os
import re
import sys
import shutil
import optparse
import unittest
import tempfile
import subprocess

parser = optparse.OptionParser()
parser.add_option('-v', dest='verbose', action='count')
options, args = parser.parse_args()

def checkCall(script, wd):
    rcl = open(script).read()
    rcl = """
        cd %s
        set -e
        xx() {
          echo 'Error executing ' !-1;
          echo $1;
          false;
        }
        """ % wd + rcl

    stdout = subprocess.PIPE
    stderr = subprocess.PIPE

    if options.verbose > 0:
        stderr = None

    if options.verbose > 1:
        stdout = None

    if options.verbose > 2:
        print "\n" + '-' * 80
        print "Executing:\n" + rcl
        
    p = subprocess.Popen(
        rcl, executable='/bin/bash', shell=True,
        stdout = stdout, stderr = stderr)

    out, err = p.communicate()

    retcode = p.returncode
    if retcode == 0: return True, ""

    message = out.strip().rsplit("\n", 1)[-1]
    return False, message

_scriptMatchRe = re.compile("([0-9]{3})\.(.*)\.sh$")
def _scriptTestDecorator(c):
    for f in os.listdir(c.testFolder):
        check = _scriptMatchRe.match(f)
        if not check: continue 
        func = eval('lambda self: self._test("%s")' % f)
        setattr(c, "test_%s_%s" % check.groups(), func)
    return c

class _scriptTest(unittest.TestCase):
    testFolder = ""
    def _test(self, _file):
        result, message =  checkCall(
            os.path.join(self.testFolder, _file),
            self.tempdir)
        self.failUnless(result, message)

    def setUp(self):
        """ Create a folder where we can experiment """
        self.tempdir = tempfile.mkdtemp(suffix='.testmoa')
         
    def tearDown(self):
        """ remove the temp folder"""
        shutil.rmtree(self.tempdir)
    
TESTCLASSTEMPLATE = """
@_scriptTestDecorator
class MoaTest_%(name)s(_scriptTest):
    testFolder = '%(path)s'
"""

testfolder = os.walk(os.path.join(os.environ['MOABASE'], 'test', 'scripts'))
for path, dirnames, filename in testfolder:
    if path == testfolder: continue
    if args and (not args[0] in path): continue
    name = path.replace('/', "_").replace('.', '_')
    exec(TESTCLASSTEMPLATE % locals())


if __name__ == '__main__':
    tests = [x for x in globals().keys() if x[:8] == 'MoaTest_']
    tests.sort()
    for t in tests:
        print "Running %s" % t
        suite = unittest.TestLoader().loadTestsFromTestCase(globals()[t])
        unittest.TextTestRunner(verbosity=options.verbose).run(suite)
