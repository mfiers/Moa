**NOTE: both the software and the manual are under development. Expect things to change.**

How to write a template
=======================

A MOA template is made up of a ``.moa file`` and a ``.jinja2`` (or ``.mk``) file.

The ``.moa`` file mainly contains input-output file sets and parameter options used for
the bash command(s). Some of these options have default values which the user can change while 
constructing the job.  

The ``.jinja2`` file includes information to structure the command(s). It is written in `jinja <http://jinja.pocoo.org>`_,
which is a templating language for python and is simple to write and easy to understand.

These files are used by the backend, currently *ruffus*, that manages file set and parameter dependencies
to make pipelines and render commands to the bash prompt. Initially, *GNU make* was the backend used. It is 
very powerful but some of its limitations and its complexity led to including *ruffus* as an option for
the backend as well.

The easiest way to write a moa template is to edit an existing template
to suit your requirements. This involves understanding the parts of an 
existing template. 

The ``bwa_aln`` template is used as an example below. Just as a background, 
the *bwa aln* command takes a FASTQ file as input and aligns it to a reference genome that 
was previously indexed. The output is a .sai file with the alignments. 

The ``bwa_aln.moa`` file has some main components:

-  *Backend*

   ::

      backend: ruff

   This is 'ruff' which means that `ruffus <http://www.ruffus.org.uk/>`_ 
   is used in the python script at a lower level to read the template .moa and .jinja2 file,
   and render the corresponding commands to the bash prompt.
-  *Commands*

   ::
   
      commands:
        run:
          mode: map
          help:  run bwa aln
        clean:
          mode: simple
          help: Remove all job data, not the Moa job itself, note that this must be implemented by the template.

   This indicates the function names that you will later define. In the example above, 
   there are 2 commands- run and clean, so ``moa run`` or ``moa clean`` on the
   command prompt in the job directory would execute these functions.
-  *Filesets*

   ::
      
      filesets:
        input:
          category: input
          extension: fq
          help: Fastq input files
          glob: '*'
          optional: false
          type: set
        output:
          category: output
          dir: .
          extension: sai
          glob: '{{ input_glob }}'
          source: input
          type: map

   Like the name, each filesets refer to a set of files in a single directory. 
   The bwa_aln template shows 2 filesets: ``input`` and ``output``.

   -  *Category*: is essentially used to separate input from output.
   -  *Extension*: refers to the type of file(s) required or generated.
   -  *Glob*: searches for files with a specified pattern.
      Moa, by default (glob= \*) automatically processes all files of the specified input
      extension in the directory specified. By specifying a glob, Moa will only process
      those files whose name pattern matches what is in the glob.
	  
   -  *Type*:  refers to the data type of the fileset or parameter. 
      
      A fileset can either be of ``set`` or ``map`` type.
      The type ``set`` refers to a simple set of files in a directory. 
      The type ``map`` refers to a set of files that are linked to what their ``source`` 
      value is. In the above code, the output fileset is mapped to the input fileset.
	  
   -  *Dir*: the directory of the output fileset is '.', which means that the output files will
      be placed in the current working directory.

-  *Parameter category order* 

   ::
   
      parameter_category_order:
        - ''
        - input
        - system
        - advanced
	  
-  *Parameters* 

   ::
   
      mismatch_penalty:
        category: ''
        default: 3
        help: mismatch penalty
        optional: true
        type: integer

   They are the variables/options that specify a command.

   -  *Category*: 
   -  *Default*: is the value that is used by default if not changed by the user.
   -  *Optional*: specifies if it is necessary for the user to fill in a value for the variable. 
      If ``optional`` is false, the user has to indicate a value for the parameter in order to execute
      the job.
   -  *Type*: specifies the data type of the variable eg. integer, string, boolean.

-  *Moa_id*

   ::
      
	  moa_id: bwa_aln
      
   is supposed to be the same as the filename. Ideally something descriptive (eg. bwa_aln).
   This is used to later link to the other template file.
   
The other template file is ''bwa_aln.jinja2'' which is written in `jinja <http://jinja.pocoo.org>`_, 
a templating language for python. 
*Note that the jinja2 file name is the same as the moa file name.*

Important features of the bwa_aln.jinja2 file are:

-  The three hash's (###) specify the start of a function and are followed by the function name.
   In our bwa_aln example, we have defined 2 funtions: ``run`` and ``clean``.
   
   ::
   
      ### run
   
-  This defination is followed by a set of commands which you would want to be executed when you type
   ``moa run`` or ``moa_clean`` in the bwa_aln job directory.
   The commands in our example file look the same as what you would put in the command prompt but the 
   values of the parameters are bought from the .moa file and hence it's value is replaced by the
   parameter name.
   
   ::
      
	  bwa aln {{db}} 			     \
	      -n {{edit_dist_missing_prob}}          \
	      . 				     \
	      . 				     \
	      .  				     \
	      {{ input }}			     \
	      -f {{ output}}
	  
-  It is also possible to add if-else statements or other computing blocks in accordance with the design
   language.
   ::
      
	  {% if color_space %} -c {% endif %}	    

