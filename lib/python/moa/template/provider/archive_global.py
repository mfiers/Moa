# Copyright 2009-2011 Mark Fiers
# The New Zealand Institute for Plant & Food Research
# 
# This file is part of Moa - http://github.com/mfiers/Moa
# 
# Licensed under the GPL license (see 'COPYING')
# 
"""
moa.provider.core
-----------------

Provides archived moa jobs (as templates) from a global directory

"""
import os
import sys
import shutil
import tarfile

import Yaco

import moa.utils
import moa.logger as l

from moa.sysConf import sysConf
from moa.template import provider
from moa.template.provider.archive import Archive

class Archive_global(Archive):

    def __init__(self, name, data):
        super(Archive_global, self).__init__(name, data)
        self.directory = os.path.join(
            moa.utils.getMoaBase(),
            'archive')
