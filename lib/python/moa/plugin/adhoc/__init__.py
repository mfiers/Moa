# Copyright 2009-2011 Mark Fiers
# The New Zealand Institute for Plant & Food Research
# 
# This file is part of Moa - http://github.com/mfiers/Moa
# 
# Licensed under the GPL license (see 'COPYING')
# 
"""
**adhoc** - create jobs from adhoc bash code
--------------------------------------------
"""

import os
import re
import sys
import optparse

import moa.job
import moa.logger as l
import moa.plugin

from moa.sysConf import sysConf

def hook_defineCommands():
    sysConf['commands']['simple'] = { 
        'desc' : 'Create a "simple" adhoc analysis',
        'call' : createSimple,
        'needsJob' : False,
        'usage' : 'moa simple -t "title" -- echo "do something"',
        }
    sysConf['commands']['map'] = { 
        'desc' : 'Create a "map" adhoc analysis',
        'call' : createMap,
        'needsJob' : False,
        'usage' : 'moa map -t "title" -- echo "do something"',
        }
    sysConf['commands']['reduce'] = { 
        'desc' : 'Create a "reduce" adhoc analysis',
        'call' : createReduce,
        'needsJob' : False,
        'usage' : 'moa reduce -t "title" -- echo "do something"',
        }
    sysConf['commands']['!'] = { 
        'desc' : 'Assign the last issued command to "process" parameter',
        'call' : exclamate,
        'needsJob' : False,        
        'usage' : 'moa !',
        }

def hook_defineOptions():
    
    parserG = sysConf.parser.get_option_group('-t')
    if parserG == None:
        parserG = optparse.OptionGroup(sysConf.parser, 'moa new')
        sysConf.parser.add_option_group(parserG)    

    try:
        parserG.add_option("-t", dest="title", help='define job title ' +
        '(when creating a job)')
    except  optparse.OptionConflictError:
        pass

    try:
        parserG.add_option("--np", dest="noprompt", action='store_true',
                           help="Do not prompt for process, input or output")        
    except optparse.OptionConflictError:
        pass # this options are probably already defined in the newjob plugin



def createSimple(job):
    """
    Create a 'simple' adhoc job. Simple meaning that no in or output
    files are tracked.

    There are a number of ways this command can be used::

        moa simple -t 'a title' -- echo 'define a command'
        
    Anything after `--` will be the executable command. Note that bash
    will attempt to process the command line. A safer method is::

        moa simple -t 'a title'

    Moa will query you for a command to execute (the parameter
    `process`).
    """

    wd = job.wd
    options = sysConf.options
    args = sysConf.args
    
    if not options.force and \
           os.path.exists(os.path.join(wd, '.moa', 'template')):
        moa.ui.exitError("Job already exists, use -f to override")

    command = " ".join(args[1:]
                       ).strip()
    if not command and not options.noprompt:
        command=moa.ui.askUser('process:\n> ', '')
        
    params = [('process', command)]

    #make sure the correct hooks are called
    sysConf.pluginHandler.run("preNew")

    moa.job.newJob(
        wd, template='simple',
        title = options.title,
        parameters=params)

    #make sure the correct hooks are called
    sysConf.pluginHandler.run("postNew")



def exclamateNoJob(job):
    """
    Create a "simple" job & set the last command
    to the 'process' parameter 
    """
    options = sysConf['options']

    title = options.title
    if not options.title: 
        moa.ui.warn("Do not forget to set a title")
    histFile = os.path.join(os.path.expanduser('~'), '.moa.last.command')
    if not os.path.exists(histFile):
        moa.ui.exitError(
            ("This needs to be used in conjunction with the " +
             "moa_prompt code. Please read the manual") )

    with open(histFile) as F:
        last = F.read().strip()
        
    
    job = moa.job.newJob(
        wd = job.wd, template='simple', 
        title = title,
        parameters = [('process', last)])

def exclamateInJob(job):
    """
    Reuse the last issued command: set it as the 'process' parameters
    in the current job    
    """
    pc = os.environ.get('PROMPT_COMMAND', '')
    if not '_moa_prompt' in pc:
        moa.ui.exitError("_moa_propt is not properly set up")

    histFile = os.path.join(job.confDir, 'local_bash_history')
    if not os.path.exists(histFile):
        moa.ui.exitError(
            ("This needs to be used in conjunction with the " +
             "moa_prompt code. Make sure you've source `moainit`") )

    with open(histFile) as F:
        last = F.readlines()[-1].strip()
        
    moa.ui.fprint("{{bold}}Using command:{{reset}}", f='jinja')
    moa.ui.fprint(last)
    job.conf.process=last
    job.conf.save()
                
