# Copyright 2009-2011 Mark Fiers
# The New Zealand Institute for Plant & Food Research
#
# This file is part of Moa - http://github.com/mfiers/Moa
#
# Licensed under the GPL license (see 'COPYING')
#
"""
**configure** - Configure jobs
------------------------------

Control job configuration
"""

import moa.ui
import moa.utils
import moa.args
import textwrap

from moa.sysConf import sysConf


##
## Show command
##
@moa.args.addFlag('-p', dest='showPrivate', help='show private parameters')
@moa.args.addFlag('-a', dest='showAll', help='show all parameters')
@moa.args.addFlag('-u', dest='showUnrendered', help='show unrendered values')
@moa.args.needsJob
@moa.args.doNotLog
@moa.args.command
def show(job, args):
    """Show parameters known to this job.

    The command outputs three columns, parameter name, flag and
    value. The two flags have the following meaning:

    * Origin: (l) locally defined; (`d`) default value; (`r`) recursively
      defined; (`s`) system defined; (`x`) extra value, not in the
      template; and (`.`) not defined.

    * Private: a `p` indicates this variable to be private.

    * Mandatory: a lower case `o` indicates this to be an optional
      variable and `M` means mandatory.

    """

    moa.utils.moaDirOrExit(job)

    keys = job.conf.keys()
    keys.sort()

    rawTemplate = job.template.getRaw()
    outkeys = []
    outvals = []
    outflags = []

    rendered = job.conf.render()

    for p in keys:

        isPrivate = False

        if p[:4] == 'moa_':
            isPrivate = True

        if p[0] == '_':
            isPrivate = True

        isPrivate = job.conf.isPrivate(p)

        if p[0] == '_':
            isPrivate = True
        if p[:4] == 'moa_':
            isPrivate = True

        isOptional = job.template.parameters[p].get('optional', True)
        isDefault = job.template.parameters[p].get('default') == job.conf[p]
        isLocal = job.conf.is_local(p)
        isDefined = len(str(job.conf[p])) > 0
        isSystem = job.template.parameters[p].get('system', False)
        inTemplate = p in rawTemplate.parameters or p in rawTemplate.filesets

        if isPrivate and not args.showPrivate:
            continue

        if not args.showAll:
            if isOptional and isDefault:
                continue
            if isOptional and (not isDefined):
                continue
        outkeys.append(p)

        key = ''
        if not isDefined:
            key += '{{gray}}.{{reset}}'
            outvals.append('')
        elif isSystem:

            outvals.append(str(job.conf[p]))
            key += '{{bold}}{{red}}s{{reset}}'
        elif isLocal and (not inTemplate):
            outvals.append(str(job.conf[p]))
            key += '{{bold}}{{blue}}x{{reset}}'
        elif isLocal and (not isDefault):
            outvals.append(str(job.conf[p]))
            key += '{{bold}}{{green}}l{{reset}}'
        elif isDefault:
            outvals.append(str(job.conf[p]))
            key += '{{gray}}d{{reset}}'
        else:
            outvals.append(str(job.conf[p]))
            key += '{{magenta}}r{{reset}}'

        if isPrivate:
            key += 'p'
        else:
            key += '{{gray}}.{{reset}}'

        if isOptional:
            key += '{{gray}}o{{reset}}'
        else:
            key += '{{green}}{{red}}M{{reset}}'

        outflags.append(key)

    maxKeylen = max([len(x) for x in outkeys]) + 1

    termx, termy = moa.utils.getTerminalSize()

    wrapInit = termx - (maxKeylen + 5)
    spacer = ' ' * (maxKeylen + 5)
    spacerR = ' ' * (maxKeylen + 1) + \
              moa.ui.fformat('{{gray}}-->  ', newline=False, f='j')
    closeR = moa.ui.fformat('{{reset}}', newline=False, f='j')

    #print outkeys
    zipped = zip(outkeys, outvals, outflags)

    zipped.sort(lambda x, y: cmp(x[0].lstrip('_'), y[0].lstrip('_')))
    #print outkeys

    for i, zippy in enumerate(zipped):
        key, val, flag = zippy

        moa.ui.fprint(("%%-%ds" % maxKeylen) % key, f='jinja', newline=False)
        moa.ui.fprint(" " + flag + "  ", f='jinja', newline=False)
        if len(str(val)) == 0:
            print

        if args.showUnrendered:
            mainval = val
        else:
            renval = rendered[key]
            if str(renval):
                mainval = renval
            else:
                mainval = val

        for j, ll in enumerate(textwrap.wrap(str(mainval), wrapInit)):
            if j == 0:
                moa.ui.fprint(ll, f=None)
            else:
                moa.ui.fprint(spacer + ll, f=None)

        if args.showUnrendered and rendered[key] and rendered[key] != val:
            for j, ll in enumerate(textwrap.wrap(str(rendered[key]),
                                                 wrapInit)):
                moa.ui.fprint(spacerR + ll + closeR)


