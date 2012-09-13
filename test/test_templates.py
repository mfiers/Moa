import random
import unittest
import doctest

import moa.job
import moa.plugin
import moa.template

## Initialize the logger
import moa.logger
l = moa.logger.getLogger(__name__)

import moa.backend.ruff.test


from moa.sysConf import sysConf
sysConf.pluginHandler = moa.plugin.PluginHandler(sysConf.plugins.system)


def load_tests(loader, tests, ignore):
    tests.addTests(templateTestSuite())
    return tests


def templateTestSuite():
    suite = unittest.TestSuite()
    for provider, template in moa.template.templateList():
        job = moa.job.newTestJob(template, provider=provider)
        if job.template.backend == 'ruff':
            test = moa.backend.ruff.test.templateTest(job)
            suite.addTest(test)
    return suite

if __name__ == '__main__':
    unittest.main()
