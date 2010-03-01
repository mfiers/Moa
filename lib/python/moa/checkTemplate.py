# Copyright 2009 Mark Fiers, Plant & Food Research
# 
# This file is part of Moa - http://github.com/mfiers/Moa
# 
# Moa is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your
# option) any later version.
# 
# Moa is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
# or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public
# License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with Moa.  If not, see <http://www.gnu.org/licenses/>.
# 
"""
 Check template - checks templates for old style templates and tries
to update them 
"""

import os
import re
import sys
import subprocess

from moa.logger import l
from moa import runMake
from moa.exceptions import *
import moa.utils
import moa.lock

MOABASE = os.environ["MOABASE"]



def checkTemplate(path):
    """
    Run all current template tests - see if any needs updating
    """

    _check_deprecated_001(path)



##
## Check for deprecated style makefile
##
def _check_deprecated_001(path):

    makefile = os.path.join(path, 'Makefile')


    _check = subprocess.Popen("cat %s 2>/dev/null |grep dont_include_moabase " % makefile,
                              shell=True,
                              stdout=subprocess.PIPE).communicate()[0].strip()    
    if 'dont_include_moabase' in _check:
        includeline=re.compile(r'include \$\(shell echo \$\$MOABASE\)/template/.*\.mk$')
        l.warning("Old style Makefile in %s, automatically updating!" % makefile)
        l.warning("The old Makefile will be copied to Makefile.old")
        shutil.move(makefile, makefile + '.old')
        F = open(makefile + '.old')
        G = open(makefile,  'w')
        count_includes = 0
        dim_removed = False
        imb_removed = False
        for line in F.readlines():
            if re.match('^dont_include_moabase=.*$', line.strip()):
                dim_removed = True
                l.debug("Removing %s" % line)
                continue
            if line.strip() == 'include $(shell echo $$MOABASE)/template/__moaBase.mk':
                imb_removed = True
                l.debug("Removing %s" % line)
                continue
            if includeline.match(line.strip()):
                l.debug("found an include line")
                l.debug(line)
                count_includes += 1

            line = line.replace('$(shell echo $$MOABASE)', '$(MOABASE)')
            G.write(line)
        F.close()
        G.close()
        if count_includes > 1:
            l.critical("This makefile might NOT work - including more than one template")
            l.critical("is not allowed (anymore :( )")
            sys.exit(1)
        if count_includes == 0:
            l.warning("Odd - you dont' seem to be including any template, have a look")
            sys.exit(1)
        if not dim_removed and imb_removed:
            l.error("Updated Makefile - unsure of success - please check")
            sys.exit(1)
        l.error("Updated Makefile - everything looks fine (check anyway)")
        sys.exit()


