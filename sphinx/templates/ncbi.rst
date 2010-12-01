ncbi
------------------------------------------------

**Download data from NCBI**

::
    Download a set of sequences from NCBI based on a query string *ncbi_query* and database *ncbi_db*. This tempate will run only **once**, after a succesful run it creates a lock file that you need to remove to rerun


Commands
~~~~~~~~

**clean**
  Remove all job data, not the Moa job itself, note that this must be implemented by the template.


**run**
  Start downloading





Parameters
~~~~~~~~~~



**db**::
    NCBI database

  | *type*: `string`
  | *default*: `nuccore`
  | *optional*: `True`



**query**::
    NCBI query (for example txid9397[Organism%3Aexp])

  | *type*: `string`
  | *default*: ``
  | *optional*: `True`



**sequence_name**::
    Name of the file to write the downloaded sequences to.

  | *type*: `string`
  | *default*: `out`
  | *optional*: `True`



**title**::
    A name for this job

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



