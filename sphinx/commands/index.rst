Command reference
=================

.. _command_moa_run:

moa **run**
~~~~~~~~~~~~~~~~~~~~~~~

usage: moa run [-h] [-v] [--bg] [--profile] [-j THREADS] [--ol]
               [--olq OPENLAVAQUEUE] [--olx OPENLAVAEXTRA]
               [--oln OPENLAVAPROCS] [--oldummy] [--olm OPENLAVAHOST]

execute the template 'run' command. Execution depends on the
template. This command can only be exeucted from within a template.

optional arguments:
  -h, --help           show this help message and exit
  -v, --verbose        Show debugging output
  --bg                 Run moa in the background (implies -s)
  --profile            Run the profiler
  -j THREADS           No threads to use when running Ruffus
  --ol                 Use OpenLava as actor
  --olq OPENLAVAQUEUE  The Openlava queue to submit this job to
  --olx OPENLAVAEXTRA  Extra arguments for bsub
  --oln OPENLAVAPROCS  The number of processors the jobs requires
  --oldummy            Do not execute - just create a script to run
  --olm OPENLAVAHOST   The host to use for openlava

~~~~~~~~~~~~~~~~~~.. _command_moa_archive:

moa **archive**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

~~~~~~~~~~~~~~~~~~
usage: moa archive [-h] [-v] [--profile] [-f] [-s] [-t] [name]

Archive a job, or tree with jobs for later reuse.

This command stores only those files that are necessary for
execution of this job, that is: templates & configuration. In &
output files, and any other file are ignored. An exception to this
are all files that start with 'moa. If the `name` is omitted, it
is derived from the `jobid` parameter.

It is possible to run this command recursively with the `-r`
parameter - in which case all (moa job containing) subdirectories
are included in the archive.

positional arguments:
  name            archive name (default: None)

optional arguments:
  -h, --help      show this help message and exit
  -v, --verbose   Show debugging output (default: False)
  --profile       Run the profiler (default: False)
  -f, --force     Force this action (default: False)
  -s, --sync      Alternative approach to deal with sync type jobs - only include _ref directories (default: False)
  -t, --template  Store this archive as a template (default: False)

~~~~~~~~~~~~~~~~~~


.. _command_moa_archive_excl:

moa **archive_excl**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

~~~~~~~~~~~~~~~~~~
usage: moa archive_excl [-h] [-v] [--profile]

Toggle a directory to be included in an moa archive.

optional arguments:
  -h, --help     show this help message and exit
  -v, --verbose  Show debugging output (default: False)
  --profile      Run the profiler (default: False)

~~~~~~~~~~~~~~~~~~


.. _command_moa_archive_incl:

moa **archive_incl**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

~~~~~~~~~~~~~~~~~~
usage: moa archive_incl [-h] [-v] [--profile]

Toggle a directory to be included in an moa archive.

optional arguments:
  -h, --help     show this help message and exit
  -v, --verbose  Show debugging output (default: False)
  --profile      Run the profiler (default: False)

~~~~~~~~~~~~~~~~~~


.. _command_moa_blog:

moa **blog**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

~~~~~~~~~~~~~~~~~~
usage: moa blog [-h] [-v] [--profile] [-t TITLE] [message [message ...]]

Add an entry to the job blog (in .moa/doc/blog/)

Allows a user to maintain a blog for this job. Use as
follows::

    $ moa blog
    Enter your blog message (ctrl-d on an empty line to finish)

    ... enter your message here ..

    [ctrl-d]

Note: the ctrl-d needs to be given on an empty line. The text is
appended to moa.desciption. In the web interface this is converted
to Markdown_.

.. _Markdown: http://daringfireball.net/projects/markdown/ markdown.

positional arguments:
  message

optional arguments:
  -h, --help            show this help message and exit
  -v, --verbose         Show debugging output (default: False)
  --profile             Run the profiler (default: False)
  -t TITLE, --title TITLE
                        mandatory job title (default: None)

~~~~~~~~~~~~~~~~~~


.. _command_moa_change:

moa **change**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

~~~~~~~~~~~~~~~~~~
usage: moa change [-h] [-v] [--profile] [-t TITLE] [message [message ...]]

Add entry to CHANGELOG.md

This function allows the user to add an entry to CHANGELOG.md
(including a timestamp). Use it as follows::

    $ moa change
    Enter your changelog message (ctrl-d on an empty line to finish)

    ... enter your message here ..

    [ctrl-d]

