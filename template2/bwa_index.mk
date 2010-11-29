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
moa_id=bwa_index
include $(MOABASE)/lib/gnumake/prepare.mk
include $(MOABASE)/lib/gnumake/core.mk

$(bwa_index_name).ann: %.ann : $(bwa_index_input_fasta)

	echo bwa index -p $(bwa_index_prefix) 			\
			  -a $(bwa_index_algorithm)     		\
			  $(if $(bwa_aln_color_space), -c) 		\
			  $(bwa_index_input_fasta)
	
	# ln $< $(bwa_index_name).fasta
	#bwa index $(bwa_index_name).fasta

bwa_index: $(bwa_index_name).ann

bwa_index_clean:
	-rm -f $(bwa_index_name).*

