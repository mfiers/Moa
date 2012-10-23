Command reference
=================

moa **!**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

~~~~~~~~~~~~~~~~~~
usage: moa ! [-h] [-r] [-v] [--profile] [-f] [-t TITLE]

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

optional arguments:
  -h, --help            show this help message and exit
  -r, --recursive       Run this job recursively (default: false)
  -v, --verbose         Show debugging output (default: False)
  --profile             Run the profiler (default: False)
  -f, --force           Force this action (default: False)
  -t TITLE, --title TITLE
                        A title for this job (default: None)

~~~~~~~~~~~~~~~~~~


moa **archive**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

~~~~~~~~~~~~~~~~~~
usage: moa archive [-h] [-r] [-v] [--profile] [-f] [-s] [-t] [name]

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
  name             archive name (default: None)

optional arguments:
  -h, --help       show this help message and exit
  -r, --recursive  Run this job recursively (default: false)
  -v, --verbose    Show debugging output (default: False)
  --profile        Run the profiler (default: False)
  -f, --force      Force this action (default: False)
  -s, --sync       Alternative approach to deal with sync type jobs - only include _ref directories (default: False)
  -t, --template   Store this archive as a template (default: False)

~~~~~~~~~~~~~~~~~~


moa **archive_excl**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

~~~~~~~~~~~~~~~~~~
usage: moa archive_excl [-h] [-r] [-v] [--profile]

Toggle a directory to be included in an moa archive.

optional arguments:
  -h, --help       show this help message and exit
  -r, --recursive  Run this job recursively (default: false)
  -v, --verbose    Show debugging output (default: False)
  --profile        Run the profiler (default: False)

~~~~~~~~~~~~~~~~~~


moa **archive_incl**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

~~~~~~~~~~~~~~~~~~
usage: moa archive_incl [-h] [-r] [-v] [--profile]

Toggle a directory to be included in an moa archive.

optional arguments:
  -h, --help       show this help message and exit
  -r, --recursive  Run this job recursively (default: false)
  -v, --verbose    Show debugging output (default: False)
  --profile        Run the profiler (default: False)

~~~~~~~~~~~~~~~~~~


moa **blog**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

~~~~~~~~~~~~~~~~~~
usage: moa blog [-h] [-r] [-v] [--profile] [message [message ...]]

Add an entry to the job blog (BLOG.md)

Allows a user to maintain a blog for this job (in BLOG.md). Use as
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
  -h, --help       show this help message and exit
  -r, --recursive  Run this job recursively (default: false)
  -v, --verbose    Show debugging output (default: False)
  --profile        Run the profiler (default: False)

~~~~~~~~~~~~~~~~~~


moa **change**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

~~~~~~~~~~~~~~~~~~
usage: moa change [-h] [-r] [-v] [--profile] [message [message ...]]

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
  -h, --help       show this help message and exit
  -r, --recursive  Run this job recursively (default: false)
  -v, --verbose    Show debugging output (default: False)
  --profile        Run the profiler (default: False)

~~~~~~~~~~~~~~~~~~


moa **cp**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

