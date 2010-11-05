
import os
import sys

import moa.utils
import moa.logger as l
import moa.conf
import moa.template
import moa.utils
import moa.actor
import moa.backend

NEW_MAKEFILE_HEADER = """#!/usr/bin/env make
## Moa Makefile
## http://mfiers.github.com/Moa

include $(MOABASE)/lib/gnumake/prepare.mk
"""

class GnumakeBackend(moa.backend.BaseBackend):
    """
    GnuMake backend
    """

    def __init__(self, job):
        """
        """
        super(GnumakeBackend, self).__init__(job)

        self.makefile = os.path.join(self.job.wd, 'Makefile')
        
        self.moamk = os.path.join(self.job.wd, 'moa.mk')
        self.makeArgs = []

        
    def isMoa(self):
        """
        Is this job a proper moa (gnumake) job?
        """    
        if not os.path.exists(self.makefile):
            return False
        with open(self.makefile) as F:
            mf = F.read()
        if 'MOABASE' in mf:
            return True
        return False

    def prepare(self):
        """
        Prepare for later execution
        """
        
        options = self.job.options

        #do not use builtin rules
        self.makeArgs.append('-r')

        if options.makedebug:
            self.makeArgs.append('-d')
            
        ## Define extra parameters to use with Make
        if options.remake:
            self.makeArgs.append('-B')
        if options.makedebug:
            self.makeArgs.append('-d')
        
        self.makeArgs.extend(self.job.args)
    
    def execute(self, command, verbose=False, background=False):

        ## make sure the MOA_THREADS env var is set - this is used from inside
        ## the Makefiles later threads need to be treated different from the
        ## other parameters. multi-threaded operation is only allowed in the
        ## second phase of execution.
        self.job.env['MOA_THREADS'] = "%s" % self.job.options.threads
        
        #if moa is not verbose, make should be silent
        if not self.job.options.verbose:
            self.makeArgs.append('-s')
            
        background = self.job.options.background

        l.debug("Calling make for command %s" % command)
        actor = self.job.getActor()

        #dump the job env into the actor environment (sys env)
        actor.setEnv(self.job.env)
        #and the job configuration
        actor.setEnv(self.job.conf)

        cl = ['make', command] + self.makeArgs
        
        l.debug("executing %s" % " ".join(cl))
        actor.run(cl, background = background)
        
        #returnCode = job.returnCode()
        #return returnCode

        
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

    def getTemplateName(self):
        """
        Return the template name
        """
        with open(self.makefile) as F:
            for line in F.readlines():
                if 'include' in line \
                       and 'MOABASE' in line \
                       and '/template/' in line \
                       and (not '/template/moa/' in line):
                    return line.strip().split('/')[-1].replace('.mk', '')
                if '$(call moa_load,' in line:
                    return line.split(',')[1][:-2]
        return None


    def initialize(self, template = None):

        """
        Create a new GnuMake job in the `wd`
        """
        
        l.debug("Creating a new job from template '%s'" % template)
        l.debug("- in wd %s" % self.wd)
           
        if not template:
            template = self.job.template
        
        if not template.valid:
            l.error("Invalid template")
            return False
            
        if not template.backend == 'gnumake':
            l.error("template backend mismatch")
            return False

        l.debug("Start writing %s" % self.makefile)
        with open(self.makefile, 'w') as F:
            F.write(NEW_MAKEFILE_HEADER)
            F.write("$(call moa_load,%s)\n" % template)


