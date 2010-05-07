The adhoc template is used to execute simple, one-line, commands, on a
set of input files. This template can run in four different modes:

* *seq* (default): Run the command sequentially on a set of input
files
* *par*: Run the command in parallel on the input files, to be used
together with the `-j NOTHREADS` parameter.  
* *all*: Run the command once on all input files (use `$^`)
* *simple*: Run the command without any input files

Input files are defined using the `adhoc_input_*`, parameters. The
command can be defined by setting `adhoc_process`. Note that commands
must be enclosed by single quotes (') to make sure that bash
interprets it as a single command and does not try to expand
variables. Another important thing to note is that if you would like
to use dollar signs (for example for environment variables) you need
to escape these with an extra `$` (so, `$$HOME` would refer to the
user home directory)

## seq, par

Both the `seq` and `par` modes process the each of the input files
seperatly by the command specified in `adhoc_process`. The path to
input file is available to the `adhoc_process` commandline through the
`$<` variable. The output file name is available using `$t`. 

The default output file name is the basename of the input file. It is
possible, however, to change the output filename using a `sed`
expression (`adhoc_name_sed`).

## all

All inputfiles are fed to the commandline at once. The list of input
files is available as `$^`.

## examples

A simple example is to create a link in the current directory to the
input files. This can be done by setting adhoc to the `par` mode and
setting`'adhoc_process` to `ln $< $t`.
    
A more complex example would be to extract the headers from a set of
input sequences and filter them for a keyword ("mitochon") and store
the IDs of hitting sequences into a single output file. This must be
run in the `seq` modus to prevent several threads writing to the
output files at the same time.

    head -1 $< | cut -c2- | grep -i mitochon \
        | cut -d' ' -f 1 >> hits

To configure moa to use this command, you must enclose the command in
single quotes (bash will try to expand variables inbetween double
quotes):

    moa set adhoc_process='head -1 $< | cut -c2- \
        | grep -i mitochon | cut -d" " -f 1 >> hits'

The `$t` parameter is not used here. It is not obligatory to do so.

The results are all concatentated together (`>>`)into a single `hits`
file. The `adhoc` template tracks which input files have been
processed (using a zero length file in the `./touch` directory). Upon
reexecuting moa only those files that are new or have changed since
the last run are executed. If you are sure that no input files will
change, then this jobs should operate fine. If you are not sure, or if
you would like to generate fresh results upon a rerun, it is wiser to
remove the output file before running:

    moa set moa_precommand='rm hits || true'
    moa set adhoctouch=F
    
The first parameter is executed at the start of each moa run and
deletes the hits file. The `|| true` makes sure that it does not exit
with an error, (for example if there is no `hits` file to delete),
since that would halt the execution of Moa. The latter parameter stops
Moa from using touch files to track if input files have changed.

