#!/usr/bin/env python

import os
import sys
import shutil
import optparse
import unittest
import tempfile
import subprocess

parser = optparse.OptionParser()
parser.add_option('-v', dest='verbose', action='count')
options, args = parser.parse_args()

def checkCall(cl):
    rcl = cl
    stdout = subprocess.PIPE
    stderr = subprocess.PIPE

    if options.verbose > 2:
        print
        print '-' * 80
        print "Executing:"
        print rcl
        
    p = subprocess.Popen(
    rcl, executable='/bin/bash', shell=True,
    stdout = stdout, stderr = stderr)

    out,err = p.communicate()

    retcode = p.returncode
    if retcode == 0: return True
    else: return False


class _scriptTests(unittest.TestCase):
    testFolder = None

class MoaTest_01_Prereqs(unittest.TestCase):
    
    #general prerequisites
    def test_021_make_is_installed(self):
        """Find Make"""
        self.failUnless(checkCall("which make"))

    def test_022_gnu_make_is_installed(self):
        """Check GNU Make"""
        self.failUnless(checkCall('make --version | grep "GNU Make"'))

    def test_023_gnu_make_version(self):
        """Check GNU Make version 3"""
        self.failUnless(checkCall('make --version | grep "GNU Make 3"'))

    def test_024_bash(self):
        """Check Bash"""
        self.failUnless(checkCall('which bash'))

    def test_025_bash_version(self):
        """Check Bash version 4"""
        self.failUnless(checkCall('bash --version  | grep "GNU bash, version 4"'))
        
    def test_026_python(self):
        """Check Python"""
        self.failUnless(checkCall('which python'))

    def test_027_python_version(self):
        """Check Python version 2.6"""
        self.failUnless(checkCall('python --version 2>&1 | grep "Python 2.6"'))


class MoaTest_02_ScriptBasics(unittest.TestCase):

    def test_001_moabase_is_defined(self):
        """$MOABASE env var defined? """
        self.failUnless(os.environ.has_key('MOABASE'))

    def test_002_moa_etc_file(self):
        """Find moa.conf.mk"""
        etc_file=os.path.join(os.environ["MOABASE"], 'etc', 'moa.conf.mk')
        self.failUnless(os.path.exists(etc_file))
        
    def test_003_moa_executable_in_path(self):
        """Find moa script"""
        self.failUnless(checkCall("which moa"))

    def test_004_run_Moa_help(self):
        """Run moa --help"""
        self.failUnless(checkCall("moa --help"))

class MoaTest_10_MiniPipeline(unittest.TestCase):

    def setUp(self):
        """
        Create a folder where we can experiment
        """
        self.tempdir = tempfile.mkdtemp(suffix='.testmoa')

    def tearDown(self):
        """ remove the temp folder"""
        shutil.rmtree(self.tempdir)
        
    def test_AA_create_main_traverse(self):
        """Run moa new 'Test run' traverse"""
        testdir = self.tempdir
        r = checkCall('''
            cd %(testdir)s
            pwd
            moa new "Test run" traverse
            ls
            ''' % locals())
        self.failUnless(r)

        #check if moa.mk & Makefile exists
        moa_mk_file = os.path.join(self.tempdir, 'moa.mk')
        makefile_file = os.path.join(self.tempdir, 'Makefile')
        self.failUnless(os.path.exists(moa_mk_file), 'moa.mk is not created')
        self.failUnless(os.path.exists(makefile_file), 'Makefile is not created')
        
        r = checkCall('''
            cd %(testdir)s
            cat moa.mk
            cat moa.mk | grep "title=Test run"
            ''' % locals())

        self.failUnless(r, "title is not properly set")

    def test_BA_check_traverse_run(self):
        """Create a moa traverse and run it"""
        testdir = self.tempdir
        r = checkCall('''
            cd %(testdir)s
            pwd
            moa new 'Test run' traverse
            ls
            make
            ''' % locals())
        self.failUnless(r)

if __name__ == '__main__':
    tests = [x for x in globals().keys() if x[:8] == 'MoaTest_']
    tests.sort()
    for t in tests:
        print "Running %s" % t
        suite = unittest.TestLoader().loadTestsFromTestCase(globals()[t])
        unittest.TextTestRunner(verbosity=2).run(suite)
