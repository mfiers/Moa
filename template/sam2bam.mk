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

include $(shell echo $$MOABASE)/template/moaBasePre.mk

moa_ids += sam2bam
moa_title_maq_fasta2bfa = Convert SAM to BAM using samtools
moa_description_maq_fasta2bfa = Converts a FASTQ file to MAQ BFQ	\
format.

#variables
$(call moa_fileset_define,sam2bam_input,sam,input SAM files)

#########################################################################
# Prerequisite testing

prereqlist += prereq_samtools

prereq_samtools:
	$(call checkPrereqPath, samtools)

################################################################################
## include moabase
include $(shell echo $$MOABASE)/template/moaBase.mk

##### Derived variables for this run
$(call moa_fileset_remap_nodir,sam2bam_input,sam2bam_output,bam)

test:
	@echo 'xx $(HAVE_INCLUDED_MOABASE)'
	@echo $(sam2bam_input_files)
	$e echo
	$e echo
	@echo $(sam2bam_output_files)

.PHONY: sam2bam_prepare
sam2bam_prepare:

.PHONY: sam2bam_post
sam2bam_post:

sam2bam: $(sam2bam_output_files)

%.bam: $(sam2bam_input_dir)/%.$(sam2bam_input_extension)
	samtools view -bS -o $@ $<

sam2bam_clean:
	$e -rm *.bam



