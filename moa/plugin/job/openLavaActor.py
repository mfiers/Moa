# Copyright 2009-2011 Mark Fiers
# The New Zealand Institute for Plant & Food Research
#
# This file is part of Moa - http://github.com/mfiers/Moa
#
# Licensed under the GPL license (see 'COPYING')
#
"""
**sgeActor** - Run jobs through SGE
-----------------------------------------------------------

"""
import os
import stat
import subprocess as sp
import sys
import tempfile


import jinja2
import moa.logger
import moa.ui
from moa.sysConf import sysConf


l = moa.logger.getLogger(__name__)
#l.setLevel(moa.logger.DEBUG)


def hook_defineCommandOptions(job, parser):
    parser.add_argument('--ol', action='store_const', const='openlava',
                        dest='actorId', help='Use OpenLava as actor')

    parser.add_argument('--olq', default='normal', dest='openlavaQueue',
                        help='The Openlava queue to submit this job to')

    parser.add_argument('--olx', default='', dest='openlavaExtra',
                        help='Extra arguments for bsub')

    parser.add_argument('--oln', default=1, type=int, dest='openlavaProcs',
                        help='The number of processors the jobs requires')

    parser.add_argument('--oldummy', default=False, dest='openlavaDummy',
                        action='store_true',
                        help='Do not execute - just create a script to run')

    parser.add_argument('--olm', default="", dest='openlavaHost',
                        help='The host to use for openlava')


def _writeOlTmpFile(wd, _script):
    #save the file
    tmpdir = os.path.join(wd, '.moa', 'tmp')
    if not os.path.exists(tmpdir):
        os.makedirs(tmpdir)

    tf = tempfile.NamedTemporaryFile(dir=tmpdir, prefix='openlava.',
                                     delete=False, suffix='.sh')
    if isinstance(_script, list):
        tf.write("\n".join(_script))
    else:
        tf.write(str(_script))

    tf.close()
    os.chmod(tf.name, stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR)
    return tf.name

@moa.actor.async
def openlavaRunner(wd, cl, conf={}, **kwargs):
    """
    Run the job using OPENLAVA

    what does this function do?
    - put env in the environment
    - Execute the commandline (in cl)
    - store stdout & stderr in log files
    - return the rc
    """

    #see if we can get a command
    command = kwargs.get('command', 'unknown')
    if command == 'unknown':
        l.critical("runner should be called with a command")
        sys.exit(-1)

    l.debug("starting openlava actor for %s" % command)

    # this is a trick to get the real path of the log dir - but not of
    # any underlying directory - in case paths are mounted differently
    # on different hosts
    outDir = os.path.abspath(os.path.join(wd, '.moa', 'log.latest'))
    outDir = outDir.rsplit('.moa', 1)[0] + '.moa' + \
        os.path.realpath(outDir).rsplit('.moa', 1)[1]

    sysConf.job.data.openlava.outDir = outDir

    if not os.path.exists(outDir):
        try:
            os.makedirs(outDir)
        except OSError:
            pass

    #expect the cl to be nothing more than a single script to execute
    outfile = os.path.join(outDir, 'stdout')
    errfile = os.path.join(outDir, 'stderr')

    sysConf.job.data.openlava.outfile = outfile
    sysConf.job.data.openlava.errfile = errfile

    bsub_cl = ['bsub']

    sc = []

    def s(*cl):
        sc.append(" ".join(map(str, cl)))

    s("#!/bin/bash")
    s("#BSUB -o %s" % outfile)
    s("#BSUB -e %s" % errfile)
    s("#BSUB -q %s" % sysConf.args.openlavaQueue)

    if '--oln' in sys.argv:
        procs = sysConf.args.openlavaProcs
    else:
        procs = sysConf.job.conf.get('threads', sysConf.args.openlavaProcs)

    s("#BSUB -C %d" % procs)

    if sysConf.args.openlavaExtra.strip():
        s("#BSUB %s" % sysConf.args.openlavaExtra)

    if '--olm' in sys.argv:
        s("#BSUB -m %s" % sysConf.args.openlavaHost)
        #bsub_cl.extend(["-m", sysConf.args.openlavaHost])

    if command == 'run':
        prep_jids = sysConf.job.data.openlava.jids.get('prepare', [])
        #hold until the 'prepare' jobs are done
        #l.critical("Prepare jids - wait for these! %s" % prep_jids)
        for j in prep_jids:
            s("#BSUB -w 'done(%d)'" % j)
            #bsub_cl.extend(["-w", "'done(%d)'" % j])

    elif command == 'finish':
        run_jids = sysConf.job.data.openlava.jids.get('run', [])
        #hold until the 'prepare' jobs are done
        for j in run_jids:
            s("#BSUB -w 'done(%d)'" % j)
            #bsub_cl.extend(["-w", "'done(%d)'" % j])

    #give it a reasonable name
    jobname = ("%s_%s" % (wd.split('/')[-1], command[0]))
    bsub_cl.extend(['-J', jobname])
    s("#BSUB -J '%s'" % jobname)

    #dump the configuration in the environment
    s("")
    s("## ensure we're in the correct directory")
    s("cd", wd)


    s("")
    s("## Defining moa specific environment variables")
    s("")

    confkeys = sorted(conf.keys())
    for k in confkeys:
        # to prevent collusion, prepend all env variables
        # with 'moa_'
        if k[0] == '_' or k[:3] == 'moa':
            outk = k
        else:
            outk = 'moa_' + k
        v = conf[k]

        #this should not happen:
        if ' ' in outk:
            continue

        if isinstance(v, list):
            s("%s='%s'" % (outk, " ".join(v)))
        elif isinstance(v, dict):
            continue
        else:
            s("%s='%s'" % (outk, v))

    s("")
    s("## Run the command")
    s("")

    s(*cl)

    if sysConf.args.openlavaDummy:
        # Dummy mode - do not execute  - just write the script.
        ii = 0
        while True:
            outFile = os.path.join(wd, 'openlava.%s.%d.bash' % (command, ii))
            if not os.path.exists(outFile):
                break
            ii += 1
        with open(outFile, 'w') as F:
            F.write("\n".join(sc))
            moa.ui.message("Created openlava submit script: %s" %
                           outFile.rsplit('/', 1)[1])

            moa.ui.message("now run:")
            moa.ui.message("   %s < %s" % ((" ".join(map(str, bsub_cl))),
                                           outFile.rsplit('/', 1)[1]))
            return 0

    tmpfile = _writeOlTmpFile(wd, sc)

    moa.ui.message("Running %s:" % " ".join(map(str, bsub_cl)))
    moa.ui.message("(copy of) the bsub script: %s" % tmpfile)
    p = sp.Popen(map(str, bsub_cl), cwd=wd, stdout=sp.PIPE, stdin=sp.PIPE)
    o, e = p.communicate("\n".join(sc))

    jid = int(o.split("<")[1].split(">")[0])

    moa.ui.message("Submitted a job to openlava with id %d" % jid)

    if not sysConf.job.data.openlava.jids.get(command):
        sysConf.job.data.openlava.jids[command] = []

    #moa.ui.message("submitted job with openlava job id %s " % jid)

    #store the job id submitted
    if not sysConf.job.data.openlava.jids.get(command):
            sysConf.job.data.openlava.jids[command] = []
    if not sysConf.job.data.openlava.get('alljids'):
            sysConf.job.data.openlava.alljids = []
    sysConf.job.data.openlava.jids[command].append(jid)
    sysConf.job.data.openlava.alljids.append(jid)
    l.debug("jids stored %s" % str(sysConf.job.data.openlava.jids))
    return p.returncode

