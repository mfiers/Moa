#this is a small adaptation of the blast template, expecting one single input file
#without escaping the following line would have read:
blast_input_dir = $(shell x=$(blast_input_file); echo $${x%/*})
#without escaping the following line would have read:
## blast_input_ext = $(shell export x=$(blast_input_file); echo ${x##*.} )
blast_input_ext = $(shell x=$(blast_input_file); echo $${x\#\#*.} )

moa_must_define += blast_input_file
blast_input_file_help = Input fasta file to BLAST
blast_input_files = $(blast_input_file)

include $(shell echo $$MOABASE)/template/blast.mk