~~~~~~~~~~~~~~~~~~
usage: moa cp [-h] [-r] [-v] [--profile] [-o] from [to]

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
  -r, --recursive  Run this job recursively (default: false)
  -v, --verbose    Show debugging output (default: False)
  --profile        Run the profiler (default: False)
  -o, --overwrite  if the target dir exists - overwrite (instead of copying into that dir (default: False)

~~~~~~~~~~~~~~~~~~


moa **dumpTemplate**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

~~~~~~~~~~~~~~~~~~
usage: moa dumpTemplate [-h] [-r] [-v] [--profile]

**moa template_dump** - Show raw template information

Usage::

   moa template_dump [TEMPLATE_NAME]

Show the raw template sysConf.

optional arguments:
  -h, --help       show this help message and exit
  -r, --recursive  Run this job recursively (default: false)
  -v, --verbose    Show debugging output (default: False)
  --profile        Run the profiler (default: False)

~~~~~~~~~~~~~~~~~~


moa **err**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

~~~~~~~~~~~~~~~~~~
usage: moa err [-h] [-r] [-v] [--profile]

Show the stderr of the most recently executed moa job

optional arguments:
  -h, --help       show this help message and exit
  -r, --recursive  Run this job recursively (default: false)
  -v, --verbose    Show debugging output (default: False)
  --profile        Run the profiler (default: False)

~~~~~~~~~~~~~~~~~~


moa **files**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

~~~~~~~~~~~~~~~~~~
usage: moa files [-h] [-r] [-v] [--profile] [-a] [-n NO_FILES]

Show in and output files for this job

Display a list of all files discovered (for input & prerequisite
type filesets) and inferred from these for map type filesets.

optional arguments:
  -h, --help            show this help message and exit
  -r, --recursive       Run this job recursively (default: false)
  -v, --verbose         Show debugging output (default: False)
  --profile             Run the profiler (default: False)
  -a, --all             Show all filesets (default: False)
  -n NO_FILES, --no_files NO_FILES
                        No filesets to show (default 10) (default: 10)

~~~~~~~~~~~~~~~~~~


moa **gitadd**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

~~~~~~~~~~~~~~~~~~
usage: moa gitadd [-h] [-r] [-v] [--profile]

add this job to a git repository

optional arguments:
  -h, --help       show this help message and exit
  -r, --recursive  Run this job recursively (default: false)
  -v, --verbose    Show debugging output (default: False)
  --profile        Run the profiler (default: False)

~~~~~~~~~~~~~~~~~~


moa **gitlog**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

~~~~~~~~~~~~~~~~~~
usage: moa gitlog [-h] [-r] [-v] [--profile]

Print a log to screen

optional arguments:
  -h, --help       show this help message and exit
  -r, --recursive  Run this job recursively (default: false)
  -v, --verbose    Show debugging output (default: False)
  --profile        Run the profiler (default: False)

~~~~~~~~~~~~~~~~~~


moa **kill**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

~~~~~~~~~~~~~~~~~~
usage: moa kill [-h] [-r] [-v] [--profile]

Kill a running job.

This command checks if a job is running. If so - it tries to kill
it by sending SIGKILL (-9) to the job.

optional arguments:
  -h, --help       show this help message and exit
  -r, --recursive  Run this job recursively (default: false)
  -v, --verbose    Show debugging output (default: False)
  --profile        Run the profiler (default: False)

~~~~~~~~~~~~~~~~~~


moa **list**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

~~~~~~~~~~~~~~~~~~
usage: moa list [-h] [-r] [-v] [--profile] [-d]

Lists all known templates

Print a list of all templates known to this moa installation. This
includes locally installed templates as well.

optional arguments:
  -h, --help       show this help message and exit
  -r, --recursive  Run this job recursively (default: false)
  -v, --verbose    Show debugging output (default: False)
  --profile        Run the profiler (default: False)
  -d               Print a short template description (default: False)

~~~~~~~~~~~~~~~~~~


moa **lock**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

~~~~~~~~~~~~~~~~~~
usage: moa lock [-h] [-r] [-v] [--profile]

Lock a job - prevent execution

optional arguments:
  -h, --help       show this help message and exit
  -r, --recursive  Run this job recursively (default: false)
  -v, --verbose    Show debugging output (default: False)
  --profile        Run the profiler (default: False)

~~~~~~~~~~~~~~~~~~


moa **log**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

~~~~~~~~~~~~~~~~~~
usage: moa log [-h] [-r] [-v] [--profile]

Show activity log

Shows a log of moa commands executed. Only commands with an impact
on the pipeline are logged, such as `moa run` & `moa set`.

optional arguments:
  -h, --help       show this help message and exit
  -r, --recursive  Run this job recursively (default: false)
  -v, --verbose    Show debugging output (default: False)
  --profile        Run the profiler (default: False)

~~~~~~~~~~~~~~~~~~


moa **map**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

~~~~~~~~~~~~~~~~~~
usage: moa map [-h] [-r] [-v] [--profile] [-f] [-t TITLE]

create an adhoc moa 'map' job

Moa will query the user for process, input & output files. An
example session

optional arguments:
  -h, --help            show this help message and exit
  -r, --recursive       Run this job recursively (default: false)
  -v, --verbose         Show debugging output (default: False)
  --profile             Run the profiler (default: False)
  -f, --force           Force this action (default: False)
  -t TITLE, --title TITLE
                        A title for this job (default: None)

~~~~~~~~~~~~~~~~~~


moa **mv**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

~~~~~~~~~~~~~~~~~~
usage: moa mv [-h] [-r] [-v] [--profile] from [to]

Move, rename or renumber a moa job.

positional arguments:
  from             copy from
  to               copy to (default: None)

optional arguments:
  -h, --help       show this help message and exit
  -r, --recursive  Run this job recursively (default: false)
  -v, --verbose    Show debugging output (default: False)
  --profile        Run the profiler (default: False)

~~~~~~~~~~~~~~~~~~


moa **new**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

~~~~~~~~~~~~~~~~~~
usage: moa new [-h] [-r] [-v] [--profile] [-f] [-t TITLE]
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
  -r, --recursive       Run this job recursively (default: false)
  -v, --verbose         Show debugging output (default: False)
  --profile             Run the profiler (default: False)
  -f, --force           Force this action (default: False)
  -t TITLE, --title TITLE
                        mandatory job title (default: )

~~~~~~~~~~~~~~~~~~


moa **out**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

~~~~~~~~~~~~~~~~~~
usage: moa out [-h] [-r] [-v] [--profile]

Show the stdout of the most recently executed moa job

optional arguments:
  -h, --help       show this help message and exit
  -r, --recursive  Run this job recursively (default: false)
  -v, --verbose    Show debugging output (default: False)
  --profile        Run the profiler (default: False)

~~~~~~~~~~~~~~~~~~


moa **pause**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

~~~~~~~~~~~~~~~~~~
usage: moa pause [-h] [-r] [-v] [--profile]

Pause a running job

optional arguments:
  -h, --help       show this help message and exit
  -r, --recursive  Run this job recursively (default: false)
  -v, --verbose    Show debugging output (default: False)
  --profile        Run the profiler (default: False)

~~~~~~~~~~~~~~~~~~


moa **pelican**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

~~~~~~~~~~~~~~~~~~
usage: moa pelican [-h] [-r] [-v] [--profile]

Run pelican :)

