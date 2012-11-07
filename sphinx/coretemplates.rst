Three core templates
=====================

Moa comes with a list of templates (see :ref:`templates`). The three
most important, flexible templates of these that allow you to embed
custom code (called `process`) in your project are:

`simple`:

    Simply executes `process` as a bash one-liner

`map`:

    Takes a set of in- and output files and executes the custom
    commands for each in- and output file (using the
    `Jinja2 <http://jinja.pocoo.org/docs/>`_ template language).

`reduce`:

    Takes a set of input files and a single output file and executes
    the custom commands with all input file, generating the output
    files.

Since `simple`, `map` and `reduce` have proven to be quite central to
how Moa operates they come with their own shortcut commands (`moa
simple`, `moa map` and `moa reduce`). These command query the user
directly for the parameters instead of having to define this manually.

For example, a `simple` job::

    $ mkdir simple_test && cd simple_test
    $ moa simple -t 'Generate some files'
    process:
    > for x in `seq 1 5`; do touch test.$x; done
    $ moa run
    $ ls
    test.1  test.2  test.3  test.4  test.5

Note that you can make your `process` as complicated as you
like. Alternatively, you can write a script that you call from
`process`.

A map job would work like this::

    $ mkdir ../map_test && cd ../map_test
    $ moa map -t 'Map some files'
    process:
    > echo {{ input }} ; echo {{ input }} > {{ output }}
    input:
    > ../simple_test/test.*
    output:
    > ./out.*
    $ moa run
    ../simple_test/test.3
    ../simple_test/test.1
    ../simple_test/test.5
    ../simple_test/test.2
    ../simple_test/test.
    Moa: Success executing "run" (<1 sec)
    $ ls
    out.1  out.2  out.3  out.4  out.5
    $ cat out.1
    ../simple_test/test.1

Moa tracks which input file generates which outputfile. So, if you
would like to repeat one of the jobs - you'll need to delete the
output file & rerun `moa`::

    $ rm out.3
    $ moa run
    ../simple_test/test.3
    Moa: Success executing "run" (<1 sec)

And a `reduce` example::


    $ mkdir ../reduce_test && cd ../reduce_test
    $ moa reduce -t 'Reduce some files'
    process:
    > echo {{ input|join(" ") }} >> {{ output }}
    input:
    > ../map_test/out.*
    output:
    > ./reduce_out
    $ moa run
    Moa: Success executing "run" (<1 sec)
    $ ls
    reduce_out
    $ cat reduce_out
    ../map_test/out.1 ../map_test/out.3 ../map_test/out.4 ../map_test/out.5 ../map_test/out.2
