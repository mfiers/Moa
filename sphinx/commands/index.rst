Command reference
=================

moa **!**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Assign the last issued command to "process" parameter


Usage::
  
  moa !



**Description:**

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




moa **archive**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Archive a job, 




**Description:**

Archive a job, or tree with jobs for later execution.

This command stores only those files that are necessary for
execution of this job, that is: templates & configuration. In &
output files, and any other file are ignored. An exception to this
are all files that start with 'moa.'

Usage::

    moa archive

or::

    moa archive [NAME]

an archive name can be omitted when the command is issued in a
directory with a moa job, in which case the name is derived from
the `jobid` parameter

It is possible to run this command recursively with the `-r`
parameter - in which case all (moa job containing) subdirectories
are included in the archive.

As an alternative application you can specify the
`--template`. 





moa **blog**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

record a short note


Usage::
  
  moa blog



**Description:**

Allows a user to enter a short note that is appended to
moa.description (including a timestamp). Use it as follows::

    $ moa blog
    Here you can enter a short, conscise, multi-
    line message describing what you have been
    doing
    [ctrl-d]

Note: the ctrl-d needs to be given on an empty line. The text is
appended to moa.desciption. In the web interface this is converted
to Markdown_.

.. _Markdown: http://daringfireball.net/projects/markdown/ markdown.




moa **cp**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Copy a moa job




**Description:**

Copy a moa job, or a tree with jobs.

moa cp copies only those files defining a job: the template files
and the job configuration. Additionaly, all files in the moa
directory that start with `moa.` (for example `moa.description`
are copied as well. Data and log files are not copied!

The command has two modes of operation. The first is::

    moa cp 10.from 20.to

copies the moa job in 10.from to a newly created 20.to
directory. If the `20.to` directory already exists, a new
directory is created in `20.to/10.from`. As an shortcut one can
use::

    moa cp 10.from 20

in which case the job will be copied to the `20.from` directory.

If the source (`10.from`) directory is not a Moa job, the command
exits with an error.

The second mode of operation is recursive copying::

   moa cp -r 10.from 20.to

in which case all subdirectories under 10.from are traversed and
copied - if a directory contains a Moa job. 

::TODO..  Warn for changing file & dir links




moa **err**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Returns stderr of the last moa run






moa **files**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Show an overview of the files for this job




**Description:**

**moa files** - Display discovered & inferred files for this job

Usage::

   moa files

Display a list of all files discovered (for input & prerequisite
type filesets) and inferred from these for map type filesets.





moa **gitadd**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Add the current job to the git repository




**Description:**

Add a job to the git repository




moa **gitlog**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

display a nicely formatted git log




**Description:**

Print a log to screen




moa **gittag**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Tag the current version






moa **help**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Display help for a template






moa **kill**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Kill a job




**Description:**

See if a job is running, if so - kill it




moa **list**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Print a list of all known templates




**Description:**

**moa list** - Print a list of all known templates

Usage::

    moa list
    moa list -l

Print a list of all templates known to this moa installation. If
the option '-l' is used, a short description for each tempalte is
printed as well.




moa **lock**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Lock this job - prevent execution






moa **log**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Show the logs for this job




**Description:**

**moa lcog** - show a log of the most recent moa calls

Usage::

    moa log [LINES]

Shows a log of moa commands executed. Only commands with an impact
on the pipeline are logged, such as `moa run` & `moa set`. The
number of log entries to display can be controlled with the
optional LINES parameter.    




moa **map**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Create a "map" adhoc analysis


Usage::
  
  moa map -t "title" -- echo "do something"



**Description:**

Anything after `--` will be stored in the `process` variable. If
`--` is omitted, Moa will query the user.

Moa will also query the user for input & output files. An example
session::

    $ moa map -t 'test map'
    process:
    > echo 'processing {{ input }} {{ output }}'
    input:
    > ../10.input/*.txt
    output:
    > ./*.out

Assuming you have a number of `*.txt` files in the `../10/input/`
directory, you will see, upon running::

   processing ../10.input/test.01.txt ./test.01.out
   processing ../10.input/test.02.txt ./test.02.out
   processing ../10.input/test.03.txt ./test.03.out
   ...

If the output file exists, and is newer than the input file, the
process will not be executed for that specific pair. If you need
the job to be repeated, you should either delete the output files
or `touch` the input files.




moa **mv**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Rename/renumber/move a job




**Description:**

Renumber or rename a moa job..




moa **new**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Create a new Moa job




**Description:**

**moa new**

Usage::

    moa new TEMPLATE_NAME -t 'a descriptive title'
    




moa **out**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Returns stdout of the last moa run






moa **pause**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Pause a job




**Description:**

pause a running job




moa **postcommand**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Run the postcommand


Usage::
  
  moa postcommand



**Description:**

Execute the `postcommand`




moa **precommand**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Run the precommand


Usage::
  
  moa pprecommand



**Description:**

Execute the `precommand`




moa **reduce**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Create a "reduce" adhoc analysis


Usage::
  
  moa reduce -t "title" -- echo "do something"



**Description:**

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





moa **refresh**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Reload the template




**Description:**

Refresh the template - i.e. reload the template from the central
repository.




moa **resume**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Resume a job




**Description:**

pause a running job




moa **set**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Set, change or remove variables


Usage::
  
  moa set [KEY] [KEY=VALUE]



**Description:**

This command can be used in a number of ways::

    moa set PARAMETER_NAME=PARAMETER_VALUE
    moa set PARAMETER_NAME='PARAMETER VALUE WITH SPACES'
    moa set PARAMETER_NAME

In the first two forms, moa sets the parameter `PARAMETER_NAME` to
the `PARAMETER_VALUE`. In the latter form, Moa will present the
user with a prompt to enter a value. Note that the first two forms
the full command lines will be processed by bash, which can either
create complications or prove very useful. Take care to escape
variables that you do not want to be expandend and use single quotes
where you can. 




moa **show**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Show configuration


Usage::
  
  moa show



**Description:**

Show all parameters know to this job. Parameters in **bold** are
specifically configured for this job (as opposed to those
parameters that are set to their default value). Parameters in red
are not configured, but need to be for the template to
operate. Parameters in blue are not configured either, but are
optional.




moa **simple**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Create a "simple" adhoc analysis


Usage::
  
  moa simple -t "title" -- echo "do something"



**Description:**

Create a 'simple' adhoc job. Simple meaning that no in or output
files are tracked.

There are a number of ways this command can be used::

    moa simple -t 'a title' -- echo 'define a command'
    
Anything after `--` will be the executable command. Note that bash
will attempt to process the command line. A safer method is::

    moa simple -t 'a title'

Moa will query you for a command to execute (the parameter
`process`).




moa **status**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Show the state of the current job




**Description:**

**moa status** - print out a status status message

Usage::

   moa status       




moa **test**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Test the currennt configuration






moa **tree**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

display a directory tree






moa **unittest**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Run Moa unittests






moa **unlock**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Unlock this job






moa **unset**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Remove a variable


Usage::
  
  moa unset KEY



**Description:**

Remove a configured parameter from this job. In the parameter was
defined by the job template, it reverts back to the default
value. If it was an ad-hoc parameter, it is lost from the
configuration.




moa **version**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Print the moa version




**Description:**

**moa version** - Print the moa version number




msp
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

moa set process

Usage::
    
    msp    

this is an alias for the often used::

     moa set process
