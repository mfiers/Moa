import random
import unittest2 as unittest
import doctest

import moa.job
import moa.utils
import moa.template
import moa.template.template

def load_tests(loader, tests, ignore):
    tests.addTests(doctest.DocTestSuite(moa.job))
    tests.addTests(doctest.DocTestSuite(moa.utils))
    tests.addTests(doctest.DocTestSuite(moa.template))
    tests.addTests(doctest.DocTestSuite(moa.template.template))
    return tests

if __name__ == '__main__':
    unittest.main()
