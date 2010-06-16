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

################################################################################
#include moabasepre
include $(MOABASE)/template/moa/prepare.mk

moa_id = bowtie
template_title = Bowtie
template_description = Run BOWTIE on an set of input files (query) \
  vs a database index.

#variables
moa_must_define += bowtie_db
bowtie_db_help = The bowtie database to use. It is allowed to define one of \
  the bowtie database files (.[0-9].ebwt).
bowtie_db_type = file

$(call moa_fileset_define,bowtie_input,fastq,Input files for bowtie)

moa_may_define += bowtie_input_format
bowtie_input_format_default = fastq
bowtie_input_format_help = Format of the input files
bowtie_input_format_type = set
bowtie_input_format_allowed = fastq fasta

moa_may_define += bowtie_extra_params
bowtie_extra_params_default = 
bowtie_extra_params_help = extra parameters to feed bowtie
bowtie_extra_params_type = string

moa_may_define += bowtie_paired_ends
bowtie_paired_ends_default = F
bowtie_paired_ends_help = perform a paired end analysis. If so, the	\
  input files are expected to be of the form							\
  '\*$(bowtie_forward_suffix).$(bowtie_input_extension)' and			\
'  \*$(bowtie_reverse_suffix).$(bowtie_input_extension)'
bowtie_paired_ends_type = set
bowtie_paired_ends_allowed = T F

moa_may_define += bowtie_forward_suffix
bowtie_forward_suffix_default = _1
bowtie_forward_suffix_help = Last part of the sequence name identifying a file with forward reads
bowtie_forward_suffix_type = string

moa_may_define += bowtie_reverse_suffix
bowtie_reverse_suffix_default = _2
bowtie_reverse_suffix_help = Last part of the sequence name identifying a file with reverse reads
bowtie_reverse_suffix_type = string

moa_may_define += bowtie_msi
bowtie_msi_help = Merge, sort and index? If *T* use samtools to merge	\
 all bamfiles into one, sort them and create an index
bowtie_msi_type = set
bowtie_msi_default = F
bowtie_msi_allowed = T F

moa_may_define += bowtie_basename
bowtie_basename_help = basename for generating the merged, sorted and indexed files
bowtie_basename_type = string
bowtie_basename_default = all

moa_may_define += bowtie_output_format
bowtie_output_format_default = bam
bowtie_output_format_help = Format of the output file
bowtie_output_format_type = set

bowtie_output_format_allowed = bowtie bam sam

moa_may_define += bowtie_insertsize
bowtie_insertsize_default = 5000
bowtie_insertsize_help = Expected insertsize
bowtie_insertsize_type = float

moa_may_define += bowtie_insertsize_sed
bowtie_insertsize_sed_default = 
bowtie_insertsize_sed_help = SED expression to filter the expected	\
insertsize from the input file name
bowtie_insertsize_sed_type = string

moa_may_define += bowtie_insertsize_min
bowtie_insertsize_min_default = 0.1
bowtie_insertsize_min_help = multiplier determining the minimal		\
acceptable value for two paired reads to be apart. If the			\
bowtie_insertsize is 10000 and this parameter is set at 0.8, than	\
reads that are closer together than 8000 nt are rejecte
bowtie_insertsize_min_type = float

moa_may_define += bowtie_insertsize_max
bowtie_insertsize_max_default = 10
bowtie_insertsize_max_help = Max insertsize for a paired alignment
bowtie_insertsize_max_type = float

#########################################################################
# Prerequisite testing
moa_prereq_simple += samtools bowtie

include $(shell echo $$MOABASE)/template/moa/core.mk

##### Derived variables for this run

#shortcuts
bfn = $(bowtie_forward_suffix)
brn = $(bowtie_reverse_suffix)

ifeq ($(bowtie_input_format),fastq)
bowtie_input_format_param=-q
endif

ifeq ($(bowtie_input_format),fasta)
bowtie_input_format_param=-f
endif

ifeq ($(bowtie_output_format),bam)
bowtie_output_convert=| samtools view -bS - 
bowtie_output_format_param = -S
endif
ifeq ($(bowtie_output_format),sam)
bowtie_output_convert
bowtie_output_format_param = -S
endif

