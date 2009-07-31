# Build a Gmap database

################################################################################
# Variable checks & definition & help
moa_ids += gmapdb
moa_title_gmapdb = gmapdb index builder
moa_description_gmapdb = Builds gmapdb index from a reference	\
  sequence

#variables
moa_must_define += gmapdb_input_dir
gmapdb_input_dir_help = The reference sequence to build a	\
  gmap database with.
gmapdb_input_dir_cdbattr = fastadir

moa_may_define += gmapdb_input_extension
gmapdb_input_extension_help = Extension of the input files, \
  defaults to 'fasta'

moa_must_define += gmapdb_name
gmapdb_name_help = Name of the gmap index to create

ifndef dont_include_moabase
	include $(shell echo $$MOABASE)/template/moaBase.mk
endif

##### Derived variables for this run
moa_register_extra += gmapdb
moa_register_gmapdb = $(shell echo `pwd`)/$(gmapdb_name)

gmapdb_input_extension ?= fasta

gmapdb_input_files = $(wildcard $(gmapdb_input_dir)/*.$(gmapdb_input_extension))

.PHONY: gmapdb_prepare
gmapdb_prepare:

.PHONY: gmapdb_post
gmapdb_post:

.PHONY: gmapdb
gmapdb: Makefile.$(gmapdb_name)
	$(MAKE) -f $< coords
	$(MAKE) -f $< gmapdb

Makefile.$(gmapdb_name):
	gmap_setup -S -d $(gmapdb_name) $(gmapdb_input_files)

comma:=,
#one of the database files
$(gmapdb_name).1.ebwt: $(gmapdb_input_files)
	gmap-build $(call merge,$(comma),$^) $(gmapdb_name)

gmapdb_clean:
	rm -f $(gmapdb_name).*
	rm -f coords.$(gmapdb_name)
	rm -f Makefile.$(gmapdb_name)
	rm -f INSTALL*



