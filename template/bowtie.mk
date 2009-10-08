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
bowtie_db_help = Bowtie db
bowtie_db_default_attrib = bowtiedb

moa_must_define += bowtie_input_dir
bowtie_input_dir_help = input dir with the query files
bowtie_input_dir_default_attrib = pwd
moa_may_define += bowtie_input_extension
bowtie_input_extension_help = Extension of the input files, \
  defaults to fastq

moa_may_define += bowtie_input_format
bowtie_input_format_help = Format of the input files, defaults \
  to fastq

moa_may_define += bowtie_extra_params
bowtie_extra_params_help = extra parameters to feed bowtie

moa_may_define += bowtie_paired_ends
bowtie_paired_ends_help = perform a paired end analysis. If so, the	\
input files are expected to be of the form							\
 '\*_1.$(bowtie_input_extension)' and 								\
'\*_2.$(bowtie_input_extension)'

moa_may_define += bowtie_output_name
bowtie_output_name_help = output file name, defaults to 'output'

moa_may_define += bowtie_insertsize
bowtie_insertsize_help = Expected insertsize

moa_may_define += bowtie_insertsize_sed
bowtie_insertsize_sed_help += A sed expression that filters the insert size	\
from the input file name. Ignored if bowtie_insertsize is defined.s

moa_may_define += bowtie_insertsize_min bowtie_insertsize_max
bowtie_insertsize_min_help = multiplier determining the minimal		\
acceptable value for two paired reads to be apart. If the			\
bowtie_insertsize is 10000 and this parameter is set at 0.8, than	\
reads that are closer together than 8000 nt are rejected
bowtie_insertsize_max_help += as bowtie_insert_min, but setting a max	\
insert size


ifndef dont_include_moabase
	include $(shell echo $$MOABASE)/template/moaBase.mk
endif

##### Derived variables for this run


bowtie_input_extension ?= fastq
bowtie_input_format ?= fastq
bowtie_output_name ?= output

bowtie_paired_ends ?= F

moa_register_extra += bowtie_output
moa_register_bowtie_output = $(shell echo `pwd`)/$(bowtie_output_name)

ifeq ($(bowtie_input_format),fastq)
bowtie_input_format_param = -q
endif
ifeq ($(bowtie_input_format),fasta)
bowtie_input_format_param = -f
endif
ifndef bowtie_input_format_param
$(error Invalid input format)
endif

ifeq ($(bowtie_paired_ends),T) 
bowtie_input_files = $(wildcard $(bowtie_input_dir)/*_1.$(bowtie_input_extension))
bowtie_output_files = $(addprefix p_,\
		$(patsubst %_1.$(bowtie_input_extension), %, $(notdir $(bowtie_input_files))))
else
bowtie_input_files = $(wildcard $(bowtie_input_dir)/*.$(bowtie_input_extension))
bowtie_output_files = $(addprefix u_,\
	$(patsubst %.$(bowtie_input_extension), %, $(notdir $(bowtie_input_files))))
endif

# -u 30 --solexa1.3-quals 
# 
.PHONY: bowtie_prepare
bowtie_prepare:

.PHONY: bowtie_post
bowtie_post: 

test:
	@echo "INPUT"
	@for x in $(bowtie_input_files); do echo $$x; done
	@echo "OUTPUT"
	@for x in $(bowtie_output_files); do echo $$x; done

comma:=,
.PHONY: bowtie
bowtie: $(bowtie_output_files)
	@echo Processed $(bowtie_output_files)


u_%: $(bowtie_input_dir)/%.$(bowtie_input_extension)
	echo bowtie $(bowtie_input_format_param) \
		$(bowtie_extra_params) $(bowtie_db) $< $@

imn=$(bowtie_insertsize_min)
imx=$(bowtie_insertsize_max)
p_%: $(bowtie_input_dir)/%_1.$(bowtie_input_extension) $(bowtie_input_dir)/%_2.$(bowtie_input_extension)
	@IS="$(bowtie_insertsize)";\
		sizeDef="";\
		[ "$$IS" ] || IS=`echo "$*" | sed "$(bowtie_insertsize_sed)"`;\
		[ "$$IS" ] && sizeDef=`python -c "print \"-I %d -X %d\" % ($$IS * $(imn), $$IS*$(imx))"`;\
		$(call echo, Executing bowtie for $<);\
		bowtie $(bowtie_input_format_param) \
			$(bowtie_extra_params) $$sizeDef $(bowtie_db) \
			 -1 $(word 1,$^) -2 $(word 2,$^) $@

bowtie_clean:
	-rm -f $(bowtie_output_name)