@moa.args.argument('parameter', nargs='+', help='parameter to unset')
@moa.args.needsJob
@moa.args.command
def unset(job, args):
    """
    Remove a parameter from the configuration

    Remove a configured parameter from this job. In the parameter was
    defined by the job template, it reverts back to the default
    value. If it was an ad-hoc parameter, it is lost from the
    configuration.
    """

    for a in args.parameter:
        if '=' in a:
            moa.ui.exitError("Invalid argument to unset %s" % a)
        try:
            del job.conf[a]
            moa.ui.message('unset %s' % a)
        except KeyError:
            #probably a non existsing key - ignor
            moa.ui.warn('failed to unset %s' % a)
            pass
    job.conf.save()


@moa.args.argument('parameter', nargs='+',
                   help='arguments for this job, specify' +
                   'as KEY=VALUE without spaces')
@moa.args.addFlag('-s', '--system', help='store this a ' +
                  'system configuration variable')
@moa.args.forceable
@moa.args.command
def set(job, args):
    """Set one or more variables

    This command can be used in two ways. In its first form both
    parameter key and value are defined on the command line: `moa set
    KEY=VALUE`. Note that the command line will be processed by bash,
    which can either create complications or prove very useful. Take
    care to escape variables that you do not want to be expandend and
    use single quotes where necessary. For example, to include a space
    in a variable: `moa set KEY='VALUE WITH SPACES'`.

    Alternative use of the set command is by just specifying the key:
    'moa set PARAMETER_NAME', in which case Moa will prompt the user
    enter a value - circumventing problems with bash interpretation.

    Note: without -s, moa needs to be executed from within a Moa job

    System configuration
    ####################

    By specifying `-s` or `--system`, the variable is stored as a
    system configuration variable in the YAML formatted
    `~/.config/moa/config`. Please, use this with care!

    The dots in the key name are interpreted as nested levels, so,
    running::

        moa set -s plugins.job.completion.enabled=false

    will result in the following section added on top of the YAML::

        plugins:
            job:
                completion:
                    enabled: false

    Adding keys like this mixes safely with configuration information
    that is already present. So, setting::

        moa set -s plugins.job.completion.something=else

    will not remove the `enabled: false` heading under `completion:`,
    resulting in::


        plugins:
            job:
                completion:
                    enabled: false
                    someting: else

    """

    #see if we need to query the user for input somehwere
    if not args.system:
        moa.utils.moaDirOrExit(job)

    new_pars = []
    for a in args.parameter:

        if not '=' in a:
            old = job.conf[a]
            key = a
            val = moa.ui.askUser("%s:\n> " % a, old)
        else:
            key, val = a.split('=', 1)

        if not args.system:
            job.conf[key] = val

        new_pars.append((key, val))
        moa.ui.message('setting "%s" to "%s"' % (key, " ".join(val.split())))

    if args.system:

        sys_pars = dict(new_pars)

        valCheck = {
            'true': True,
            'false': False}

        def _dictify(d):
            for k in list(d.keys()):
                if '.' in k:

                    na, nb = k.split('.', 1)
                    d[na] = _dictify({nb: d[k]})
                    del d[k]
                else:
                    val = d[k]
                    if val.lower() in valCheck:
                        val = valCheck[val.lower()]
                        d[k] = val
            return d

        userConf = sysConf.getUser()
        userConf.update(_dictify(sys_pars))
        sysConf.saveUser(userConf)
    else:
        job.conf.save()


def hook_git_finish_set():
    """
    Execute just after setting a parameter
    """
    job = sysConf.job
    sysConf.api.git_commit_job(
        job, 'moa set %s in %s' % (
        " ".join(sysConf['newargs']), job.wd))
