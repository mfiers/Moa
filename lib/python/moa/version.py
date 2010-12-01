# 
# Copyright 2009, 2010 Mark Fiers
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

import os
import sys

import moa.logger as l
import moa.job

## Quick fix - see if this is an old style moa job
def fixOld(wd):
    makefile = os.path.join(wd,'Makefile')
    if not os.path.exists(makefile): return False
    
    with open(makefile) as F:
        t = F.read()
    if not 'include $(MOABASE)/template/moa/prepare.mk' in t:
        return False

    import shutil

    l.warning("Old style Makefile trying to upgrade!")
    
    t = t.replace('/template/moa/', '/lib/gnumake/')
    
    if os.path.exists('%s.old' % makefile):
        os.unlink('%s.old' % makefile)
    shutil.move(makefile,'%s.old' % makefile)
    with open('%s' % makefile, 'w') as F:
        F.write(t)
        
    templateName = t.split('moa_load,')[1].replace(')','').strip()
    l.warning("Found a makefile with template %s" % templateName)
    cdir = os.path.join(wd, '.moa')
    if not os.path.exists(cdir): os.mkdir(cdir)
    
    l.warning("wrote an updated Makefile - please check!")
    with open(os.path.join(cdir, 'template'), 'w') as F:
        F.write(templateName)

    moamk = os.path.join(wd, 'moa.mk')
    if not os.path.exists(moamk): return
    
    #create a regular job
    l.info("create a new style %s job" % templateName)
    job = moa.job.Job(wd)
    #convert moamk
    with open(moamk) as F:
        for line in F.readlines():
            line = line.strip()
            if '+=' in line:
                l.critical("Cannot autoconvert: %s" % line)
            k,v = line.split('=',1)
            l.info("found parameter %s=%s" % (k,v))
            if job.template.moa_id in k:
                k = k.replace('%s_' % job.template.moa_id, '')
                l.info("  -> saving to %s=%s" % (k,v))
            job.conf[k] = v
    l.info("saving configuration")
    job.conf.save()
    l.warning("converted moa.mk - please check %s/config" % cdir)
                
    sys.exit()
