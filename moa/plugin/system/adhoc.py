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

import moa.args
import moa.job
import moa.logger
from moa.sysConf import sysConf


l = moa.logger.getLogger(__name__)

def _checkTitle(j, argstitle):
    """
    check if there is anything resembling a title in `t` - otherwise
    see if there is one in the job object j, else ask the user
    """
    rv = ""

    if argstitle:
        rv = argstitle
    else:
        default = ""
        if j.conf.is_local('title') and j.conf.title:
            default = j.conf.title
        while rv == "":
            rv = moa.ui.askUser("title", default)

    moa.ui.message('Setting "title" to "%s"' % rv)
    return rv

def _get_bash_history_file():
    """
    get the proper history file - a local one if it exists - otherwise
    use bash_history
    """
    hf = os.path.join('.moa', 'local_bash_history')

    if os.path.exists(hf):
        return hf
    else:
        return os.path.join(os.path.expanduser('~'), '.bash_history')

def _createAdhocJob(job, args, template, query=[]):
    """
    One function for all adhoc type new job commands
    """

    wd = job.wd
    if (not args.force and
            os.path.exists(os.path.join(wd, '.moa', 'template'))):

        moa.ui.exitError("Job already exists, use -f to override")

    params = []
    for qdata in query:
        param, xtra_history = qdata[0], qdata[1]

        v = moa.ui.askUser(param,
                           job.conf.get(param),
                           xtra_history)

        params.append((param, v))

    title = _checkTitle(job, args.title)
        
    #make sure the correct hooks are called
    sysConf.pluginHandler.run("preNew")

    job = moa.job.newJob(job, template=template, title=title,
                         parameters=params)

    #make sure the correct hooks are called
    sysConf.pluginHandler.run("postNew")

@moa.args.argument('-t', '--title', help='A title for this job')
@moa.args.forceable
@moa.args.command
def simple(job, args):
    """
    Create a 'simple' adhoc job.

    Simple meaning that no in or output files are tracked. Moa will
    query you for a command to execute (the `process` parameter). Note
    that Moa tracks a history for all 'process' parameters used.
    """
    _createAdhocJob(job, args, 'simple', 
                    [ ('process', None)
                     ])

@moa.args.argument('-t', '--title', help='A title for this job')
@moa.args.forceable
@moa.args.commandName('simple!')
def simpleX(job, args):
    """
    Create a 'simple' adhoc job. 

    This command is exactly the same as `moa simple` except for the
    fact that Moa uses the bash history specific for the moa job or,
    if absent, the user bash history. This is convenient if you would
    like to register or reuse a command that you have alreayd
    executed.
    """

    _createAdhocJob(job, args, 'simple', 
                    [ ('process', _get_bash_history_file())])


@moa.args.argument('-t', '--title', help='A title for this job')
@moa.args.forceable
@moa.args.commandName('map')
def createMap(job, args):
    """
    create an adhoc moa 'map' job

    Moa will query the user for process, input & output files. A `map`
    job maps a set of input files on a set of output files, executing
    the `process` command for each combination. The `process`
    parameter is interpreted as a Jinja2 template with the input file
    available as `{{ input }}` and the output as `{{ output }}`.

    """
    _createAdhocJob(job, args, 'map', [
            ('process', None ),
            ('input', None),
            ('output', None),
            ])


@moa.args.argument('-t', '--title', help='A title for this job')
@moa.args.forceable
@moa.args.commandName('map!')
def createMapX(job, args):
    """
    create an adhoc moa 'map' job

    This command is exactly the same as `moa map` but uses the Moa
    local (or user) bash history instead.

    """
    _createAdhocJob(job, args, 'map', [
            ( 'process', _get_bash_history_file() ),
            ('input', None),
            ('output', None),
            ])

@moa.args.argument('-t', '--title', help='A title for this job')
@moa.args.forceable
@moa.args.commandName('reduce')
def createReduce(job, args):
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
    _createAdhocJob(job, args, 'reduce', [
            ('process', None ),
            ('input', None),
            ('output', None),
            ])


@moa.args.argument('-t', '--title', help='A title for this job')
@moa.args.forceable
@moa.args.commandName('reduce!')
def createReduceX(job, args):
    """
    Create a 'reduce' adhoc job using the bash history

    This command is exactly the same as moa reduce, but uses the bash
    history instead of the moa process history.
    """
    _createAdhocJob(job, args, 'reduce', [
            ('process', _get_bash_history_file()),
            ('input', None),
            ('output', None),
            ])
