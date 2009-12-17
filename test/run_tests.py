#!/usr/bin/env python

import os
import re
import sys
import site
import optparse
import doctest

#moa specific libs - first prepare for loading libs
if not os.environ.has_key('MOABASE'):
    raise Exception("MOABASE is undefined")

#process the .pth file in the $MOABASE/bin folder !
site.addsitedir(os.path.join(os.environ['MOABASE'], 'lib', 'python'))

MOABASE = os.environ["MOABASE"]

import moa.api

if __name__ == "__main__":
    
    doctest.testmod(moa.api)
