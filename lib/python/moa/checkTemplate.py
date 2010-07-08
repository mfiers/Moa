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

import moa.logger as l
import moa.job

MOABASE = os.environ["MOABASE"]

def checkTemplate(path):
    """
    Run all current template tests - see if any needs updating

    All job Makefiles should look exactly alike and have only two
    lines of actual Makefile code:

    include $(MOABASE)/template/moa/prepare.mk
    
    $(call moa_load,emboss/revseq)

    """

    makefilePath = os.path.join(path, 'Makefile')

    if not os.path.exists(makefilePath):
        l.error("template check failed - cannot find a Makefile")

    seenIncludePrepare = False
    seenIncludeTemplate = False
    superfluousLines = False
    template = None
    
    makefile = open(makefilePath)
    i = 0
    nmf = []
    for line in makefile.readlines():
        line = line.strip()
        i += 1
        if not line: continue
        if line[0] == '#':
            nmf += line
            continue
        if line == 'include $(MOABASE)/template/moa/prepare.mk':
            nmf += line
            seenIncludePrepare = True
            continue
        if 'include $(MOABASE)/template/' in line:
            if template:
                l.error("Duplicate template include??")
                l.error("Please fix this!")
                sys.exit(-1)
            template = line.replace('include $(MOABASE)/template/', '')
            template = template.replace('.mk', '')
            l.debug("Discovered template %s" % template)
            continue
        if '$(call moa_load,' in line:
            if template:
                l.error("Duplicate template include??")
                l.error("Please fix this!")
                sys.exit(-1)
            seenIncludeTemplate = True
            template = line.replace('call moa_load,', '').replace(')', '').strip()
            l.debug("Discovered template %s" % template)
            continue
        if line in ['.PHONY: moa_preprocess', 'moa_preprocess:',
                    '.PHONY: moa_postprocess', 'moa_postprocess:',
                    '-include moa.mk', 'MOAMK_INCLUDE=done',
                    '@echo preprocess commands go here',
                    '@echo Postprocess commands go here..',
                    ]:
            continue
        
        superfluousLines = True
        l.info("extra code: '%s'" % line)
        
    if seenIncludePrepare and seenIncludeTemplate and (not superfluousLines):
        return True

    if superfluousLines:
        l.error("Deprecated Makefile, discovered extra code")
        l.error("Please fix this manually")
        sys.exit(-1)

    l.error("Deprecated template, fixing. Please check!")
    shutil.move(makefilePath, makefilePath + '.old')
    moa.job.newJob(template=template, wd=path,
                   noInit=True, titleCheck=False)
    sys.exit(0)

    
