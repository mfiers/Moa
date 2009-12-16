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
moa_ids += bowtie 
moa_title_bowtie = Bowtie
moa_description_bowtie = Run BOWTIE on an set of input files (query) \
  vs a database index.

#variables
moa_must_define += bowtie_db
bowtie_db_help = The bowtie database to use. It is allowed to define	\
one of the bowtie database files (.[0-9].ebwt).
bowtie_db_type = file

moa_must_define += bowtie_input_dir
bowtie_input_dir_help = input dir with the query files
bowtie_input_type = directory

moa_may_define += bowtie_input_extension
bowtie_input_extension_help = Extension of the input files
bowtie_input_extension_type = string
bowtie_input_extension_default = fastq

moa_may_define += bowtie_input_format
bowtie_input_format_help = Format of the input files
bowtie_input_format_default = fastq
bowtie_input_format_type = set
bowtie_input_format_allowed = fastq fasta

moa_may_define += bowtie_extra_params
bowtie_extra_params_help = extra parameters to feed bowtie
bowtie_extra_params_type = string

moa_may_define += bowtie_paired_ends 
bowtie_paired_ends_help = perform a paired end analysis. If so, the	\
input files are expected to be of the form							\
 '\*$(bowtie_forward_suffix).$(bowtie_input_extension)' and			\
'\*$(bowtie_reverse_suffix).$(bowtie_input_extension)'
bowtie_paired_ends_type = set
bowtie_paired_ends_allowed = T F
bowtie_paired_ends_default = F

moa_may_define += bowtie_forward_suffix
bowtie_forward_suffix_help = Last part of the sequence name 			\
identifying a file with forward reads
bowtie_forward_suffix_default=_1
bowtie_forward_suffix_type=string

moa_may_define += bowtie_reverse_suffix
bowtie_reverse_suffix_help = Last part of the sequence name 			\
identifying a file with reverse reads
bowtie_reverse_suffix_default=_2
bowtie_reverse_suffix_type=string

moa_may_define += bowtie_output_format
bowtie_output_format_help = Format of the output file
bowtie_output_format_type = set 
bowtie_output_format_allowed = bowtie bam sam
bowtie_output_format_default = bam

moa_may_define += bowtie_insertsize
bowtie_insertsize_help = Expected insertsize
bowtie_insertsize_type = integer

moa_may_define += bowtie_insertsize_sed
bowtie_insertsize_sed_help += A sed expression that filters the insert	\
size from the input file name. Ignored if bowtie_insertsize is			\
defined.
bowtie_insertsize_sed_type = string


moa_may_define += bowtie_insertsize_min bowtie_insertsize_max
bowtie_insertsize_min_help = multiplier determining the minimal		\
acceptable value for two paired reads to be apart. If the			\
bowtie_insertsize is 10000 and this parameter is set at 0.8, than	\
reads that are closer together than 8000 nt are rejecte
dbowtie_insertsize_min_type = float
bowtie_insertsize_min_default = 0.1

moa_may_define += bowtie_insertsize_max
bowtie_insertsize_max_help += as bowtie_insert_min, but setting a max	\
  insert size
bowtie_insertsize_max_type = float
bowtie_insertsize_max_default = 10

#########################################################################
# Prerequisite testing
moa_prereq_simple += samtools bowtie

include $(shell echo $$MOABASE)/template/moaBase.mk

##### Derived variables for this run

#shortcuts
bfn = $(bowtie_forward_suffix)
brn = $(bowtie_reverse_suffix)

bowtie_paired_ends ?= F

ifeq ($(bowtie_input_format),fastq)
bowtie_input_format_param = -q
endif
ifeq ($(bowtie_input_format),fasta)
bowtie_input_format_param = -f
endif

ifeq ($(bowtie_output_format),bam)
bowtie_output_format_param=-S
bowtie_output_convert=| samtools view -bS - 
endif
ifeq ($(bowtie_output_format),sam)
bowtie_output_format_param=-S
bowtie_output_convert=
endif
ifeq ($(bowtie_output_format),bowtie)
$(warning, set output format to default bowtie)
bowtie_output_format_param =
bowtie_output_convert = 
endif

ifeq ($(bowtie_paired_ends),T) 
bowtie_input_files = $(wildcard $(bowtie_input_dir)/*$(bfn).$(bowtie_input_extension))
bowtie_output_files = $(addprefix pair_, $(addsuffix .$(bowtie_output_format),\
		$(patsubst %$(bfn).$(bowtie_input_extension), %, $(notdir $(bowtie_input_files)))))
else
bowtie_input_files = $(wildcard $(bowtie_input_dir)/*.$(bowtie_input_extension))
bowtie_output_files = $(addprefix single_, $(addsuffix .$(bowtie_output_format),\
		$(patsubst %$(bfn).$(bowtie_input_extension), %, $(notdir $(bowtie_input_files)))))
endif

.PHONY: bowtie_prepare
bowtie_prepare:

.PHONY: bowtie_post
bowtie_post: 

test: test_input $(addprefix check_exists_, $(bowtie_output_files))

test_input:
	@echo "INPUT"
	@for x in $(bowtie_input_files); do echo $$x; done

check_exists_%:
	$e if [[ -f '*x' ]]; then echo -n "* "; fi
	$e echo $*

comma:=,
.PHONY: bowtie
bowtie: $(bowtie_output_files)
	@echo Processed $(bowtie_output_files)


single_%.$(bowtie_output_format): \
		$(bowtie_input_dir)/%.$(bowtie_input_extension)
	echo bowtie $(bowtie_input_format_param) \
		$(bowtie_extra_params) $(bowtie_db) $< $(bowtie_output_convert) > $@ 

imn=$(bowtie_insertsize_min)
imx=$(bowtie_insertsize_max)
bis=$(bowtie_insertsize_sed)
ls -l pair_%.$(bowtie_output_format): \
		$(bowtie_input_dir)/%$(bfn).$(bowtie_input_extension) \
		$(bowtie_input_dir)/%$(brn).$(bowtie_input_extension)
	$e IS="$(bowtie_insertsize)";\
		sizeDef="";\
		[[ ! "$$IS" && "$(bis)" ]] && IS=`echo "$*" | sed "$(bis)"`;\
		[[ "$$IS" ]] && sizeDef=`python -c "print \"-I %d -X %d\" % ($$IS * $(imn), $$IS*$(imx))"`;\
		$(call echo, Executing bowtie for $<);\
		bowtie $(bowtie_input_format_param) $(bowtie_output_format_param) 			\
			$(bowtie_extra_params) $$sizeDef $(bowtie_db) 							\
			 -1 $(word 1,$^) -2 $(word 2,$^) $(bowtie_output_convert) > $@

bowtie_clean:
	-rm -f $(bowtie_output_file)


