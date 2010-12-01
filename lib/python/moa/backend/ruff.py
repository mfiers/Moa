"""
Ruff
----

Ruffus/Jinja Backend
"""

import os
import re
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

def jinjaTemplateLoader(moa_id, command):
    templateFile = os.path.join(
        TEMPLATEDIR, '%s.jinja2' % (moa_id))
    
    with open(templateFile) as F:
        raw = F.read()

    rawc = re.split('### *(\w+) *\n', raw)
    commands = dict([(rawc[i], rawc[i+1].strip())
                     for i in range(1, len(rawc), 2)])
    return jTemplate(commands[command])
    
def defineOptions(job, parser):
    g = parser.add_option_group('Ruffus backend')
    parser.set_defaults(threads=1)
    g.add_option("-j", dest="threads", type='int',
                 help="threads to use when running Ruffus")
    
    g.add_option("-B", dest="remake", action='store_true',
                 help="Reexecute all targets (corresponds to make -B) ")

def execute(job, command, verbose=False, background=False):


    l.debug("executing %s" % command)

    jt = jinjaTemplateLoader(job.template.moa_id, command)
    actor = moa.actor.Actor(job.wd)

    rawConf = {}
    for k in job.conf.keys():
            rawConf[k] = job.conf[k]

    def generate_data():
        rv = []
                
        if len(job.data.inputs) + len(job.data.outputs) == 0:
            l.critical("no in or output files")
            sys.exit()
        noFiles = len(job.data.fileSets[
                (job.data.inputs + job.data.outputs)[0]
                ]['files'])

        prereqs = []
        for fsid in job.data.prerequisites:
            prereqs.extend(job.data.fileSets[fsid]['files'])
        for i in range(noFiles):
            outputs = [job.data.fileSets[x]['files'][i] 
                       for x in job.data.outputs]
            inputs =  [job.data.fileSets[x]['files'][i] 
                       for x in job.data.inputs]
            fsdict = dict([(x, job.data.fileSets[x]['files'][i]) 
                           for x in job.data.inputs + job.data.outputs])
            
            l.debug('pushing job with inputs %s' % ", ".join(inputs[:10]))
            
            yield([inputs + prereqs, outputs, fsdict, rawConf, jt, actor])

    cmode = job.template.commands[command].mode

    if cmode == 'map':
        #late decoration - see if that works :/
        executor2 = ruffus.files(generate_data)(executor_map)
        ruffus.pipeline_run([executor2],
                            verbose = job.options.verbose,
                            one_second_per_job=False,
                            multiprocess= job.options.threads,
                            )
    elif cmode == 'reduce':
        pass
    elif cmode == 'simple':
        tf = tempfile.NamedTemporaryFile( 
            delete = False, prefix='moa', mode='w')
        tf.write(jt.render(job.conf))
        tf.close()
        actor.run(['bash', tf.name])
    
    
def executor_map(input, output, fsdict, conf, template, actor):
    tf = tempfile.NamedTemporaryFile( delete = False,
                                      prefix='moa',
                                      mode='w')

    data = fsdict
    data.update(conf)
        
    tf.write(template.render(data))
    tf.close()
    cl = ['bash', tf.name]
    
    return actor.run(cl)
        
