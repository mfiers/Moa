getorf
------------------------------------------------

**Getorf**

::
    Predicts open reading frames using the EMBOSS [[emboss]] getorf tool.


Commands
~~~~~~~~

**clean**
  Remove all job data, not the Moa job itself, note that this must be implemented by the template.


**run**
  *no help defined*





Filesets
~~~~~~~~




**gff**::
    {}

  | *type*: `map`
  | *source*: `input`
  | *category*: `output`
  | *optional*: `{}`
  | *extension*: `{}`
  | *glob*: `{}`
  | *dir*: `{}`







**input**::
    Input files for getorf

  | *type*: `map`
  | *source*: `{}`
  | *category*: `input`
  | *optional*: `False`
  | *extension*: `{}`
  | *glob*: `{}`
  | *dir*: `{}`







**output**::
    {}

  | *type*: `map`
  | *source*: `input`
  | *category*: `output`
  | *optional*: `{}`
  | *extension*: `{}`
  | *glob*: `{}`
  | *dir*: `{}`






Parameters
~~~~~~~~~~



**circular**::
    Is the sequence linear?

  | *type*: `set`
  | *default*: `N`
  | *optional*: `True`



**default_command**::
    command to run for this template

  | *type*: `{}`
  | *default*: `run`
  | *optional*: `True`



**find**::
    What to output? 0: Translation between stop codons, 1: Translation between start & stop codon, 2: Nucleotide sequence between stop codons; 3: Nucleotide sequence between start and stop codons. Default: 3

  | *type*: `set`
  | *default*: `3`
  | *optional*: `True`



**gff_source**::
    source field to use in the gff.

  | *type*: `string`
  | *default*: `getorf`
  | *optional*: `True`



**maxsize**::
    maximal nucleotide size of the predicted ORF.

  | *type*: `integer`
  | *default*: `1000000`
  | *optional*: `True`



**minsize**::
    minimal nucleotide size of the predicted ORF.

  | *type*: `integer`
  | *default*: `30`
  | *optional*: `True`



**table**::
    Genetic code to use: 0 Standard; 1 Standard with alternative initiation codons; 2 Vertebrate Mitochondrial; 3 Yeast Mitochondrial; 4 Mold, Protozoan, Coelenterate Mitochondrial and Mycoplasma/Spiroplasma; 5 Invertebrate Mitochondrial; 6 Ciliate Macronuclear and Dasycladacean; 9 Echinoderm Mitochondrial; 10 Euplotid Nuclear; 11 Bacterial; 12 Alternative Yeast Nuclear; 13 Ascidian Mitochondrial; 14 Flatworm Mitochondrial; 15 Blepharisma Macronuclear; 16 Chlorophycean Mitochondrial; 21 Trematode Mitochondrial; 22 Scenedesmus obliquus; 23 Thraustochytrium Mitochondrial.

  | *type*: `set`
  | *default*: `11`
  | *optional*: `True`



**title**::
    A name for this job

  | *type*: `string`
  | *default*: ``
  | *optional*: `True`



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