OnSuccessScript = """#!/bin/bash
#BSUB -o {{ job.data.openlava.outfile }}
#BSUB -w {{ job.data.openlava.errfile }}
#BSUB -q {{ args.openlavaQueue }}
#BSUB -J "{{ job.data.openlava.uid }}_Ok"
{% if args.openlavaHost -%}
#BSUB -m {{ args.openlavaHost }}
{%- endif %}

#BSUB -w '({%- for j in job.data.openlava.alljids -%}
{%- if loop.index0 > 0 %}&&{% endif -%}
done({{j}})
{%- endfor -%})'
cd {{ job.wd }}
echo "Openlava OnSuccess Start"
echo "Killing the OnError job"
bkill -J "{{ job.data.openlava.uid }}_Err"
moasetstatus success
"""


OnErrorScript = """#!/bin/bash

## only run this job if there is a single job
#BSUB -o {{ job.data.openlava.outfile }}
#BSUB -w {{ job.data.openlava.errfile }}
#BSUB -q {{ args.openlavaQueue }}
#BSUB -J "{{ job.data.openlava.uid }}_Err"
{% if args.openlavaHost -%}
#BSUB -m {{ args.openlavaHost }}
{%- endif %}
#BSUB -w '({%- for j in job.data.openlava.alljids -%}
{%- if loop.index0 > 0 %}||{% endif -%}
exit({{j}},!=0)
{%- endfor -%}
)'

cd {{ job.wd }}
echo "Openlava OnError Start"
echo "Killing the all other jobs"
#killing all jobs
{% for j in job.data.openlava.alljids %}
bkill -s 9 {{ j }}
{% endfor %}

bkill -J "{{ job.data.openlava.uid }}_Ok"
moasetstatus error
"""

def hook_async_exit(job):
    """
    Need to exit here, and reconvene once all jobs have executed
    """

    #make sure that this is the correct actor
    actor = moa.actor.getActor()
    if actor.__name__ != 'openlavaRunner':
        return

    jidlist = sysConf.job.data.openlava.get('alljids', [])
    if len(jidlist) == 0:
        return


    uid = "%s.%s" % (job.wd.split('/')[-1],max(jidlist))
    sysConf.job.data.openlava.uid = uid
    onsuccess = jinja2.Template(OnSuccessScript).render(sysConf)
    onerror = jinja2.Template(OnErrorScript).render(sysConf)

    with open('succ', 'w') as F:
        F.write(onsuccess)
    with open('onerr', 'w') as F:
        F.write(onerror)
    P = sp.Popen('bsub', stdin=sp.PIPE)
    P.communicate(onsuccess)
    P = sp.Popen('bsub', stdin=sp.PIPE)
    P.communicate(onerror)




#register this actor globally
sysConf.actor.actors['openlava'] = openlavaRunner
sysConf.actor.openlava.jids = []
