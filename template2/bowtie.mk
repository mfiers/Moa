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
include $(MOABASE)/lib/gnumake/prepare.mk
moa_id = bowtie

#variables

$(call moa_fileset_define,bowtie_input,fastq,Input files for bowtie)

#########################################################################
# Prerequisite testing

include $(MOABASE)/lib/gnumake/core.mk
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

