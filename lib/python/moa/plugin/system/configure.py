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
import os
import moa.ui
import moa.utils
import moa.args
import textwrap
import optparse
import moa.logger as l
from moa.sysConf import sysConf

##
## Set command
##
@moa.args.addFlag('-a', dest='showAll', help='show all parameters')
@moa.args.addFlag('-p', dest='showPrivate', help='show private parameters')
@moa.args.addFlag('-R', dest='showRecursive', help='show recursively defined '
                  + 'parameters not specified by the local template')
@moa.args.addFlag('-u', dest='showUnrendered', help='show unrendered values '+
                  '(when using inline parameters)')
@moa.args.needsJob
@moa.args.doNotLog
@moa.args.command
def show(job, args):
    """
    Show all parameters know to this job.

    Parameters in **bold** are specifically configured for this job
    (as opposed to those parameters that are set to their default
    value). Parameters in red are not configured, but need to be for
    the template to operate. Parameters in blue are not configured
    either, but are optional.
    """
    moa.utils.moaDirOrExit(job)

    keys = job.conf.keys()
    keys.sort()

    outkeys = []
    outvals = []
    outflags = []

    rendered = job.conf.render()
    
    for p in keys:

        isPrivate = False
        
        if p[:4] == 'moa_':
            if not args.showAll:
                continue

        if p[0] == '_':
            if not args.showPrivate:
                continue

        #see if this private in the template defintion
        if job.conf.isPrivate(p):
            if args.showPrivate:
                isPrivate = True
            else:
                continue

        if not args.showAll: 
            if job.template.parameters[p].optional and \
                   (not job.conf.setInJobConf(p)):
                #do not show undefined optional parameters unless -a
                #is defined on the command line
                continue

        if args.showRecursive:
            #also - no recursively defined stuff - unless it is relevant
            #to the current job
            if not job.conf.is_local(p):
                continue


        outkeys.append(p)

        #is this variable defined?
        if isPrivate:
            outflags.append('{{red}}p{{reset}}')
            outvals.append(job.conf[p])
        elif job.conf.setInJobConf(p):
            #yes: locally?
            if job.conf.is_local(p):
                outflags.append('{{green}}L{{reset}}')
            else:
                outflags.append('{{magenta}}R{{reset}}')
            outvals.append(job.conf[p])
        else:
            #not defined - does it need to be??            
            if job.template.parameters[p].optional:
                outflags.append('{{blue}}o{{reset}}')
                val = job.conf[p]
                if val != None:
                    outvals.append(
                        moa.ui.fformat('{{gray}}%s{{reset}}' % val, f='j'))
                else:
                    outvals.append(
                        moa.ui.fformat(
                            '{{gray}}(undefined){{reset}}', f='j'))
            else:
                #not optional                
                outflags.append('{{bold}}{{red}}E{{reset}}')
                outvals.append(
                    moa.ui.fformat(
                        '{{red}}{{bold}}(undefined){{reset}}', f='j'))

    maxKeylen = max([len(x) for x in outkeys]) + 1

    termx, termy = moa.utils.getTerminalSize()

    wrapInit = termx - (maxKeylen + 5)
    spacer = ' ' * (maxKeylen + 5)
    spacerR = ' ' * (maxKeylen + 1) + moa.ui.fformat('{{gray}}r ', newline=False, f='j')
    closeR = moa.ui.fformat('{{reset}}', newline=False, f='j')

    #print outkeys
    zipped = zip(outkeys, outvals, outflags)
    
    zipped.sort(lambda x,y: cmp(x[0].lstrip('_'), y[0].lstrip('_')))
    #print outkeys
    
    for i, zippy in enumerate(zipped):
        key, val, flag = zippy
        if not args.showAll:
            if not val: continue
        moa.ui.fprint(("%%-%ds" % maxKeylen) % key, f='jinja', newline=False)
        moa.ui.fprint(" " + flag + " ", f='jinja', newline=False)
        if len(str(val)) == 0:
            print 

        #print str( val)
        #print textwrap.wrap(str(val), wrapInit)

        if args.showUnrendered: mainval = val
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
            for j, ll in enumerate(textwrap.wrap(str(rendered[key]), wrapInit)):
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

@moa.args.argument('parameter', nargs='+', help='arguments for this job, specify' +
                   'as KEY=VALUE without spaces')
@moa.args.forceable
@moa.args.needsJob
@moa.args.command
def set(job, args):
    """
    Set one or more variables
    
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
    """

    #see if we need to query the user for input somehwere
    new_pars = []
    for a in args.parameter:
        if not '=' in a:
            old = job.conf[a]
            val = moa.ui.askUser("%s:\n> " % a, old)
            job.conf[a] = val
            new_pars.append((a,val))
            moa.ui.message('set "%s" to "%s"' % (a, " ".join(val.split())))
        else:
            key,val = a.split('=',1)
            job.conf[key] = val
            new_pars.append((key,val))
            moa.ui.message('set "%s" to "%s"' % (a, " ".join(val.split())))

    job.conf.save()


def hook_git_finish_set():
    """
    Execute just after setting a parameter
    """
    job = sysConf.job
    sysConf.git.commitJob(job, 'moa set %s in %s' % (
        " ".join(sysConf['newargs']), job.wd))
    



