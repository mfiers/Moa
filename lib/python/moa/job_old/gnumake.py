#!/usr/bin/env python
# 
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
Job
"""

import os
import re
import sys
import tempfile

import moa.utils
import moa.logger as l
import moa.conf
import moa.template
import moa.utils
import moa.runMake

from moa.job.base import BaseJob

MOABASE = moa.utils.getMoaBase()
TEMPLATEDIR = os.path.join(MOABASE, 'template')

class GnuMakeJob(BaseJob):
    """
    New MoaJob class - should combine a lot of functionality
    that is now spread around over multiple locations
    """
    def __init__(self, wd):
        self.wd = wd
        super(GnuMakeJob, self).__init__(wd)

        self.makefile = os.path.join(self.wd, 'Makefile')
        self.moamk = os.path.join(self.wd, 'moa.mk')
        
        if self.isMoa():
            self.conf.load()
            self.getTemplateName()

    def getTemplateName(self):
        """
        Return the template name
        """
        with open(self.makefile) as F:
            for line in F.readlines():
                if 'include' in line and 'MOABASE' in line \
                    and '/template/' in line \
                    and (not '/template/moa/' in line):
                    self.template = line.strip().split('/')[-1].replace('.mk', '')
                return
            
            if '$(call moa_load,' in line:
                self.template = line.split(',')[1][:-2]
                return

    @moa.utils.deprecated
    def saveConfig(self):
        """
        Save the configuration to moa.mk
        """
        self.conf.save()

    @moa.utils.deprecated
    def loadConfig(self):
        self.conf.load()
        
    @moa.utils.deprecated
    def setConf(self, item):
        self.conf.add(item)

    @moa.utils.deprecated
    def setConfKV(self, key, value, operator='='):
        self.conf.add(key, operator, value)

    @moa.utils.deprecated
    def setConfFromString(self, s):
        self.conf.add(s)
        
    def isMoa(self):
        """
        Is the job directory a Moa directory

        currently we assume if there is a moa.mk file
        
        >>> job = Job('/')
        >>> job.isMoa()
        False
        >>> import moa.job
        >>> jobdir = moa.job.newTestJob('traverse')
        >>> job = Job(jobdir)
        >>> job.isMoa()
        True
        
        """
        makefile = os.path.join(self.wd, 'Makefile')
        if not os.access(makefile, os.R_OK):
            #ok, this might be a moa directory, but
            #you do not have sufficient permissions
            return False

        l.debug('isMoaDir: checking %s' % makefile)
        if not os.path.exists(makefile):
            return False

        #we could run make, but that is rather slow just to check if the
        #Makefile is a proper Moa Makefile - so, we' quickly read the
        #Makefile to get a quick indication
        isMoa = False

        F = open(makefile)
        for line in F.readlines():
            if 'MOABASE' in line:
                isMoa = True
                break
            if '$(call moa_load' in line:
                isMoa = True
                break

        F.close()        
        return isMoa

    def new(self,
            template,
            title = None,
            parameters = [],
            force = False,
            titleCheck = True,
            noInit = False):
        
        """
        Create a new template in the `wd`
        """
        l.debug("Creating a new job from template '%s'" % template)
        l.debug("- in wd %s" % self.wd)

        if not os.path.exists(self.wd):
            l.debug("creating folder for %s" % self.wd)
            os.makedirs(self.wd)
        #TODO: do something with the results of this check
            
        if not moa.template.check(template):
            l.error("Invalid template")

        if os.path.exists(self.makefile):
            l.debug("Makefile exists!")
            if not force:
                l.error("makefile exists, use -f (--force) to overwrite")
                sys.exit(-1)

        l.debug("Start writing %s" % self.makefile)
        with open(self.makefile, 'w') as F:
            F.write(NEW_MAKEFILE_HEADER)
            F.write("$(call moa_load,%s)\n" % template)

        if title:
            self.conf.add('title', title)

        params = []
        for par in parameters:
            if not '=' in par: continue
            self.conf.add(par)

        self.conf.save()
        if noInit: return

        l.debug("Running moa initialization")
        job = moa.runMake.MOAMAKE(wd = self.wd,
                                  target='initialize',
                                  captureOut = False,
                                  captureErr = False,
                                  stealth = True,
                                  verbose=False)
        job.run()
        job.finish()
        l.debug("Written %s, try: moa help" % self.makefile)

        # check if a title is defined as 'title=something' on the
        # commandline, as opposed to using the -t option
        if not title:
            for p in parameters:
                if p.find('title=') == 0:
                    title = p.split('=',1)[1].strip()
                    parameters.remove(p)
                    break

        if (not title) and titleCheck and (not template == 'traverse'):
            l.warning("You *must* specify a job title")
            l.warning("You can still do so by running: ")
            l.warning("   moa set title='something descriptive'")
            title = ""
        if title:
            l.debug('creating a new moa makefile with title "%s" in %s' % (
                title, self.wd))
        else:
            l.debug('creating a new moa makefile in %s' % ( self.wd))