Note: the ctrl-d needs to be given on an empty line. The text is
appended to moa.desciption. In the web interface this is converted
to Markdown_.

.. _Markdown: http://daringfireball.net/projects/markdown/ markdown.

Note the same can be achieved by specifying the -m parameter
(before the command - for example:

`moa -m 'intelligent remark' set ...`

Note. It is also possible to cat some text into moa change:

wc -l | moa change

Moa will still query you for a message and append the data from
stdin to the message

positional arguments:
  message

optional arguments:
  -h, --help            show this help message and exit
  -v, --verbose         Show debugging output (default: False)
  --profile             Run the profiler (default: False)
  -t TITLE, --title TITLE
                        mandatory job title (default: None)

~~~~~~~~~~~~~~~~~~


.. _command_moa_changelog:

moa **changelog**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

~~~~~~~~~~~~~~~~~~
usage: moa changelog [-h] [-v] [--profile] [no_entries]

Print a changelog to stdout

positional arguments:
  no_entries     No of changelog entries to show (default 10) (default: 10)

optional arguments:
  -h, --help     show this help message and exit
  -v, --verbose  Show debugging output (default: False)
  --profile      Run the profiler (default: False)

~~~~~~~~~~~~~~~~~~


.. _command_moa_clean:

moa **clean**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

~~~~~~~~~~~~~~~~~~
usage: moa clean [-h] [-v] [--profile]

Clean everything except the moa job from a directory.

moa clean removes all files in the current directory plus all
known output files that are not in the current directory. Empty
directories will be removed as well.

Note that this command can be overridden by defining a template
"clean" command

optional arguments:
  -h, --help     show this help message and exit
  -v, --verbose  Show debugging output (default: False)
  --profile      Run the profiler (default: False)

~~~~~~~~~~~~~~~~~~


.. _command_moa_cp:

moa **cp**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

~~~~~~~~~~~~~~~~~~
usage: moa cp [-h] [-v] [--profile] [-r] [-o] from [to]

Copy a moa job, or a tree with jobs (with -r).

moa cp copies only those files defining a job: the template files
and the job configuration. Additionaly, all files in the moa
directory that start with `moa.` (for example `moa.description`
are copied as well. Data and log files are not copied!. If used in
conjunction with the -r (recursive) flag the complete tree is
copied.

positional arguments:
  from             copy from
  to               copy to (default: None)

optional arguments:
  -h, --help       show this help message and exit
  -v, --verbose    Show debugging output (default: False)
  --profile        Run the profiler (default: False)
  -r, --recursive  copy recursively - including all subdirectories (default: False)
  -o, --overwrite  if the target dir exists - overwrite (instead of copying into that dir (default: False)

~~~~~~~~~~~~~~~~~~


.. _command_moa_dumpTemplate:

moa **dumpTemplate**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

~~~~~~~~~~~~~~~~~~
usage: moa dumpTemplate [-h] [-v] [--profile]

**moa template_dump** - Show raw template information

Usage::

   moa template_dump [TEMPLATE_NAME]

Show the raw template sysConf.

optional arguments:
  -h, --help     show this help message and exit
  -v, --verbose  Show debugging output (default: False)
  --profile      Run the profiler (default: False)

~~~~~~~~~~~~~~~~~~


.. _command_moa_err:

moa **err**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

~~~~~~~~~~~~~~~~~~
usage: moa err [-h] [-v] [--profile]

Show the stderr of the most recently executed moa job

optional arguments:
  -h, --help     show this help message and exit
  -v, --verbose  Show debugging output (default: False)
  --profile      Run the profiler (default: False)

~~~~~~~~~~~~~~~~~~


.. _command_moa_files:

moa **files**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

~~~~~~~~~~~~~~~~~~
usage: moa files [-h] [-v] [--profile] [-a] [-n NO_FILES]

Show in and output files for this job

Display a list of all files discovered (for input & prerequisite
type filesets) and inferred from these for map type filesets.

optional arguments:
  -h, --help            show this help message and exit
  -v, --verbose         Show debugging output (default: False)
  --profile             Run the profiler (default: False)
  -a, --all             Show all filesets (default: False)
  -n NO_FILES, --no_files NO_FILES
                        No filesets to show (default 10) (default: 10)

~~~~~~~~~~~~~~~~~~


.. _command_moa_gitadd:

moa **gitadd**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

~~~~~~~~~~~~~~~~~~
usage: moa gitadd [-h] [-v] [--profile]

add this job to a git repository

optional arguments:
  -h, --help     show this help message and exit
  -v, --verbose  Show debugging output (default: False)
  --profile      Run the profiler (default: False)

~~~~~~~~~~~~~~~~~~


.. _command_moa_gitlog:

moa **gitlog**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

~~~~~~~~~~~~~~~~~~
usage: moa gitlog [-h] [-v] [--profile]

Print a log to screen

optional arguments:
  -h, --help     show this help message and exit
  -v, --verbose  Show debugging output (default: False)
  --profile      Run the profiler (default: False)

~~~~~~~~~~~~~~~~~~


.. _command_moa_kill:

moa **kill**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

~~~~~~~~~~~~~~~~~~
usage: moa kill [-h] [-v] [--profile]

Kill a running job.

This command checks if a job is running. If so - it tries to kill
it by sending SIGKILL (-9) to the job.

optional arguments:
  -h, --help     show this help message and exit
  -v, --verbose  Show debugging output (default: False)
  --profile      Run the profiler (default: False)

~~~~~~~~~~~~~~~~~~


.. _command_moa_list:

moa **list**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

~~~~~~~~~~~~~~~~~~
usage: moa list [-h] [-v] [--profile]

Lists all known local templates

Print a list of all templates known to this moa installation. This
includes locally installed templates as well.

optional arguments:
  -h, --help     show this help message and exit
  -v, --verbose  Show debugging output (default: False)
  --profile      Run the profiler (default: False)

~~~~~~~~~~~~~~~~~~


.. _command_moa_lock:

moa **lock**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

~~~~~~~~~~~~~~~~~~
usage: moa lock [-h] [-v] [--profile]

Lock a job - prevent execution

optional arguments:
  -h, --help     show this help message and exit
  -v, --verbose  Show debugging output (default: False)
  --profile      Run the profiler (default: False)

~~~~~~~~~~~~~~~~~~


.. _command_moa_log:

moa **log**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

~~~~~~~~~~~~~~~~~~
usage: moa log [-h] [-v] [--profile]

Show activity log

Shows a log of moa commands executed. Only commands with an impact
on the pipeline are logged, such as `moa run` & `moa set`.

optional arguments:
  -h, --help     show this help message and exit
  -v, --verbose  Show debugging output (default: False)
  --profile      Run the profiler (default: False)

~~~~~~~~~~~~~~~~~~


.. _command_moa_map:

moa **map**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

~~~~~~~~~~~~~~~~~~
usage: moa map [-h] [-v] [--profile] [-f] [-t TITLE]

create an adhoc moa 'map' job

Moa will query the user for process, input & output files. A `map`
job maps a set of input files on a set of output files, executing
the `process` command for each combination. The `process`
parameter is interpreted as a Jinja2 template with the input file
available as `{{ input }}` and the output as `{{ output }}`.

optional arguments:
  -h, --help            show this help message and exit
  -v, --verbose         Show debugging output (default: False)
  --profile             Run the profiler (default: False)
  -f, --force           Force this action (default: False)
  -t TITLE, --title TITLE
                        A title for this job (default: None)

~~~~~~~~~~~~~~~~~~


.. _command_moa_map!:

moa **map!**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

~~~~~~~~~~~~~~~~~~
usage: moa map! [-h] [-v] [--profile] [-f] [-t TITLE]

create an adhoc moa 'map' job

This command is exactly the same as `moa map` but uses the Moa
local (or user) bash history instead.

optional arguments:
  -h, --help            show this help message and exit
  -v, --verbose         Show debugging output (default: False)
  --profile             Run the profiler (default: False)
  -f, --force           Force this action (default: False)
  -t TITLE, --title TITLE
                        A title for this job (default: None)

~~~~~~~~~~~~~~~~~~


.. _command_moa_mv:

moa **mv**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

~~~~~~~~~~~~~~~~~~
usage: moa mv [-h] [-v] [--profile] from [to]

Move, rename or renumber a moa job.

positional arguments:
  from           copy from
  to             copy to (default: None)

optional arguments:
  -h, --help     show this help message and exit
  -v, --verbose  Show debugging output (default: False)
  --profile      Run the profiler (default: False)

~~~~~~~~~~~~~~~~~~


.. _command_moa_new:

moa **new**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

~~~~~~~~~~~~~~~~~~
usage: moa new [-h] [-v] [--profile] [-f] [-t TITLE]
               template [parameter [parameter ...]]

Create a new job.

This command creates a new job with the specified template in the
current directory. If the directory already contains a job it
needs to be forced using '-f'. It is possible to define arguments
for the job on the commandline using KEY=VALUE after the
template. Note: do not use spaces around the '=' sign. Use quotes
if you need spaces in variables (KEY='two values')

positional arguments:
  template              name of the template to use for this moa job 
  parameter             arguments for this job, specifyas KEY=VALUE without spaces (default: None)

optional arguments:
  -h, --help            show this help message and exit
  -v, --verbose         Show debugging output (default: False)
  --profile             Run the profiler (default: False)
  -f, --force           Force this action (default: False)
  -t TITLE, --title TITLE
                        mandatory job title (default: )

~~~~~~~~~~~~~~~~~~


.. _command_moa_out:

moa **out**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

~~~~~~~~~~~~~~~~~~
usage: moa out [-h] [-v] [--profile]

Show the stdout of the most recently executed moa job

optional arguments:
  -h, --help     show this help message and exit
  -v, --verbose  Show debugging output (default: False)
  --profile      Run the profiler (default: False)

~~~~~~~~~~~~~~~~~~


.. _command_moa_pause:

moa **pause**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

~~~~~~~~~~~~~~~~~~
usage: moa pause [-h] [-v] [--profile]

Pause a running job

optional arguments:
  -h, --help     show this help message and exit
  -v, --verbose  Show debugging output (default: False)
  --profile      Run the profiler (default: False)

~~~~~~~~~~~~~~~~~~


.. _command_moa_pelican:

moa **pelican**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

~~~~~~~~~~~~~~~~~~
usage: moa pelican [-h] [-v] [--profile]

Run pelican :)

optional arguments:
  -h, --help     show this help message and exit
  -v, --verbose  Show debugging output (default: False)
  --profile      Run the profiler (default: False)

~~~~~~~~~~~~~~~~~~


.. _command_moa_postcommand:

moa **postcommand**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

~~~~~~~~~~~~~~~~~~
usage: moa postcommand [-h] [-v] [--profile]

Execute 'postcommand'

optional arguments:
  -h, --help     show this help message and exit
  -v, --verbose  Show debugging output (default: False)
  --profile      Run the profiler (default: False)

~~~~~~~~~~~~~~~~~~


.. _command_moa_precommand:

moa **precommand**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

~~~~~~~~~~~~~~~~~~
usage: moa precommand [-h] [-v] [--profile]

Execute 'precommand'

optional arguments:
  -h, --help     show this help message and exit
  -v, --verbose  Show debugging output (default: False)
  --profile      Run the profiler (default: False)

~~~~~~~~~~~~~~~~~~


.. _command_moa_raw_commands:

moa **raw_commands**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

~~~~~~~~~~~~~~~~~~
usage: moa raw_commands [-h] [-v] [--profile]

return a list available commands

Print a list of known Moa commands, both global, plugin defined
commands as template specified ones. This command meant to be used
by software interacting with Moa.

optional arguments:
  -h, --help     show this help message and exit
  -v, --verbose  Show debugging output (default: False)
  --profile      Run the profiler (default: False)

~~~~~~~~~~~~~~~~~~


.. _command_moa_raw_parameters:

moa **raw_parameters**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

~~~~~~~~~~~~~~~~~~
usage: moa raw_parameters [-h] [-v] [--profile]

Print a list of all known parameters

optional arguments:
  -h, --help     show this help message and exit
  -v, --verbose  Show debugging output (default: False)
  --profile      Run the profiler (default: False)

~~~~~~~~~~~~~~~~~~


.. _command_moa_readme:

moa **readme**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

~~~~~~~~~~~~~~~~~~
usage: moa readme [-h] [-v] [--profile]

Edit the README.md file for this job

You could, obviously, also edit the file yourself - this is a mere
shortcut - maybe it will stimulate you to maintain a README file

optional arguments:
  -h, --help     show this help message and exit
  -v, --verbose  Show debugging output (default: False)
  --profile      Run the profiler (default: False)

~~~~~~~~~~~~~~~~~~


.. _command_moa_reduce:

moa **reduce**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

~~~~~~~~~~~~~~~~~~
usage: moa reduce [-h] [-v] [--profile] [-f] [-t TITLE]

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

optional arguments:
  -h, --help            show this help message and exit
  -v, --verbose         Show debugging output (default: False)
  --profile             Run the profiler (default: False)
  -f, --force           Force this action (default: False)
  -t TITLE, --title TITLE
                        A title for this job (default: None)

~~~~~~~~~~~~~~~~~~


.. _command_moa_reduce!:

moa **reduce!**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

~~~~~~~~~~~~~~~~~~
usage: moa reduce! [-h] [-v] [--profile] [-f] [-t TITLE]

Create a 'reduce' adhoc job using the bash history

This command is exactly the same as moa reduce, but uses the bash
history instead of the moa process history.

optional arguments:
  -h, --help            show this help message and exit
  -v, --verbose         Show debugging output (default: False)
  --profile             Run the profiler (default: False)
  -f, --force           Force this action (default: False)
  -t TITLE, --title TITLE
                        A title for this job (default: None)

~~~~~~~~~~~~~~~~~~


.. _command_moa_refresh:

moa **refresh**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

~~~~~~~~~~~~~~~~~~
usage: moa refresh [-h] [-v] [--profile]

Refresh the template

Reload the template from the original repository.

optional arguments:
  -h, --help     show this help message and exit
  -v, --verbose  Show debugging output (default: False)
  --profile      Run the profiler (default: False)

~~~~~~~~~~~~~~~~~~


.. _command_moa_rehash:

moa **rehash**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

~~~~~~~~~~~~~~~~~~
usage: moa rehash [-h] [-v] [--profile]

cache a list of variables for command line completion

optional arguments:
  -h, --help     show this help message and exit
  -v, --verbose  Show debugging output (default: False)
  --profile      Run the profiler (default: False)

~~~~~~~~~~~~~~~~~~


.. _command_moa_resume:

moa **resume**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

~~~~~~~~~~~~~~~~~~
usage: moa resume [-h] [-v] [--profile]

Resume a running job

optional arguments:
  -h, --help     show this help message and exit
  -v, --verbose  Show debugging output (default: False)
  --profile      Run the profiler (default: False)

~~~~~~~~~~~~~~~~~~


.. _command_moa_set:

moa **set**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

~~~~~~~~~~~~~~~~~~
usage: moa set [-h] [-v] [--profile] [-f] [-s] parameter [parameter ...]

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

positional arguments:
  parameter      arguments for this job, specifyas KEY=VALUE without spaces

optional arguments:
  -h, --help     show this help message and exit
  -v, --verbose  Show debugging output (default: False)
  --profile      Run the profiler (default: False)
  -f, --force    Force this action (default: False)
  -s, --system   store this a system configuration variable (default: False)

~~~~~~~~~~~~~~~~~~


.. _command_moa_show:

moa **show**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

~~~~~~~~~~~~~~~~~~
usage: moa show [-h] [-v] [--profile] [-u] [-a] [-p]

Show parameters known to this job.

The command outputs three columns, parameter name, flag and
value. The two flags have the following meaning:

* Origin: (l) locally defined; (`d`) default value; (`r`) recursively
  defined; (`s`) system defined; (`x`) extra value, not in the
  template; and (`.`) not defined.

* Private: a `p` indicates this variable to be private.

* Mandatory: a lower case `o` indicates this to be an optional
  variable and `M` means mandatory.

optional arguments:
  -h, --help     show this help message and exit
  -v, --verbose  Show debugging output (default: False)
  --profile      Run the profiler (default: False)
  -u             show unrendered values (default: False)
  -a             show all parameters (default: False)
  -p             show private parameters (default: False)

~~~~~~~~~~~~~~~~~~


.. _command_moa_showblog:

moa **showblog**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

~~~~~~~~~~~~~~~~~~
usage: moa showblog [-h] [-v] [--profile] [no_entries]

Print a changelog to stdout

positional arguments:
  no_entries     No of blog entries to show (default 10) (default: 10)

optional arguments:
  -h, --help     show this help message and exit
  -v, --verbose  Show debugging output (default: False)
  --profile      Run the profiler (default: False)

~~~~~~~~~~~~~~~~~~


.. _command_moa_simple:

moa **simple**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

~~~~~~~~~~~~~~~~~~
usage: moa simple [-h] [-v] [--profile] [-f] [-t TITLE]

Create a 'simple' adhoc job.

Simple meaning that no in or output files are tracked. Moa will
query you for a command to execute (the `process` parameter). Note
that Moa tracks a history for all 'process' parameters used.

optional arguments:
  -h, --help            show this help message and exit
  -v, --verbose         Show debugging output (default: False)
  --profile             Run the profiler (default: False)
  -f, --force           Force this action (default: False)
  -t TITLE, --title TITLE
                        A title for this job (default: None)

~~~~~~~~~~~~~~~~~~


.. _command_moa_simple!:

moa **simple!**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

~~~~~~~~~~~~~~~~~~
usage: moa simple! [-h] [-v] [--profile] [-f] [-t TITLE]

Create a 'simple' adhoc job. 

This command is exactly the same as `moa simple` except for the
fact that Moa uses the bash history specific for the moa job or,
if absent, the user bash history. This is convenient if you would
like to register or reuse a command that you have alreayd
executed.

optional arguments:
  -h, --help            show this help message and exit
  -v, --verbose         Show debugging output (default: False)
  --profile             Run the profiler (default: False)
  -f, --force           Force this action (default: False)
  -t TITLE, --title TITLE
                        A title for this job (default: None)

~~~~~~~~~~~~~~~~~~


.. _command_moa_status:

moa **status**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

~~~~~~~~~~~~~~~~~~
usage: moa status [-h] [-v] [--profile] [-u] [-R] [-p] [-a]

Show job status

Print a short status of the job, including configuration

optional arguments:
  -h, --help     show this help message and exit
  -v, --verbose  Show debugging output (default: False)
  --profile      Run the profiler (default: False)
  -u             show unrendered values (when using inline parameters) (default: False)
  -R             show recursively defined parameters not specified by the local template (default: False)
  -p             show private parameters (default: False)
  -a             show all parameters (default: False)

~~~~~~~~~~~~~~~~~~


.. _command_moa_template:

moa **template**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

~~~~~~~~~~~~~~~~~~
usage: moa template [-h] [-v] [--profile]

**moa template** - Print the template name of the current job

Usage::

    moa template

optional arguments:
  -h, --help     show this help message and exit
  -v, --verbose  Show debugging output (default: False)
  --profile      Run the profiler (default: False)

~~~~~~~~~~~~~~~~~~


.. _command_moa_test:

moa **test**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

~~~~~~~~~~~~~~~~~~
usage: moa test [-h] [-v] [--profile]

Test the job parameters

optional arguments:
  -h, --help     show this help message and exit
  -v, --verbose  Show debugging output (default: False)
  --profile      Run the profiler (default: False)

~~~~~~~~~~~~~~~~~~


.. _command_moa_tree:

moa **tree**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

~~~~~~~~~~~~~~~~~~
usage: moa tree [-h] [-v] [--profile] [-a] [filter]

Show a directory tree and job status

positional arguments:
  filter         show only directories that match this filter (default: None)

optional arguments:
  -h, --help     show this help message and exit
  -v, --verbose  Show debugging output (default: False)
  --profile      Run the profiler (default: False)
  -a, --all

~~~~~~~~~~~~~~~~~~


.. _command_moa_unlock:

moa **unlock**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

~~~~~~~~~~~~~~~~~~
usage: moa unlock [-h] [-v] [--profile]

Unlock a job - allow execution

optional arguments:
  -h, --help     show this help message and exit
  -v, --verbose  Show debugging output (default: False)
  --profile      Run the profiler (default: False)

~~~~~~~~~~~~~~~~~~


.. _command_moa_unset:

moa **unset**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

~~~~~~~~~~~~~~~~~~
usage: moa unset [-h] [-v] [--profile] parameter [parameter ...]

Remove a parameter from the configuration

Remove a configured parameter from this job. In the parameter was
defined by the job template, it reverts back to the default
value. If it was an ad-hoc parameter, it is lost from the
configuration.

positional arguments:
  parameter      parameter to unset

optional arguments:
  -h, --help     show this help message and exit
  -v, --verbose  Show debugging output (default: False)
  --profile      Run the profiler (default: False)

~~~~~~~~~~~~~~~~~~


.. _command_moa_version:

moa **version**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

~~~~~~~~~~~~~~~~~~
usage: moa version [-h] [-v] [--profile]

print moa version number

optional arguments:
  -h, --help     show this help message and exit
  -v, --verbose  Show debugging output (default: False)
  --profile      Run the profiler (default: False)

~~~~~~~~~~~~~~~~~~


msp
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

moa set process

Usage::
    
    msp    

this is an alias for the often used::

     moa set process
