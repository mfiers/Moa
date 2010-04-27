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
moa_main_target: check concatenate weka_set

################################################################################
# Definitions
# targets that the enduser might want to use

# Help
moa_id = concatenate
template_title = Concatenate
template_description = Concatenate a set of fasta files into one.

# Output definition
moa_outputs += concatenate
moa_output_concatenate = ./outputfile.fasta
moa_output_concatenate_help = The concatenated file

#varables that NEED to be defined
moa_must_define += input_dir
input_dir_help = Directory with the input data
input_dir_type = directory

moa_must_define += name
name_help = name of the file, the outputfile will become ./name.fasta
name_type = string

moa_may_define += input_extension
input_extension_default = fasta
input_extension_help = extension to the fasta files (default .fasta)
input_extension_type = string

#Include base moa code - does variable checks & generates help
ifndef dont_include_moabase
	include $(shell echo $$MOABASE)/template/moa/core.mk
endif

################################################################################

input_files = $(wildcard $(input_dir)/*.$(input_extension))
output_file = $(name).fasta

.PHONY: prep concat concatenate concatenate_run

concatenate: concatenate_run

concatenate_run: $(output_file)

$(output_file):  $(input_files) 
	-rm $(output_file)
	cat $(input_files) > $(output_file)	
	@echo "end of concatenation"

#CLEAN	        
clean: concatenate_clean
concatenate_clean:
	-rm $(name).fasta	