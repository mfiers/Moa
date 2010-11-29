blast
------------------------------------------------

**Basic Local Alignment Tool** - Wraps BLAST [[Alt90]], probably the most popular similarity search tool in bioinformatics.

Commands
~~~~~~~~

**blast_report**
  Generate a text BLAST report.

**clean**
  Remove all job data, not the Moa job itself, note that this must be implemented by the template.

**run**
  Running BLAST takes an input directory (*blast_input_dir*), determines what sequence files are present (with the parameter *blast_input_extension*) and executes BLAST on each of these. Moa BLAST is configured to create XML output (as opposed to the standard text based output) in the *./out* directory. The output XML is subsequently converted to GFF3 by the custom *blast2gff* script (using BioPython). Additionally, a simple text report is created.



Backend 
  gnumake
Author
  Mark Fiers
Creation date
  Wed Nov 10 07:56:48 2010
Modification date
  Wed Nov 10 07:56:48 2010



