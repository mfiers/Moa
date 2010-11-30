fq2bq
------------------------------------------------

**Convert FASTQ to BFQ** - Converts a FASTQ file to MAQ BFQ format.

Commands
~~~~~~~~

**clean**
  Remove all job data, not the Moa job itself, note that this must be implemented by the template.


**run**
  *no help defined*





Filesets
~~~~~~~~




**bfq** - {}

  | *type*: `map`
  | *source*: `input`
  | *category*: `output`
  | *optional*: `{}`
  | *extension*: `bfq`
  | *glob*: `{}`
  | *dir*: `./bfq`







**input** - input FASTA files

  | *type*: `input`
  | *category*: `input`
  | *optional*: `False`
  | *extension*: `fastq`
  | *glob*: `{}`






Parameters
~~~~~~~~~~



**title** - A name for this job
  | *type*: `string`
  | *default*: ``
  | *optional*: `False`



Other
~~~~~

**Backend**
  gnumake
**Author**
  Mark Fiers
**Creation date**
  Wed Nov 10 07:56:48 2010
**Modification date**
  Wed Nov 10 07:56:48 2010



