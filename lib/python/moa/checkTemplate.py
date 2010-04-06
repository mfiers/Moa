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
import shutil
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

    makefilePath = os.path.join(path, 'Makefile')

    if not os.path.exists(makefilePath):
        l.error("template check failed - cannot find a Makefile")
    
    makefile = open(makefilePath).readlines()
    
    _check_deprecated_001(path, makefilePath, makefile)
    _check_deprecated_002(path, makefilePath, makefile)


##
## Make sure the $(call moa_load construct is used)
##
def _check_deprecated_002(path, makefilePath, makefile):
    for line in makefile:
        if not 'include $(MOABASE)' in line: continue
        if 'prepare.mk' in line: continue
        break
    else: return

    #if we're here - need to update the Makefile
    l.error("Fixing Makefile")
    shutil.move(makefilePath, makefilePath + '.old')
    F = open(makefilePath, 'w')
    for line in makefile:
        if ('include $(MOABASE)' in line) and (not 'prepare.mk' in line):
            line = line.replace('include $(MOABASE)/template/', '$(call moa_load,')\
                   .replace('.mk', ')')
        F.write(line)
    F.close()
    l.error("Updated old style Makefile - everything looks fine (check anyway!)")
    sys.exit()
    
        
        

##
## Check for deprecated style makefile
##
def _check_deprecated_001(path, makefilePath, makefile):

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


