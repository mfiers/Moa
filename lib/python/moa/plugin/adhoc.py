# 
# Copyright 2009 Mark Fiers, Plant & Food Research
# 
# This file is part of Moa - http://github.com/mfiers/Moa
# 
# Moa is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your
# option) any later version.
# 
# Moa is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
# or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public
# License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with Moa.  If not, see <http://www.gnu.org/licenses/>.
# 

"""
Adhoc - some utilities to quickly create adhoc jobs
"""

import os
import sys
import optparse

import moa.job
import moa.logger
import moa.plugin
l = moa.logger.l

#class Adhoc(moa.plugin.BasePlugin):
#    pass

def defineCommands(commands):
    commands['adhoc'] = { 
        'desc' : 'Quickly create an adhoc analysis',
        'call' : createAdhoc
        }

def defineOptions(parser):
    parserN = optparse.OptionGroup(parser, "Moa adhoc (a)")
    parser.set_defaults(directory=".")
    try:
        parserN.add_option("-t", "--title", dest="title", help="Job title")
        parserN.add_option("-d", "--directory", 
                           dest="directory",
                           help="Directory to create the new template in (default: .)")
    except optparse.OptionConflictError:
        pass # probably already defined in the newjob plugin
    parserN.add_option("--mode",
                       dest="mode",
                       help="Directory to create the new template in (default: .)")
    parserN.add_option("-i", "--input",
                       dest="input",
                       help="Input files for this adhoc job")
    parser.add_option_group(parserN)


def createAdhoc(wd, options, args):
    """
    Create an adhoc job
    """

    command = " ".join(args).strip()
    if not command:
        l.critical("need to specify a command")
        sys.exit(-1)

    l.critical('command is: %s' % command)
    params = []
    mode = None
    if options.mode:
        if not options.mode in ['seq', 'par', 'all', 'simple']:
            l.critical("Unknown adhoc mode: %s" % options.mode)
            sys.exit(-1)
        mode = options.mode
    elif '$<' in command:
        mode = 'seq'
        l.info("Setting adhoc mode to 'seq', change to 'par' if you are ")
        l.info(" confident that parallel operation is possible")
    elif ('$^' in command) or ('$?' in command):
        mode = 'all'
        l.info("Observed '$^' or '$?', setting mode to 'all'")
        l.info("Processing all files in one go")
    else:
        mode = 'simple'
        l.info('did not see $? or $^ in the command line')
        l.info('assuming no input files, setting mode to "simple"')

    params += ['adhoc_mode=%s' % options.mode]

    if options.input:
        l.debug("interpreting adhoc input: %s" % options.input)
        i = options.input
        if i[-1] == '/':
            p = 'adhoc_input_dir=%s' % i
            params.append(p)
            l.info('setting %s' % p)
        else:
            path, rest = i.rsplit('/', 1)
            p = 'adhoc_input_dir=%s' % path
            l.debug('setting %s' % p)
            params.append(p)
            l.info('setting %s' % p)
            if '.' in rest:
                glob, ext = rest.rsplit('.', 1)
                if glob != '*':
                    l.debug('setting glob to %s' % glob)
                    params.append('adhoc_input_glob=%s' % glob)
                l.debug('setting extension to %s' % ext)
                params.append('adhoc_input_extension=%s' % ext)
          
    if command: 
        params.append('adhoc_process=%s' % command)

    l.debug('setting parameters %s' % params)
    moa.job.newJob(template='adhoc',
                   wd = wd,
                   title = options.title,
                   force = options.force,
                   parameters=params)


        

