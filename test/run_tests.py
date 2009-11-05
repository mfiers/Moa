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
          echo $1;
          false;
        }
        """ % wd + rcl

    stdout = subprocess.PIPE
    stderr = subprocess.PIPE

    if options.verbose > 2:
        print "\n" + '-' * 80
        print "Executing:\n" + rcl
        
    p = subprocess.Popen(
        rcl, executable='/bin/bash', shell=True,
        stdout = stdout, stderr = stderr)

    out,err = p.communicate()
    if options.verbose > 1:
        print '#OUT' * 10
        print out
    if options.verbose > 0:
        print '$ERR' * 10
        print err
        
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
    
@_scriptTestDecorator
class MoaTest_05_Prereqs(_scriptTest):
    testFolder = '05.prereqs'

@_scriptTestDecorator
class MoaTest_10_MoaBase(_scriptTest):
    testFolder = '10.moabase'

@_scriptTestDecorator
class MoaTest_10_MoaBase(_scriptTest):
    testFolder = '15.basic_pipeline'

#         r = checkCall('''
#             cd %(testdir)s
#             cat moa.mk
#             cat moa.mk | grep "title=Test run"
#             ''' % locals())

#         self.failUnless(r, "title is not properly set")

#     def test_BA_check_traverse_run(self):
#         """Create a moa traverse and run it"""
#         testdir = self.tempdir
#         r = checkCall('''
#             cd %(testdir)s
#             pwd
#             moa new 'Test run' traverse
#             ls
#             make
#             ''' % locals())
#         self.failUnless(r)

if __name__ == '__main__':
    tests = [x for x in globals().keys() if x[:8] == 'MoaTest_']
    tests.sort()
    for t in tests:
        print "Running %s" % t
        suite = unittest.TestLoader().loadTestsFromTestCase(globals()[t])
        unittest.TextTestRunner(verbosity=2).run(suite)
