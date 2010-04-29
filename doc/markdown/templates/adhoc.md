
The adhoc template is used to execute simple commands (typically a
oneliner) on a set of input files. Input files are defined using the
`adhoc_input_*`, parameters. Each of the input files is then processed
by the command specified in `adhoc_process`. The path to input file is
available to the `adhoc_process` commandline using the `$<`
variable. The output file is available using `$t`. The default output
file name is the basename of the input file. It is possible, however,
to change the output filename using a `sed` expression (in parameters
`adhoc_name_sed`. 

The default operation is to (hard) link all files to the current
directory using the following command:

    ln $< $t
    
Another, more complex example, is to extract the headers from a set of
input sequences and filter them for a keyword ("mitochon") and store
the IDs of hitting sequences into a single output file.

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

