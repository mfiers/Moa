
Command reference (+private)
============================

Includes private commands - private commands are for internal use
only.

moa **!**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Moa-fy the last (bash) command issued


Usage::
  
  moa !



**Description:**

Set the 'process' parameter to the last issued command. If no moa
job exists, create a 'simple'job.




*Usage of this command will be logged*



moa **adhoc**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Create an adhoc analysis


Usage::
  
  moa adhoc -t "title" -- echo "do something"



**Description:**

Creates an adhoc job.




*Usage of this command will be logged*



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




*Usage of this command will be logged*



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




*Usage of this command will be logged*



moa **err**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Returns stderr of the last moa run






*Usage of this command will **NOT** be logged*



moa **files**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Show an overview of the files for this job




**Description:**

**moa files** - Display discovered & inferred files for this job

Usage::

   moa files

Display a list of all files discovered (for input & prerequisite
type filesets) and inferred from these for map type filesets.





*Usage of this command will be logged*



moa **help**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Display help for a template






*Usage of this command will be logged*



moa **history**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

display a version control log




**Description:**

Print a log to screen




*Usage of this command will be logged*



moa **kill**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Kill a currently running job




**Description:**

See if a job is running, if so - kill it




*Usage of this command will be logged*



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




*Usage of this command will be logged*



moa **lock**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Lock this job - prevent execution






*Usage of this command will be logged*



moa **log**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Show the logs for this job




**Description:**

**moa log** - show a log of the most recent moa calls

Usage::

    moa log [LINES]

Shows a log of moa commands executed. Only commands with an impact
on the pipeline are logged, such as `moa run` & `moa set`. The
number of log entries to display can be controlled with the
optional LINES parameter.    




*Usage of this command will **NOT** be logged*



moa **map**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Create a "map" adhoc analysis


Usage::
  
  moa map -t "title" -- echo "do something"



**Description:**

Create a 'map' adhoc job.

There are a number of ways this command can be used::

    $ moa map -t 'a title' -- echo 'define a command'

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





*Usage of this command will be logged*



moa **new**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Create a new Moa job




**Description:**

**moa new**

Usage::

    moa new TEMPLATE_NAME -t 'a descriptive title'
    




*Usage of this command will be logged*



moa **out**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Returns stdout of the last moa run






*Usage of this command will **NOT** be logged*



moa **pack**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

pack a job or pipeline, or manage packs




**Description:**

Create an adhoc job




*Usage of this command will be logged*



moa **raw_commands**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

{}




**Description:**

*(private)* **moa raw_commands** - Print a list of all known commands

Usage::

    moa raw_commands

Print a list of known Moa commands, both global, plugin defined
commands as template specified ones. This command is mainly used
by software interacting with Moa.




*Usage of this command will **NOT** be logged*



moa **raw_parameters**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

{}




**Description:**

*(private)* **moa raw_parameters** - Print out a list of all known parameters

Usage::

    moa raw_parameters
    
print a list of all defined or known parameters




*Usage of this command will **NOT** be logged*



moa **refresh**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Reload the template






*Usage of this command will be logged*



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




*Usage of this command will be logged*



moa **show**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Show configured variables


Usage::
  
  moa show



**Description:**

Show all parameters know to this job. Parameters in **bold** are
specifically configured for this job (as opposed to those
parameters that are set to their default value). Parameters in red
are not configured, but need to be for the template to
operate. Parameters in blue are not configured either, but are
optional.




*Usage of this command will **NOT** be logged*



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




*Usage of this command will be logged*



moa **status**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Show the state of the current job




**Description:**

**moa status** - print out a short status status message

Usage::

   moa status       




*Usage of this command will **NOT** be logged*



moa **tag**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Tag the current version






*Usage of this command will be logged*



moa **template**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Display the template name




**Description:**

**moa template** - Print the template name of the current job

Usage::

    moa template

    




*Usage of this command will be logged*



moa **template_dump**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Display the raw template description




**Description:**

**moa template_dump** - Show raw template information

Usage::

   moa template_dump [TEMPLATE_NAME]

Show the raw template data.




*Usage of this command will be logged*



moa **template_set**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Set a template parameters




**Description:**

**moa template_set** - set a template parameter.

This only works for top level template parameters




*Usage of this command will be logged*



moa **test**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Test the currennt configuration






*Usage of this command will be logged*



moa **tree**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

display a directory tree






*Usage of this command will **NOT** be logged*



moa **unittest**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Run Moa unittests






*Usage of this command will be logged*



moa **unlock**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Unlock this job






*Usage of this command will be logged*



moa **unpack**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

unpack an earlier packed job/pipeline






*Usage of this command will be logged*



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




*Usage of this command will be logged*



moa **version**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Print the moa version




**Description:**

**moa version** - Print the moa version number




*Usage of this command will **NOT** be logged*



moa **welcome**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Display a welcome text




**Description:**

print a welcome message




*Usage of this command will be logged*



