
import os
import sys
import tempfile

import ruffus

from jinja2 import Template as jTemplate

import moa.utils
import moa.template
import moa.actor
import moa.backend
import moa.sysConf
import moa.logger as l

MOABASE = moa.utils.getMoaBase()
TEMPLATEDIR = os.path.join(MOABASE, 'template2')

RUNDATA = []
JOBCONF = {}
JTEMP = None
ACTOR = None

@ruffus.files(RUNDATA)
def executor(output, input, fsdict):
    l.debug("executing with input %s" % input)
    l.debug("  and output %s" % output)
    tf = tempfile.NamedTemporaryFile( delete = False,
                                      prefix='moa',
                                      mode='w')
    
    data = fsdict
    data.update(JOBCONF)
    
    tf.write(JTEMP.render(data))
    tf.close()
    cl = ['bash', tf.name]
    
    ACTOR.run(cl)
    

def ruffus_runner(jTemp, data, conf, actor):
    global JTEMP
    JTEMP = jTemp
    global JOBCONF
    JOBCONF = conf
    global RUNDATA
    RUNDATA = data
    print len(RUNDATA)
    global ACTOR
    ACTOR = actor
    
    
    ruffus.pipeline_run([executor],
                        verbose = 0,
                        one_second_per_job=False,
                        multiprocess= 1,
                        )


class MruffusBackend(moa.backend.BaseBackend):
    """
    GnuMake backend
    """

    def __init__(self, job):
        """
        """
        super(MruffusBackend, self).__init__(job)

        self.actor = moa.actor.Actor(job.wd)
        
        self.mode = self.job.template.ruffus_mode
        l.debug("ruffus job in mode %s" % self.mode)

        self.fileSets = {}
        self.inputs = []
        self.outputs = []
        for fsid in self.job.template.filesets.keys():
            fs = self.job.template.filesets[fsid]
            self.fileSets[fsid] = fs
            self.fileSets[fsid]['files'] = self.readFileSet(fsid)
            if fs.category == 'input':
                self.inputs.append(fsid)
            if fs.category == 'output':
                self.outputs.append(fsid)
        
    def isMoa(self):
        """
        Is this job a proper moa (gnumake) job?
        """    
        return True

    def defineOptions(self, parser):
        g = parser.add_option_group('Ruffus backend')
        parser.set_defaults(threads=1)
        g.add_option("-j", dest="threads", type='int',
                  help="threads to use when running Ruffus")

        g.add_option("-B", dest="remake", action='store_true',
                  help="Reexecute all targets (corresponds to make -B) ")

        #g.add_option("--md", dest="makedebug", action='store_true',
        #          help="Run Make with -d : lots of extra debugging "+
        #          "information")

    def readFileSet(self, fsid):

        fof = os.path.join('.moa', '%s.fof' % fsid)
        with open(fof) as F:
            return F.read().split()

    def generate_parameters(self):
        rv = []
        if len(self.inputs) + len(self.outputs) == 0:
            l.critical("no in or output files")
            sys.exit()
        noFiles = len(self.fileSets[(self.inputs + self.outputs)[0]]['files'])
        for i in range(noFiles):
            outputs = [self.fileSets[x]['files'][i] for x in self.outputs]
            inputs =  [self.fileSets[x]['files'][i] for x in self.inputs]
            fsdict = dict([(x, self.fileSets[x]['files'][i]) for x in self.fileSets])
            rv.append([outputs, inputs, fsdict])
        return rv

    def execute(self, command, verbose=False, background=False):

        jinjaTemplateFile = os.path.join(
            TEMPLATEDIR, '%s.%s.jinja2' % (self.job.template.moa_id, command))
        
        with open(jinjaTemplateFile) as F:
            jTemp = jTemplate(F.read())

        data = self.generate_parameters()

        ruffus_runner(jTemp, data, self.job.conf, self.actor)
        

 
    def initialize(self):

        """
        Create a new GnuMake job in the `wd`
        """
        
        l.debug("Creating a new job from template '%s'" %
                self.job.template.name)
        l.debug("- in wd %s" % self.wd)
          
        template = self.job.template
        
        if not template.backend == 'gnumake':
            l.error("template backend mismatch")
            return False


        l.debug("Start writing %s" % self.makefile)
        with open(self.makefile, 'w') as F:
            F.write(NEW_MAKEFILE_HEADER)
            F.write("$(call moa_load,%s)\n" % template.moa_id)
