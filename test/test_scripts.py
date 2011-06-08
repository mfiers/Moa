import os
import shutil
import random
import tempfile
import subprocess
import unittest2 as unittest

def load_tests(loader, tests, ignore):
    tests.addTests(scriptTestSuite())
    return tests

class scriptTester(unittest.TestCase):
    
    def setScript(self, name, script):
        self.name = name
        self.script = script

    def runTest(self):
        if not hasattr(self, 'script'):
            # only test if a job is set
            # hence, only if it is called by RuffSuite()
            return
        d = tempfile.mkdtemp()
        shutil.copy(self.script, d)
        
        scriptBase = os.path.basename(self.script)
        P = subprocess.Popen(
            [os.path.join(d, scriptBase)], cwd = d,
            stdout = subprocess.PIPE,
            stderr = subprocess.PIPE)
        out, err = P.communicate()
        rc = P.returncode
        if not rc == 0:
            print "error executing %s" % self.name
            if err.strip():
                print "stderr" + '-' * 70
                print err
            if out.strip():
                print "stdout" + '-' * 70
                print out

        shutil.rmtree(d)
        self.assertEqual(rc, 0)
        
    

def scriptTestSuite():
    suite = unittest.TestSuite()
    scriptDir = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        'scripts')

    for path, dirs, files in os.walk(scriptDir):
        for f in files:
            if f[-3:] != '.sh': continue            
            scriptPath = os.path.join(path, f)
            scriptName = scriptPath.replace(scriptDir, '')
            tester = scriptTester()
            tester.setScript(scriptName, scriptPath)
            suite.addTest(tester)
    return suite
    
if __name__ == '__main__':
    unittest.main()