optional arguments:
  -h, --help       show this help message and exit
  -r, --recursive  Run this job recursively (default: false)
  -v, --verbose    Show debugging output (default: False)
  --profile        Run the profiler (default: False)

~~~~~~~~~~~~~~~~~~


moa **postcommand**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

~~~~~~~~~~~~~~~~~~
usage: moa postcommand [-h] [-r] [-v] [--profile]

Execute 'postcommand'

optional arguments:
  -h, --help       show this help message and exit
  -r, --recursive  Run this job recursively (default: false)
  -v, --verbose    Show debugging output (default: False)
  --profile        Run the profiler (default: False)

~~~~~~~~~~~~~~~~~~


moa **precommand**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

~~~~~~~~~~~~~~~~~~
usage: moa precommand [-h] [-r] [-v] [--profile]

Execute 'precommand'

optional arguments:
  -h, --help       show this help message and exit
  -r, --recursive  Run this job recursively (default: false)
  -v, --verbose    Show debugging output (default: False)
  --profile        Run the profiler (default: False)

~~~~~~~~~~~~~~~~~~


moa **raw_commands**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

~~~~~~~~~~~~~~~~~~
usage: moa raw_commands [-h] [-r] [-v] [--profile]

return a list available commands

Print a list of known Moa commands, both global, plugin defined
commands as template specified ones. This command meant to be used
by software interacting with Moa.

optional arguments:
  -h, --help       show this help message and exit
  -r, --recursive  Run this job recursively (default: false)
  -v, --verbose    Show debugging output (default: False)
  --profile        Run the profiler (default: False)

~~~~~~~~~~~~~~~~~~


moa **raw_parameters**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

~~~~~~~~~~~~~~~~~~
usage: moa raw_parameters [-h] [-r] [-v] [--profile]

Print a list of all known parameters

