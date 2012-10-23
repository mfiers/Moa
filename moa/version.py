# Copyright 2009-2011 Mark Fiers
# The New Zealand Institute for Plant & Food Research
# 
# This file is part of Moa - http://github.com/mfiers/Moa
# 
# Licensed under the GPL license (see 'COPYING')
# 
import re
import os
import sys
import shutil

import moa.logger as l
import moa.job
import moa.ui

## Quick fix - see if this is an old style moa job
def fixOld(wd):

    if os.path.exists(os.path.join(wd, 'moa.description')):
        moa.ui.warn("Moving moa.description to Readme.md")
        shutil.move(
            os.path.join(wd, 'moa.description'),
            os.path.join(wd, 'Readme.md'))

    makefile = os.path.join(wd,'Makefile')
    if not os.path.exists(makefile): return False
    
    with open(makefile) as F:
        t = F.read()
    if not 'include $(MOABASE)/template/moa/prepare.mk' in t:
        return False

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
    filesets = {}
    fs_re = re.compile(job.template.moa_id + '_(.*?)_((?:glob)|(?:dir)|(?:extension))')

    with open(moamk) as F:
        for line in F.readlines():
            line = line.strip()
            if '+=' in line:
                l.critical("Cannot autoconvert: %s" % line)
            k,v = line.split('=',1)
            
            fsmatch = fs_re.match(k)
            if fsmatch:
                name, comp = fsmatch.groups()
                l.info("Found fileset component %s %s" % (name, comp))
                if not filesets.has_key(name): filesets[name] = {}
                filesets[name][comp] = v
            else:                
                l.info("found parameter %s=%s" % (k,v))
                if job.template.moa_id in k:
                    k = k.replace('%s_' % job.template.moa_id, '')
                    l.info("  -> saving to %s=%s" % (k,v))
                job.conf[k] = v
        for fs in filesets.keys():
            fsinf = filesets[fs]
            l.info("processing fileset %s" % fs)
            fsdir = fsinf.get('dir', '*')
            if fsdir[-1] == '/': fsdir = fsdir[:-1]
            fspat = '%s/%s.%s' % (
                fsdir,
                fsinf.get('glob', '*'),
                fsinf.get('extension', '*'))
            l.info("  -> saving fileset %s=%s" % (fs, fspat))
            job.conf[fs] = fspat
    l.info("saving configuration")
    job.conf.save()
    l.warning("converted moa.mk - please check %s/config" % cdir)
                
    sys.exit()
