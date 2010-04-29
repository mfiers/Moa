
The adhoc template is used to execute simple commands (typically a
oneliner) on a set of input files. Input files are defined using the
`adhoc_input_*`, parameters. Each of the input files is then processed
by the command specified in `adhoc_process`. The path to input file is
available to the `adhoc_process` commandline using the `$<`
variable. The output file is available using `$t`. The default output
file name is the basename of the input file. It is possible, however,
to change the output filename using a `sed` expression (in parameters
`adhoc_name_sed`. 