optional arguments:
  -h, --help       show this help message and exit
  -r, --recursive  Run this job recursively (default: false)
  -v, --verbose    Show debugging output (default: False)
  --profile        Run the profiler (default: False)

~~~~~~~~~~~~~~~~~~


moa **readme**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

~~~~~~~~~~~~~~~~~~
usage: moa readme [-h] [-r] [-v] [--profile]

Edit the README.md file for this job

You could, obviously, also edit the file yourself - this is a mere
shortcut - maybe it will stimulate you to maintain a README file

optional arguments:
  -h, --help       show this help message and exit
  -r, --recursive  Run this job recursively (default: false)
  -v, --verbose    Show debugging output (default: False)
  --profile        Run the profiler (default: False)

~~~~~~~~~~~~~~~~~~


moa **refresh**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

~~~~~~~~~~~~~~~~~~
usage: moa refresh [-h] [-r] [-v] [--profile]

Refresh the template

Reload the template from the original repository.

optional arguments:
  -h, --help       show this help message and exit
  -r, --recursive  Run this job recursively (default: false)
  -v, --verbose    Show debugging output (default: False)
  --profile        Run the profiler (default: False)

~~~~~~~~~~~~~~~~~~


moa **rehash**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

~~~~~~~~~~~~~~~~~~
usage: moa rehash [-h] [-r] [-v] [--profile]

cache a list of variables for command line completion

optional arguments:
  -h, --help       show this help message and exit
  -r, --recursive  Run this job recursively (default: false)
  -v, --verbose    Show debugging output (default: False)
  --profile        Run the profiler (default: False)

~~~~~~~~~~~~~~~~~~


moa **resume**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

~~~~~~~~~~~~~~~~~~
usage: moa resume [-h] [-r] [-v] [--profile]

Resume a running job

optional arguments:
  -h, --help       show this help message and exit
  -r, --recursive  Run this job recursively (default: false)
  -v, --verbose    Show debugging output (default: False)
  --profile        Run the profiler (default: False)

~~~~~~~~~~~~~~~~~~


moa **set**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

~~~~~~~~~~~~~~~~~~
usage: moa set [-h] [-r] [-v] [--profile] [-f] [-s] parameter [parameter ...]

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

if -s is specified, the variable is stored as a system
configuration variable in the YAML formatted::

~/.config/moa/config

Please, use this with care!

Note that dots in the key name are interpreted as nested levels,
so, running::

      moa set -s plugins.job.completion.enabled=false

will result in the following section added on top of the YAML::

    plugins:
        job:
            completion:
                enabled: false

Adding keys like this mixes safely with configuration information
that is already present. So, if one later sets::

    moa set -s plugins.job.completion.enabled=false

the `enabled: false` heading under `completion:` will not be
removed

positional arguments:
  parameter        arguments for this job, specifyas KEY=VALUE without spaces

optional arguments:
  -h, --help       show this help message and exit
  -r, --recursive  Run this job recursively (default: false)
  -v, --verbose    Show debugging output (default: False)
  --profile        Run the profiler (default: False)
  -f, --force      Force this action (default: False)
  -s, --system     store this a system configuration variable (default: False)

~~~~~~~~~~~~~~~~~~


moa **show**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

~~~~~~~~~~~~~~~~~~
usage: moa show [-h] [-r] [-v] [--profile] [-u] [-R] [-p] [-a]

Show all parameters know to this job.

Parameters in **bold** are specifically configured for this job
(as opposed to those parameters that are set to their default
value). Parameters in red are not configured, but need to be for
the template to operate. Parameters in blue are not configured
either, but are optional.

optional arguments:
  -h, --help       show this help message and exit
  -r, --recursive  Run this job recursively (default: false)
  -v, --verbose    Show debugging output (default: False)
  --profile        Run the profiler (default: False)
  -u               show unrendered values (when using inline parameters) (default: False)
  -R               show recursively defined parameters not specified by the local template (default: False)
  -p               show private parameters (default: False)
  -a               show all parameters (default: False)

~~~~~~~~~~~~~~~~~~


moa **simple**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

~~~~~~~~~~~~~~~~~~
usage: moa simple [-h] [-r] [-v] [--profile] [-f] [-t TITLE]

