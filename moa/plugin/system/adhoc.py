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

def _checkTitle(t):
    """
    check if there is anything resembling a title in `t` - otherwise
    ask the user for one
    """
    if t is None or str(t).strip() == "":
        return moa.ui.askUser("Title: ")
    else:
        return t


@moa.args.argument('-t', '--title', help='A title for this job')
@moa.args.forceable
@moa.args.command
def simple(job, args):
    """
    Create a 'simple' adhoc job.

    Simple meaning that no in or output files are tracked. Moa will
    query you for a command to execute (the `process` parameter).
    """

    wd = job.wd
    if (not args.force and
            os.path.exists(os.path.join(wd, '.moa', 'template'))):

        moa.ui.exitError("Job already exists, use -f to override")

    command = moa.ui.askUser('process:\n> ', '')

    params = [('process', command)]

    #make sure the correct hooks are called
    sysConf.pluginHandler.run("preNew")

    title = _checkTitle(args.title)

    job = moa.job.newJob(
        job, template='simple',
        title=title,
        parameters=params)

    #make sure the correct hooks are called
    sysConf.pluginHandler.run("postNew")


def exclamateNoJob(job, args, command):
    """
    Create a "simple" job & set the last command
    to the 'process' parameter
    """

    title = _checkTitle(args.title)

    job = moa.job.newJob(
        job, template='simple',
        title=title,
        parameters=[('process', command)])


def exclamateInJob(job, args, command):
    """
    Reuse the last issued command: set it as the 'process' parameters
    in the current job
    """
    moa.ui.fprint("{{bold}}Using command:{{reset}}", f='jinja')
    moa.ui.fprint(command)
    job.conf.process = command
    job.conf.save()


@moa.args.argument('-t', '--title', help='A title for this job')
@moa.args.forceable
@moa.args.commandName('!')
def exclamate(job, args):
    """
    Create a 'simple' job from the last command issued.

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

    pc = os.environ.get('PROMPT_COMMAND', '')
    if not '_moa_prompt' in pc:
        moa.ui.exitError("moa is not set up to capture the last command")

    histFile = os.path.join(os.path.expanduser('~'), '.moa.last.command')
    with open(histFile) as F:
        last = F.readlines()[-1].strip()

    if job.isMoa():
        exclamateInJob(job, args, last)
    else:
        exclamateNoJob(job, args, last)


@moa.args.argument('-t', '--title', help='A title for this job')
@moa.args.forceable
@moa.args.commandName('map')
def createMap(job, args):
    """
    create an adhoc moa 'map' job

    Moa will query the user for process, input & output files. An
    example session
    """
    wd = job.wd

    if (not args.force and
            os.path.exists(os.path.join(wd, '.moa', 'template'))):

        moa.ui.exitError("Job already exists, use -f to override")


    params = []

    command = moa.ui.askUser('process:\n> ', '')

    params.append(('process', command))


    title = _checkTitle(args.title)

    input = moa.ui.askUser('input:\n> ', '')
    output = moa.ui.askUser('output:\n> ', './*')
    params.append(('input', input))
    params.append(('output', output))

    moa.job.newJob(
        job, template='map',
        title=title,
        parameters=params)


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
    wd = job.wd

    if (not args.force and
            os.path.exists(os.path.join(wd, '.moa', 'template'))):

        moa.ui.exitError("Job already exists, use -f to override")

    params = []

    command = moa.ui.askUser('process:\n> ', '')

    params.append(('process', command))

    title = _checkTitle(args.title)

    input = moa.ui.askUser('input:\n> ', '')
    output = moa.ui.askUser('output:\n> ', './output')
    params.append(('input', input))
    params.append(('output', output))

    moa.job.newJob(
        job, template='reduce',
        title=title,
        parameters=params)


### Old adhoc code - still here for historical purposes
def _sourceOrTarget(g):
    """
    Determine if this glob is a likely source or
    target, depending on where the output is aimed to go
    """
    d = g.groups()[0]
    if not d:
        return 'target'
    if d[:2] == './': return 'target'

    if d[:2] == '..': return 'source'
    if d[0] == '/':
        return 'source'
    return 'target'

