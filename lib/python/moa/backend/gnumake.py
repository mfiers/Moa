"""
Gnumake
-------

"""
import os
import sys

import moa.utils
import moa.template
import moa.actor
import moa.backend
import moa.sysConf
import moa.logger as l

NEW_MAKEFILE_HEADER = """#!/usr/bin/env make
## Moa Makefile
## http://mfiers.github.com/Moa

include $(MOABASE)/lib/gnumake/prepare.mk
"""

class Gnumake(moa.backend.BaseBackend):
    def prepare(self):
        """
        Prepare for later execution
        """

        self.job.options = self.job.options

        self.job.makeArgs = getattr(self.job, 'makeArgs', [])
        self.job.env = getattr(self.job, 'env', {})

        if self.job.options.makedebug:
            self.job.makeArgs.append('-d')

        ## Define extra parameters to use with Make
        if self.job.options.remake:
            self.job.makeArgs.append('-B')
        if self.job.options.makedebug:
            self.job.makeArgs.append('-d')

        self.job.makeArgs.extend(self.job.args)

    def hasCommand(self, command):
        """
        No way of finding out if this self.job exists (well, we might have a
        way, but I'm to lazy to try to find out.
        """
        return True

    def execute(self, command, **options):
        """
        Execute!
        """
        #self.job.plugins.run("readFilesets")
        
        verbose = options.get('verbose', False)
        
        ## make sure the MOA_THREADS env var is set - this is used from inside
        ## the Makefiles later threads need to be treated different from the
        ## other parameters. multi-threaded operation is only allowed in the
        ## second phase of execution.
        self.job.env['MOA_THREADS'] = "%s" % self.job.options.threads
        self.job.env['moa_plugins'] = "%s" % " ".join(moa.sysConf.getPlugins())

        #if moa is silent, make should be silent
        if not self.job.options.verbose:
            self.job.makeArgs.append('-s')


        l.debug("Calling make for command %s" % command)
        actor = self.job.getActor()

        #dump the self.job env into the actor environment (sys env)
        actor.setEnv(self.job.env)

        #and the self.job configuration
        confDict = {}
        moaId = self.job.template.moa_id
        for k in self.job.conf.keys():
            v = self.job.conf[k]
            if isinstance(v, dict):
                continue
            if isinstance(v, list) or \
                   isinstance(v, set):
                v = " ".join(map(str,v))
            if isinstance(v, bool):
                if not v: v = ""
            if k[:3] == 'moa':
                confDict[k] = v
            else:
                confDict['%s_%s' % (moaId, k)] = str(v)

        actor.setEnv(confDict)

        cl = ['make', command] + self.job.makeArgs

        l.debug("executing %s" % " ".join(cl))
        actor.run(cl)

    def defineOptions(self, parser):
        g = parser.add_option_group('Gnu Make Backend')
        parser.set_defaults(threads=1)
        g.add_option("-j", dest="threads", type='int',
                  help="threads to use when running Make (corresponds " +
                  "to the make -j parameter)")

        g.add_option("-B", dest="remake", action='store_true',
                  help="Reexecute all targets (corresponds to make -B) ")

        g.add_option("--md", dest="makedebug", action='store_true',
                  help="Run Make with -d : lots of extra debugging "+
                  "information")

    def initialize(self):

        """
        Create a new GnuMake self.job in the `wd`
        """

        l.debug("Creating a new self.job from template '%s'" %
                self.job.template.name)
        l.debug("- in wd %s" % self.job.wd)

        if not self.job.template.backend == 'gnumake':
            l.error("template backend mismatch")
            return False

        makefile = os.path.join(self.job.wd, 'Makefile')

        l.debug("Start writing %s" % makefile)
        with open(makefile, 'w') as F:
            F.write(NEW_MAKEFILE_HEADER)
            F.write("$(call moa_load,%s)\n" % self.job.template.moa_id)
