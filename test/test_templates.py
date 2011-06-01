import random
import unittest2 as unittest
import doctest

import moa.job
import moa.plugin
import moa.template

import moa.backend.ruff.test
#import moa.backend.gnumake.test

from moa.sysConf import sysConf

pluginHandler = moa.plugin.PluginHandler()
sysConf.pluginHandler = pluginHandler

def load_tests(loader, tests, ignore):
    tests.addTests(templateTestSuite())
    return tests
    

def templateTestSuite():
    suite = unittest.TestSuite()
    for template in moa.template.templateList():
        job = moa.job.newTestJob(template)
        if job.template.backend == 'ruff':
            tester = moa.backend.ruff.test.templateTest()
            tester.setJob(job)
            suite.addTest(tester)
    return suite
    
if __name__ == '__main__':
    unittest.main()
