# 
# Copyright 2009 Mark Fiers, Plant & Food Research
# 
# This file is part of Moa - http://github.com/mfiers/Moa
# 
# Moa is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your
# option) any later version.
# 
# Moa is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
# or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public
# License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with Moa.  If not, see <http://www.gnu.org/licenses/>.
# 

include $(shell echo $$MOABASE)/template/moa/prepare.mk

moa_id = newbler
moa_title_newbler = Newbler
moa_description_newbler = Run a simple, out of the box, newbler		\
assembly.															\
																	\
As an extra feature, this template automatically creates uniquely	\
named links to the two main output fasta files (454AllContigs.fna,	\
454LargeContigs.fna). This is convenient for subsequence 'gather'	\
steps. The links are named after the directory. 

#variables
$(call moa_fileset_define,newbler_input,sff,input SFF files)

moa_may_define += newbler_library_name
newbler_library_name_type = string
newbler_library_name_default = $(shell echo `basename $(CURDIR)` | sed "s/[ \///\/]//g" )
newbler_library_name_help = A library identifier for this				\
assembly. This is used to create an extra fasta file, named using this	\
variable, that contain the generated contigs with their ids prepended	\
with the library id.

moa_may_define += newbler_mids
newbler_mids_help = mids to use for this assembly
newbler_mids_type = string
newbler_mids_default = 

moa_may_define += newbler_mid_configuration
newbler_mid_configuration_help = Mid configuration file to use
newbler_mid_configuration_type = file
newbler_mid_configuration_default = 

moa_may_define += newbler_min_identity
newbler_min_identity_help = Minimal overalp identity used during assembly 
newbler_min_identity_type = integer
newbler_min_identity_default = 

moa_may_define += newbler_largecontig_cutoff
newbler_largecontig_cutoff_help = min length of a contig in 454LargeContigs.fna
newbler_largecontig_cutoff_type = integer
newbler_largecontig_cutoff_default = 


################################################################################
## Include MOABASE
include $(MOABASE)/template/moa/core.mk
################################################################################

.PHONY: newbler_prepare
newbler_prepare:

.PHONY: newbler_post

nln = $(newbler_library_name)
newbler_post:
	cat 454AllContigs.fna | sed 's/>contig/>$(nln)_contig/' > $(nln).all.fasta 
	cat 454LargeContigs.fna | sed 's/>contig/>$(nln)_contig/' > $(nln).large.fasta 

.PHONY: newbler
newbler: 454AllContigs.fna 454LargeContigs.all.png 

newbler_cl = runAssembly -ace -o . -consed \
		$(if $(newbler_mid_configuration),-mcf $(newbler_mid_configuration)) \
		$(if $(newbler_min_identity), -mi $(newbler_min_identity)) \
		$(if $(newbler_largecontig_cutoff), -l $(newbler_largecontig_cutoff)) \
		$(if $(newbler_mids), \
				$(addprefix $(newbler_mids)@, $(newbler_input_files)),\
				$(newbler_input_files))

#454AllContigs.fna is one of the files generated
454AllContigs.fna:
	echo "Executing"
	echo $(newbler_cl)
	$(newbler_cl)

454LargeContigs.all.png:
	fastaInfo -i 454LargeContigs.fna length gcfrac -b 20 -s > 454LargeContigs.stats
	fastaInfo -i 454AllContigs.fna length gcfrac -b 20 -s > 454AllContigs.stats

newbler_clean:
	$e -rm -rf 454* sff/

