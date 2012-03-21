#!/usr/bin/env python
"""
Wrapper around argparse for Moa
"""

import argparse
import inspect
from moa.sysConf import sysConf

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
            if not subaction.dest in sysConf.commands:
                print subaction.dest, self._format_action(subaction)
                continue
            if sysConf.commands[subaction.dest]['private']:
                continue
            parts.append(self._format_action(subaction))

        # return a single string
        return self._join_parts(parts)


def getParser():
    if sysConf.args.parser:
        return sysConf.args.parser, sysConf.args.cParser
    else:
        parser =  argparse.ArgumentParser(
            formatter_class=MoaHelpFormatter)
        commandParser = parser.add_subparsers(
            title='command', help='Moa Command', dest='command',
            description='Any of the following Moa commands')
        
        sysConf.args.parser = parser
        sysConf.args.cParser =  commandParser
        return parser, commandParser

#
# Decorators - @command must always come last (hence - is executed first)
#

def command(f):
    name = f.func_name
    assert(inspect.getargspec(f).args == ['job', 'args'])
    l.debug("registering command %s" % name)
    _desc = [x.strip() for x in f.__doc__.strip().split("\n", 1)]
    if len(_desc) == 2:
        shortDesc, longDesc = _desc
    else:
        shortDesc = _desc[0]
        longDesc = ''
    
    parser, cparser = getParser()
    
    this_parser = cparser.add_parser(
       name, help= shortDesc,
        description="%s %s" % ( shortDesc, longDesc))

    sysConf.commands[name] = {
        'desc' : shortDesc,
        'long' : longDesc,
        'recursive' : 'gbobal',
        'needsJob' : False,
        'call' : f,
        }
    f.arg_parser = this_parser
    return f


def argument(*args, **kwargs):
    def decorator(f):
        f.arg_parser.add_argument(*args, **kwargs)
        return f
    return decorator

def addFlag(*args, **kwargs):
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

def private(f):
    sysConf.commands[f.func_name]['private'] = True

def forceable(f):
    f.arg_parser.add_argument('-f', '--force', action='store_true',
                              default=False, help='Force this action')
    return f
    