ifeq ($(bowtie_output_format),bowtie)
$(warning, set output format to default bowtie)
bowtie_output_convert = 
endif

ifeq ($(bowtie_paired_ends),T) 
bowtie_input_files = $(wildcard $(bowtie_input_dir)/$(bowtie_input_glob)$(bfn).$(bowtie_input_extension))
bowtie_output_files = $(addprefix pair_, $(addsuffix .$(bowtie_output_format),\
		$(patsubst %$(bfn).$(bowtie_input_extension), %, $(notdir $(bowtie_input_files)))))
else
bowtie_input_files = $(wildcard $(bowtie_input_dir)/$(bowtie_input_glob).$(bowtie_input_extension))
bowtie_output_files = $(addprefix unpaired_,$(addsuffix .$(bowtie_output_format),\
		$(patsubst %.$(bowtie_input_extension), %, $(notdir $(bowtie_input_files)))))
endif

.PHONY: bowtie_prepare
bowtie_prepare:

.PHONY: bowtie_post
bowtie_post: 

test: test_input $(addprefix check_exists_, $(bowtie_output_files))

t:
	@echo "INPUT"
	@for x in $(bowtie_input_files); do echo input $$x; done
	@echo "OUTPUT"
	@for x in $(bowtie_output_files); do echo output $$x; done

check_exists_%:
	$e if [[ -f '*x' ]]; then echo -n "* "; fi
	$e echo $*

comma:=,
.PHONY: bowtie
bowtie: $(bowtie_output_files) bowtie_msi

bowtie_msi: $(if $(call seq,$(bowtie_msi),T),$(bowtie_basename).sorted.bam.bai)

$(bowtie_basename).sorted.bam.bai: $(bowtie_basename).sorted.bam
	$(call warn,Start indexing)
	samtools index $<

$(bowtie_basename).sorted.bam: $(bowtie_basename).merged.bam
	$(call warn,Start sorting)
	samtools sort $< $(bowtie_basename).sorted

$(bowtie_basename).merged.bam: $(bowtie_output_files)
	if [[ $(words $^) > 1 ]]; then \
		$(call warn,Start merging) ;\
		samtools merge $@ $^ ;\
	else \
		$(call echo,Only one bam file - linking) ;\
		ln $^ $@ -s ;\
	fi

imn=$(bowtie_insertsize_min)
imx=$(bowtie_insertsize_max)
bis=$(bowtie_insertsize_sed)
pair_%.$(bowtie_output_format): \
		$(bowtie_input_dir)/%$(bfn).$(bowtie_input_extension) \
		$(bowtie_input_dir)/%$(brn).$(bowtie_input_extension)
	$e IS="$(bowtie_insertsize)";\
		sizeDef="";\
		[[ ! "$$IS" && "$(bis)" ]] && IS=`echo "$*" | sed "$(bis)"`;\
		[[ "$$IS" ]] && sizeDef=`python -c "print \"-I %d -X %d\" % ($$IS * $(imn), $$IS*$(imx))"`;\
		$(call echo, Executing bowtie for $<);\
		bowtie $(bowtie_input_format_param) \
				$(bowtie_output_format_param) \
				$(bowtie_extra_params) \
				$$sizeDef \
				$(bowtie_db) \
				-1 $(word 1,$^) \
				-2 $(word 2,$^) \
				$(bowtie_output_convert) \
				> $@

unpaired_%.$(bowtie_output_format): $(bowtie_input_dir)/%.$(bowtie_input_extension)
	@echo "hi $<"
	@echo "bowtie $(bowtie_input_format_param) $(bowtie_output_format_param) $(bowtie_extra_params) $(bowtie_db) $< $(bowtie_output_convert)"
	bowtie $(bowtie_input_format_param) $(bowtie_extra_params) $(bowtie_output_format_param) $(bowtie_db) $< $(bowtie_output_convert) > $@

bowtie_clean:
	-rm -f $(bowtie_output_files)


