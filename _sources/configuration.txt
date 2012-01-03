Configuring Moa
===============

Moa is configured using the command line tool `Moa`. For example, you
are creating a simple job somewhere::

    $ moa simple -t 'test job' -- echo "Hello"

and you would like to change the title, you can do this with `moa
set`::

    $ moa set title='I mean: Hello!!'

When setting parameters on the command line you need to consider the
fact that bash might try to expand or interpret the command line. For
example, if you would like to set the process parameter to `echo "it's
complicated"`, you would need the following command line::

    $ moa set process='echo "it'\'' complicated"'

only to be able to use a single quote. Similar care needs to be taken
with, for example, the `$` character, as that will be expanded by
bash, unless placed between single quotes or properly escaped. An
alternative way of setting variables would be by running::

     $ moa set process

which will prompt you for the value of `process`, without tyring to
expand any variables. 

It is at all times possible to check what the current configuration is
by running::

    $ moa show

which will give you (possibly with more color)::

    postcommand  o (undefined)
    precommand   o (undefined)
    process      L echo "it's complicated"
    project      o (undefined)
    title        L I mean: Hello!!

The first column has the parameter name, followed by a single letter,
and the value of the parameter, or `(undefined)` if no value is
specified. The letters in the second column signify the state of the
parameter:

* **o**: Undefined, but **O**\ ptional.
* **L**: Locally defined
* **R**: **R**\ ecursively defined
* **E**: **E**\ rror - undefined and not optional.