Create a 'simple' adhoc job.

Simple meaning that no in or output files are tracked. Moa will
query you for a command to execute (the `process` parameter).

optional arguments:
  -h, --help            show this help message and exit
  -r, --recursive       Run this job recursively (default: false)
  -v, --verbose         Show debugging output (default: False)
  --profile             Run the profiler (default: False)
  -f, --force           Force this action (default: False)
  -t TITLE, --title TITLE
                        A title for this job (default: None)

~~~~~~~~~~~~~~~~~~


moa **status**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

~~~~~~~~~~~~~~~~~~
usage: moa status [-h] [-r] [-v] [--profile] [-u] [-R] [-p] [-a]

Show job status

Print a short status of the job, including configuration

optional arguments:
  -h, --help       show this help message and exit
  -r, --recursive  Run this job recursively (default: false)
  -v, --verbose    Show debugging output (default: False)
  --profile        Run the profiler (default: False)
  -u               show unrendered values (when using inline parameters) (default: False)
  -R               show recursively defined parameters not specified by the local template (default: False)
  -p               show private parameters (default: False)
  -a               show all parameters (default: False)

~~~~~~~~~~~~~~~~~~


moa **template**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

~~~~~~~~~~~~~~~~~~
usage: moa template [-h] [-r] [-v] [--profile]

**moa template** - Print the template name of the current job

Usage::

    moa template

optional arguments:
  -h, --help       show this help message and exit
  -r, --recursive  Run this job recursively (default: false)
  -v, --verbose    Show debugging output (default: False)
  --profile        Run the profiler (default: False)

~~~~~~~~~~~~~~~~~~


moa **test**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

~~~~~~~~~~~~~~~~~~
usage: moa test [-h] [-r] [-v] [--profile]

Test the job parameters

optional arguments:
  -h, --help       show this help message and exit
  -r, --recursive  Run this job recursively (default: false)
  -v, --verbose    Show debugging output (default: False)
  --profile        Run the profiler (default: False)

~~~~~~~~~~~~~~~~~~


moa **tree**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

~~~~~~~~~~~~~~~~~~
usage: moa tree [-h] [-r] [-v] [--profile] [-a] [filter]

Show a directory tree and job status

positional arguments:
  filter           show only directories that match this filter (default: None)

optional arguments:
  -h, --help       show this help message and exit
  -r, --recursive  Run this job recursively (default: false)
  -v, --verbose    Show debugging output (default: False)
  --profile        Run the profiler (default: False)
  -a, --all

~~~~~~~~~~~~~~~~~~


moa **unlock**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

~~~~~~~~~~~~~~~~~~
usage: moa unlock [-h] [-r] [-v] [--profile]

Unlock a job - allow execution

optional arguments:
  -h, --help       show this help message and exit
  -r, --recursive  Run this job recursively (default: false)
  -v, --verbose    Show debugging output (default: False)
  --profile        Run the profiler (default: False)

~~~~~~~~~~~~~~~~~~


moa **unset**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

~~~~~~~~~~~~~~~~~~
usage: moa unset [-h] [-r] [-v] [--profile] parameter [parameter ...]

Remove a parameter from the configuration

Remove a configured parameter from this job. In the parameter was
defined by the job template, it reverts back to the default
value. If it was an ad-hoc parameter, it is lost from the
configuration.

positional arguments:
  parameter        parameter to unset

optional arguments:
  -h, --help       show this help message and exit
  -r, --recursive  Run this job recursively (default: false)
  -v, --verbose    Show debugging output (default: False)
  --profile        Run the profiler (default: False)

~~~~~~~~~~~~~~~~~~


moa **version**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

~~~~~~~~~~~~~~~~~~
usage: moa version [-h] [-r] [-v] [--profile]

print moa version number

optional arguments:
  -h, --help       show this help message and exit
  -r, --recursive  Run this job recursively (default: false)
  -v, --verbose    Show debugging output (default: False)
  --profile        Run the profiler (default: False)

~~~~~~~~~~~~~~~~~~


msp
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

moa set process

Usage::
    
    msp    

this is an alias for the often used::

     moa set process
