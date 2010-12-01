**NOTE: both the software and the manual are under development. Expect things to change.**

How to write a template
=======================

A MOA template is made up of a .moa file and a .jinja2 (or .mk file).

The easiest way to write a moa template is to edit an existing template
to suit your requirements. This involves understanding the parts of an 
existing template so let’s use the bwa_aln template as an example.  

The ''bwa_aln.moa'' file has some important components:

-  *Backend*: This is ‘ruff’ which means that `ruffus <http://www.ruffus.org.uk/>`_ 
   is used in the python script at a lower level, but this essentially means that
   ..... (have to write templates in jinja2 or similar script)
-  *Command*: This indicates the function names that you will later define. In our 
   example, there are 2 options- run and clean, so ``moa run`` or ``moa clean`` on the
   command prompt in the job directory would run these functions.
-  Filesets: Like the name, each filesets refer to a set of files in a single directory. 
   The bwa_aln template shows 2 filesets: ``input`` and ``output``.
   
   -  *Category*: is essentially used to separate input from output.
   -  *Extension*: refers to the extension of the set of files that you want to use.
   -  *Glob*:  searches for files with a specified pattern.
      Moa, by default (glob= *) automatically processes all files of the specified input
	  extension in the directory specified. By specifying a glob, Moa will only process
	  those files whose name pattern matches what is in the glob.
   -  *Type*:  refers to the data type of the fileset or parameter. 
      With filesets, the type ``set`` refers to a simple set of files in a directory. 
	  The type ``map`` refers to a set of files that are linked to what their ``source`` 
	  value is. In the case of bwa_aln.moa, the output fileset is mapped to the input fileset.   
   -  *Dir*: the directory of the output fileset is ‘.’, which means that the output files will
      be placed in the current working directory.
	  
-  *Parameter category order*: 
-  *Parameters*: are the variables that specify the limits of a command. 

   -  *Category*: 
   -  *Default*: is the value that is used by default if not changed by the user.
   -  *Optional*: specifies if it is imperative for the user to fill in a value to the variable. 
      If this is false, it means that the user has to put in a value else MOA will show an error.
   -  *Type*: specifies the data type of the variable eg. Integer, string, Boolean
   
-  *Moa_id*: is supposed to be the same as the filename. Ideally something descriptive (eg. bwa_aln).
   This is used to later link to the other template file.
   
The other template file is ''bwa_aln.jinja2'' which is written in `jinja <http://jinja.pocoo.org>`_, 
a templating language for python. 
*Note that the jinja2 file name is the same as the moa file name.*

Important features of the bwa_aln.jinja2 file are:

-  The three hash’s (###) specify the start of a function and are followed by the function name and 
   defination. In our bwa_aln example, we have defined 2 funtions: run and clean.
-  This defination is followed by a set of commands which you would want to be executed when you type
  ``moa run`` or ``moa_clean`` in the bwa_aln job directory.
-  The commands in our example file look the same as what you would put in the command prompt but the 
   values of the parameters are bought from the .moa file and hence it's value is replaced by the
   parameter name.
-  It is also possible to add if-else statements or other computing blocks in accordance with the design
   language.

