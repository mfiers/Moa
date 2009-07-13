# lftp a set of files

################################################################################
# Definitions
# targets that the enduser might want to use
moa_targets += fasta2gff
fasta2gff_help = generate gff from a fasta file

# Help
moa_ids += fasta2gff
moa_title_fasta2gff = Fasta to gff
moa_description_fasta2gff = Create gff from a fasta file to accompany upload to \
  a gbrowse db

# Output definition
moa_outputs += fasta2gff
moa_output_fasta2gff = ./gff/*
moa_output_fasta2gff_help = gff output files

#varables that NEED to be defined
moa_must_define += f2g_gffsource
f2g_gffsource_help = Source to be used in the gff

#varables that MAY  be defined
moa_may_define += f2g_input_dir 
f2g_input_dir_help = Directory with the input fasta (default: ./fasta)

moa_may_define += f2g_input_extension
f2g_input_extension_help = glob pattern of the fasta files (default: *.fasta) 

moa_may_define += f2g_options
f2g_options_help = options to be passed to the fasta2gff script 

#Include base moa code - does variable checks & generates help
ifndef dont_include_moabase
	include $(shell echo $$MOABASE)/template/moaBase.mk
endif

################################################################################

f2g_options ?=
f2g_input_dir ?= ./fasta
f2g_input_extension ?= fasta
f2g_input_files = $(wildcard $(f2g_input_dir)/*.$(f2g_input_extension))
f2g_output_files = \
    $(addprefix ./gff/, \
        $(patsubst %.fasta, %.gff, \
            $(notdir $(f2g_input_files) )\
        )\
     )

.PHONY: prep concat fasta2gff fasta2gff_run fasta2gff_prep

.PHONY: fasta2gff_prepare
fasta2gff_prepare:
	-mkdir gff

#rerun make, make sure all files are recognized
.PHONY: fasta2gff
fasta2gff: 
	$(MAKE) fasta2gff2

.PHONY: fasta2gff2
fasta2gff2: $(f2g_output_files)
	@echo fasta2gff2 - done

$(f2g_output_files): gff/%.gff : $(f2g_input_dir)/%.$(f2g_input_extension)
	fasta2gff $< -s $(f2g_gffsource) $(f2g_options) > $@

.PHONY: fasta2gff_post
fasta2gff_post: 

.PHONY: fasta2gff_clean
fasta2gff_clean:
	-rm -rf gff	