def exclamate(job):
    """
    Set the `process` parameter to the last issued command. If a moa
    job exists in the current directory, then the `process` parameter
    is set without questions. (even if the Moa job in question does
    not use the `process` parameter).  If no moa job exists, a
    `simple` job is created first.

    *Note:* This works only when using `bash` and if `moainit` is
    sourced properly. `moainit` defines a bash function `_moa_prompt`
    that is called every time a command is issued (using
    `$PROMPT_COMMAND`). The `_moa_prompt` function takes the last
    command from the bash history and stores it in
    `~/.config/moa/last.command`. Additionally, the `_moa_prompt`
    function stores all commands issued in a Moa directory in
    `.moa/local_bash_history`.
    """
    
    if job.isMoa():
        exclamateInJob(job)
    else: 
        exclamateNoJob(job)
    
def createMap(job):
    """
    Anything after `--` will be stored in the `process` variable. If
    `--` is omitted, Moa will query the user.

    Moa will also query the user for input & output files. An example
    session::

        $ moa map -t 'test map'
        process:
        > echo 'processing {{ input }} {{ output }}'
        input:
        > ../10.input/*.txt
        output:
        > ./*.out

    Assuming you have a number of `*.txt` files in the `../10/input/`
    directory, you will see, upon running::

       processing ../10.input/test.01.txt ./test.01.out
       processing ../10.input/test.02.txt ./test.02.out
       processing ../10.input/test.03.txt ./test.03.out
       ...

    If the output file exists, and is newer than the input file, the
    process will not be executed for that specific pair. If you need
    the job to be repeated, you should either delete the output files
    or `touch` the input files.
    """
    wd = job.wd
    options = sysConf.options
    args = sysConf.args
    
    if not options.force and \
           os.path.exists(os.path.join(wd, '.moa', 'template')):
        moa.ui.exitError("Job already exists, use -f to override")

    command = " ".join(args[1:]
                       ).strip()
    params = []
    if not command and not options.noprompt:
        command=moa.ui.askUser('process:\n> ', '')
        params.append(('process', command))

    if not options.noprompt:
        input=moa.ui.askUser('input:\n> ', '')
        output=moa.ui.askUser('output:\n> ', './*')
        params.append(('input', input))
        params.append(('output', output))
        
    moa.job.newJob(
        wd, template='map',
        title = options.title,
        parameters=params)


def createReduce(job):
    """
    Create a 'reduce' adhoc job.

    There are a number of ways this command can be used::

        $ moa reduce -t 'a title' -- echo 'define a command'

    Anything after `--` will be the executable command. If omitted,
    Moa will query the user for a command.

    Moa will also query the user for input & output files. An example
    session::

        $ moa map -t 'something intelligent'
        process:
        > echo 'processing {{ input }} {{ output }}'
        input:
        > ../10.input/*.txt
        output:
        > ./*.out

    Assuming you have a number of text files in the `../10/input/`
    directory, you will see, upon running::

       processing ../10.input/test.01.txt ./test.01.out
       processing ../10.input/test.02.txt ./test.02.out
       processing ../10.input/test.03.txt ./test.03.out
       ...

    """
    wd = job.wd
    options = sysConf.options
    args = sysConf.args
    
    if not options.force and \
           os.path.exists(os.path.join(wd, '.moa', 'template')):
        moa.ui.exitError("Job already exists, use -f to override")

    command = " ".join(args[1:]
                       ).strip()
    params = []
    if not command and not options.noprompt:
        command=moa.ui.askUser('process:\n> ', '')
        params.append(('process', command))

    if not options.noprompt:
        input=moa.ui.askUser('input:\n> ', '')
        output=moa.ui.askUser('output:\n> ', './output')
        params.append(('input', input))
        params.append(('output', output))
        
    moa.job.newJob(
        wd, template='reduce',
        title = options.title,
        parameters=params)




### Old adhoc code - still here for historical purposes
def _sourceOrTarget(g):
    """
    Determine if this glob is a likely source or
    target, depending on where the output is aimed to go
    """
    d = g.groups()[0]
    if not d: return 'target'
    if d[:2] == './': return 'target'

    if d[:2] == '..': return 'source'
    if d[0] == '/': return 'source'
    return 'target'
    
