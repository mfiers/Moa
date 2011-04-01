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

include $(MOABASE)/lib/gnumake/prepare.mk
moa_id = newbler

#variables

################################################################################
## Include MOABASE
include $(MOABASE)/lib/gnumake/core.mk################################################################################

.PHONY: newbler_prepare
newbler_prepare:

.PHONY: newbler_post

nln = $(newbler_library_name)
newbler_post:
	cat 454AllContigs.fna | sed 's/>contig/>$(nln)_contig/' > $(nln).all.fasta 
	cat 454LargeContigs.fna | sed 's/>contig/>$(nln)_contig/' > $(nln).large.fasta

.PHONY: newbler
newbler: 454AllContigs.fna 454LargeContigs.all.png

#454LargeContigs.all.png

newbler_cl = runAssembly -ace -o . \
		$(if $(newbler_mid_configuration),-mcf $(newbler_mid_configuration)) 	\
		$(if $(newbler_min_identity), -mi $(newbler_min_identity)) 		\
		$(if $(newbler_largecontig_cutoff), -l $(newbler_largecontig_cutoff)) 	\
		$(if $(newbler_mids), 							\
			$(addprefix $(newbler_mids)@, $(newbler_input_files)),		\
			$(newbler_input_files))

#454AllContigs.fna is one of the files generated
454AllContigs.fna:
	echo "Executing"
	echo "Input files $(newbler_input_files)"
	echo $(newbler_cl)
	$(newbler_cl)

454LargeContigs.all.png:
	fastaInfo -i 454LargeContigs.fna length gcfrac -b 20 -s > 454LargeContigs.stats
	fastaInfo -i 454AllContigs.fna length gcfrac -b 20 -s > 454AllContigs.stats

newbler_clean:
	$e -rm -rf 454* sff/

