#!/usr/bin/env python
"""
Wrapper around argparse for Moa
"""

import re
import argparse
import inspect
from moa.sysConf import sysConf

import moa.ui
import moa.exceptions
import moa.logger as l



class MoaHelpFormatter(argparse.HelpFormatter):
    """
    Copy pasted some code from argparse.py - and made minor changes
    to better suit the moa help.
    """
    def _metavar_formatter(self, action, default_metavar):
        if action.metavar is not None:
            result = action.metavar
        elif action.choices is not None:
            result = '{command}'
        else:
            result = default_metavar

        def format(tuple_size):
            if isinstance(result, tuple):
                return result
            else:
                return (result, ) * tuple_size
        return format


    def _format_action(self, action):
        # determine the required width and the entry label
        help_position = min(self._action_max_length + 2,
                            self._max_help_position)
        help_width = self._width - help_position
        action_width = help_position - self._current_indent - 2
        
        if action.dest == 'command':
            action_header = argparse.SUPPRESS
        else: 
            action_header = self._format_action_invocation(action)

        # no nelp; start on same line and add a final newline
        if not action.help:
            tup = self._current_indent, '', action_header
            action_header = '%*s%s\n' % tup

        # short action name; start on the same line and pad two spaces
        elif len(action_header) <= action_width:
            tup = self._current_indent, '', action_width, action_header
            action_header = '%*s%-*s  ' % tup
            indent_first = 0
        # long action name; start on the next line
        else:
            tup = self._current_indent, '', action_header
            action_header = '%*s%s\n' % tup
            indent_first = help_position

        # collect the pieces of the action help
        parts = [action_header]

        # if there was help for the action, add lines of help text
        if action.help:            
            help_text = self._expand_help(action)
            help_lines = self._split_lines(help_text, help_width)
            if argparse.SUPPRESS in action_header:
                parts = []
            else:
                parts.append('%*s%s\n' % (indent_first, '', help_lines[0]))
            for line in help_lines[1:]:
                parts.append('%*s%s\n' % (help_position, '', line))

        # or add a newline if the description doesn't end with one
        elif not action_header.endswith('\n'):
            parts.append('\n')

        # if there are any sub-actions, add their help as well
        for subaction in self._iter_indented_subactions(action):
            flag = "."
            if not subaction.dest in sysConf.commands:
                continue
            if sysConf.commands[subaction.dest]['private']:
                continue
            if sysConf.commands[subaction.dest].get('needsJob') and \
               (not sysConf.job.isMoa()):
                continue
            if sysConf.commands[subaction.dest].get('source', '') == \
                   'template':
                flag='*'
            elif sysConf.commands[subaction.dest].get('needsJob', False):
                flag='j'
                
            if not re.match(r'^[\*j.] .*$', subaction.help):
                subaction.help = '%s %s' % (flag, subaction.help)

            parts.append(self._format_action(subaction))

        # return a single string
        return self._join_parts(parts)

class MoaArgumentParser(argparse.ArgumentParser):
        
    def error(self, message):
        """error(message: string)
        Prints a usage message incorporating the message to stderr and
        exits.
        
        If you override this in a subclass, it should not return -- it
        should either exit or raise an exception.
        """
        self.error_message = message
        raise moa.exceptions.MoaInvalidCommandLine, self
    
    def real_error(self):
        """
        after argparser.error, but takes the message from self.error_meesage

        this structure allows problems to be raise and caught
        """

        self.print_usage(argparse._sys.stderr)
        self.exit(2, argparse._('%s: error: %s\n') % (self.prog, self.error_message))
                   
                                


def getParser(reuse=True):
    
    if reuse and  sysConf.argParser:
        return sysConf.argParser, sysConf.commandParser
    else:
        parser =  MoaArgumentParser(
            formatter_class=MoaHelpFormatter)

        hlptxt = ("Command legend: '.' can be executed everywhere; "+
                  "'j' require a job; '*' are specified by the template")
            
        commandParser = parser.add_subparsers(
            title='command', help='Moa Command', dest='command',
            description=hlptxt)
        
        sysConf.argParser = parser
        sysConf.commandParser =  commandParser
        return parser, commandParser

#
# Decorators - @command must always come last (hence - is executed first)
#

def _commandify(f, name):
    """
    Do the actual commandification of function f with specified name 
    """
    try:
        assert(inspect.getargspec(f).args == ['job', 'args'])
    except AssertionError:
        moa.ui.exitError("Command function for %s seems invalid - contact a developer" % name)

    l.debug("registering command %s" % name)
    _desc = [x.strip() for x in f.__doc__.strip().split("\n", 1)]
    if len(_desc) == 2:
        shortDesc, longDesc = _desc
    else:
        shortDesc = _desc[0]
        longDesc = ''
    
    parser, cparser = getParser()
    
    cp = cparser.add_parser(
       name, help= shortDesc,
        description="%s %s" % ( shortDesc, longDesc))


    cp.add_argument("-r", "--recursive", dest="recursive", action="store_true",
                    default="false", help="Run this job recursively")

    cp.add_argument("-v", "--verbose", dest="verbose", action="store_true",
                    help="Show debugging output")

    
    cp.add_argument("--profile", dest="profile", action="store_true",
                    help="Run the profiler")

    sysConf.commands[name] = {
        'desc' : shortDesc,
        'long' : longDesc,
        'recursive' : 'gbobal',
        'needsJob' : False,
        'call' : f,
        }
    f.arg_parser = cp
    return f
    

def command(f):
    """
    Decorator for any function in moa - name is derived from function name
    """
    return _commandify(f, f.__name__)

def commandName(name):
    """
    Decorate a function as a moa command with the option to specify a
    name for the function
    """
    def decorator(f):
        return _commandify(f, name)
    return decorator

def argument(*args, **kwargs):
    """
    Add an argument to a function
    """
    def decorator(f):
        f.arg_parser.add_argument(*args, **kwargs)
        return f
    return decorator

def addFlag(*args, **kwargs):
    """
    Add a flag to (default false - true if specified) any command
    """
    def decorator(f):
        if not kwargs.has_key('action'):
            kwargs['action'] = 'store_true'
        if not kwargs.has_key('default'):
            kwargs['default'] = False
        f.arg_parser.add_argument(*args, **kwargs)
        return f
    return decorator
    
def needsJob(f):
    sysConf.commands[f.func_name]['needsJob'] = True
    return f

def localRecursive(f):
    sysConf.commands[f.func_name]['recursive'] = 'local'
    return f

def private(f):
    sysConf.commands[f.func_name]['private'] = True

def forceable(f):
    f.arg_parser.add_argument('-f', '--force', action='store_true',
                              default=False, help='Force this action')
    return f
    
