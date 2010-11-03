
import os
import sys

import moa.utils
import moa.logger as l
import moa.conf
import moa.template
import moa.utils
import moa.runMake
import moa.actor
import moa.backend

NEW_MAKEFILE_HEADER = """#!/usr/bin/env make
## Moa Makefile
## http://mfiers.github.com/Moa

include $(MOABASE)/template/moa/prepare.mk
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
        
        ## make sure the MOA_THREADS env var is set - this is used from inside
        ## the Makefiles later threads need to be treated different from the
        ## other parameters. multi-threaded operation is only allowed in the
        ## second phase of execution.
        self.job.env['MOA_THREADS'] = "%s" % options.threads

        ## Define extra parameters to use with Make
        if options.remake:
            self.makeArgs.append('-B')
        if options.makedebug:
            self.makeArgs.append('-d')
        
        self.makeArgs.extend(self.job.args)
    
    def execute(self, command):
        l.debug("Calling make for command %s" % command)
        actor = moa.actor.Actor(self.job.wd)
        cl = ['make', command] + self.makeArgs
        l.critical("executing %s" % " ".join(cl))
        #job = runMake.MOAMAKE(wd,
        #                      target = command,
        #                      verbose = options.verbose,
        #                      threads = options.threads,
        #                      makeArgs = makeArgs,
        #                      background = options.background)
        returnCode = job.returnCode()
        return returnCode

        
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


    def initialize(self,
            template = None,
            title = None,
            parameters = [],
            titleCheck = True,
            noInit = False):        

        """
        Create a new GnuMake job in the `wd`
        """
        
        l.debug("Creating a new job from template '%s'" % template)
        l.debug("- in wd %s" % self.wd)
           
        if not template:
            l.error("need to specify a template")
            return False
        
        if not template.valid:
            l.error("Invalid template")
            return False
            
        if not template.backend == 'gnumake':
            l.error("Template backend mismatch :(")
            return False


        l.debug("Start writing %s" % self.makefile)
        with open(self.makefile, 'w') as F:
            F.write(NEW_MAKEFILE_HEADER)
            F.write("$(call moa_load,%s)\n" % template)

        if title:
            self.job.conf.set('title', title)

        params = []
        for par in parameters:
            if not '=' in par: continue
            self.job.conf.add(par)

        self.job.conf.save()
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