def createAdhoc(job):
    """
    Creates an adhoc job.
    """
    wd = sysConf['cwd']
    options = sysConf['options']
    args = sysConf['newargs']

    if not options.force and \
           os.path.exists(os.path.join(wd, '.moa', 'template')):
        moa.ui.exitError("Job already exists, use -f to override")
        
    command = " ".join(args).strip()
    
    if not command:
        command=moa.ui.askUser('command:\n>', '')

    l.info('Parsing command: %s' % command)
    params = []
    mode = None
    searchGlobs = True
        
    if options.mode:
        mode = options.mode
        if options.mode == 'simple': searchGlobs = False
        if not options.mode in ['seq', 'par', 'all', 'simple']:
            l.critical("Unknown adhoc mode: %s" % options.mode)
            sys.exit(-1)
    elif '$<' in command:
        mode = 'seq'
        searchGlobs = False
    elif ('$^' in command) or ('$?' in command):
        mode = 'all'
        searchGlobs = False
        l.warning("Observed '$^' or '$?', setting mode to 'all'")
        l.warning("Processing all files in one go")

    #see if we have to look for file globs
    if not searchGlobs:
        l.info("No recognizable globs found")
    else:
        #it appears to make sense to see if there is a glob in the command
        refindGlob = re.compile(
            r"([^ *]+" \
            + os.sep \
            + ")?([^ *]*\*[^ *]*?)((?:\.[^ .*]+)?)")
        
        globs = []
        for g in refindGlob.finditer(command):
            globs.append(g)

        if globs:
            globReplace = '$<', '$t'                                
            mode = 'seq'
            if len(globs) > 2:
                raise Exception("Too many globs ??  I not understand :(")
            if len(globs) == 2:
                st1 = _sourceOrTarget(globs[0])
                st2 = _sourceOrTarget(globs[1])
                if st1 == st2:
                    l.warn("Unsure wich is the source &  target glob, assuming:")
                    inGlob,outGlob = globs
                if st1 == 'source': inGlob,outGlob = globs
                else:
                    outGlob,inGlob = globs
                    globReplace = '$t', '$<'
                    
                l.info("Input glob: %s" % inGlob.group())
                l.info("Output glob: %s" % outGlob.group())
            else:
                l.info("Input glob: %s" % globs[0].group())
                inGlob, outGlob = globs[0], None

            inD, inG, inE = inGlob.groups()
            if not inD: inD = ""
            if not inE: inE = ""
            l.info(" - set input dir        : %s" % inD)
            l.info(" - set input glob       : %s" % inG)
            l.info(" - set input extension  : %s" % inE[1:])

            params.append(('input_dir', inD))
            params.append(('input_glob', inG))
            params.append(('input_extension', inE[1:]))

            if outGlob:
                ouD, ouG, ouE = outGlob.groups()
                if not ouD: ouD = ""
                if not ouE: ouE = ""

                ouG1, ouG2 = ouG.split('*')
                sed = r"s^\(.*\)%s^%s%s\1%s%s^g" % (
                    inE.replace('.', '\.'),
                    ouD.replace('/', '/'),
                    ouG.split('*')[0],
                    ouG.split('*')[1],
                    ouE
                    )
                l.info(" - set name_sed         : %s " % sed)
                l.info(" - set output dir       : %s " % ouD)
                params.append(('output_dir', ouD))
                params.append(('name_sed', sed))

            #hack the commandline
            for i in range(len(globs)-1, -1, -1):
                g = globs[i]
                command = command[:g.start()] + globReplace[i] + command[g.end():]

    if not mode:
        mode = 'simple'

    if command:
        l.info(" - set command          : %s" % command)
        params.append(('process', command))

    params.append(('mode', mode))
    
    l.info(" - set mode             : %s" % mode)

    if mode == 'seq':
        l.warning("Note: adhoc is running in sequential ('seq') mode. If ")
        l.warning("you are confident that the individual jobs do not interfere, you might ")
        l.warning("consider setting adhoc to parallel operation:")
        l.warning("$ moa set mode=par")

    for pk, pv in params:
        l.debug('setting parameters %s to %s' % (pk, pv))
    
    moa.job.newJob(wd, template='adhoc',
                         title = options.title,
                         parameters=params)

