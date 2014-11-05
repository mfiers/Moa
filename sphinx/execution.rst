Execution
=========

What is executed upon a Moa run can either be defined by a plugin, or
by a template. Most Moa commands (such as `moa show` are plugin
defined). Only `moa prepare`, `moa run` and `moa finish` call code
defined in a template. A number of steps are:

Main invocation
---------------

The complete Moa Invocation is embedded in a try / except.

On an error, Moa tries to execute a `post_error` hook and then attempts to fail quietly. 
If you are interested in the actual error, run moa with the
'-v' flag

Upon a keyboard interrupt, Moa executes the `post_interrupt` hook and
exists with a return code of -2.

Background execution
--------------------

The first thing Moa does is to check if '--bg' is defined on the
command line? If so, fork, let the child thread continue and let
parent thread exit.

Before continuation, the parent thread executes the `background_exit`
hook before exit. The child thread executes the `post_background`
hook before continuing.

Recursive execution
-------------------

Moa **used** to have the '-r' flag for all operations, allowing
recursive operation of Moa. This was rather confusing and has been
removed. Some commands still define -r (such as 'moa cp'), but for the
majority of commands, you will need to use bash (find, xargs, etc), or
use the new, stand-alone, helper script 'moar'. Using 'moar' is very
simple::

    moar -- moa run

runs 'moa run' in this directory, and all (non hidden)
sub-directories. If you would like to limit execution to a certain
depth, for example only first level sub-directories, you can run::

    moar -d 1 -- moa run




