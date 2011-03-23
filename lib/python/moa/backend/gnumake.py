"""
Gnumake
-------

"""
import re
import os
import sys

import moa.utils
import moa.template
import moa.actor
import moa.backend
import moa.sysConf
import moa.logger as l

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
        if self.job.options.threads:
            self.job.env['MOA_THREADS'] = "%s" % self.job.options.threads
        else:
            self.job.env['MOA_THREADS'] = "1"
        self.job.env['MOA_TEMPLATE'] = "%s" % self.job.template.name
        self.job.env['moa_plugins'] = "%s" % " ".join(moa.sysConf.getPlugins())

        #if moa is silent, make should be silent
        if not self.job.options.verbose:
            self.job.makeArgs.append('-s')

        self.job.makeArgs.append('-f')
        makefileLoc = os.path.join(moa.utils.getMoaBase(), 'lib', 
                                   'gnumake', 'execute.mk')
        self.job.makeArgs.append(makefileLoc)
        l.debug("makefile @ %s" % makefileLoc)

        l.debug("Calling make for command %s" % command)

        #put the job.env in the environment
        for k in self.job.env.keys():
            os.putenv(k, str(self.job.env[k]))

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
                
        #and store some extra fileset information in the env
        for fsid in self.job.template.filesets.keys():
            fsconf = self.job.conf[fsid]
            refs = re.compile('(?P<path>.*/)?(?P<glob>[^/]*?)(?:\.(?P<ext>[^/\.]*))?$')
            match = refs.match(fsconf)
            if match:                
                confDict['%s_%s_dir' % (moaId, fsid)] = match.groups()[0]
                confDict['%s_%s_glob' % (moaId, fsid)] = match.groups()[1]
                confDict['%s_%s_extension' % (moaId, fsid)] = match.groups()[2]

        #dump the configuration in the environment
        for k in confDict.keys():
            os.putenv(k, str(confDict[k]))

        if command == 'run':
            command = self.job.template.name
            
        cl = ['make', command] + self.job.makeArgs

        l.debug("executing %s" % " ".join(cl))
        return moa.actor.simpleRunner(self.job.wd, cl)
        

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

