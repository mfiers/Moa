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
moa_ids += dotself
moa_title_mummer = Dottup self
moa_description_mummer = Run dottup with a sequence against itself

#targets
dotself_help = run clustalw

#variables
moa_must_define += dotself_input_dir
dotself_input_dir_help = Set of sequences to use
dotself_input_dir_type = directory

moa_may_define += dotself_input_extension
dotself_input_extension_default = fasta
dotself_input_extension_help = Extension of input files
dotself_input_extension_type = string

moa_may_define += dotself_wordsize
dotself_wordsize_default = 6
dotself_wordsize_help = Wordsize used for recognizing similarity
dotself_wordsize_type = integer

include $(MOABASE)/template/moaBase.mk

ix = $(dotself_input_extension)

dotself_input_files = $(addprefix a__,\
	$(wildcard $(dotself_input_dir)/*.$(ix)))

dotself_output_files = $(addprefix png/,\
	$(patsubst %.$(ix),%.png,$(notdir $(dotself_input_files))))

.PHONY: test
test:
	@echo $(dotself_input_files)
	@echo $(dotself_output_files)

.PHONY: dotself_prepare
dotself_prepare:
	-mkdir png

.PHONY: dotself_post
dotself_post: 

.PHONY: dotself
dotself: $(dotself_output_files)

$(dotself_output_files): png/%.png: $(dotself_input_dir)/%.$(dotself_input_extension)
	@$(call echo, running dottup for $*);
	dottup -asequence $< -bsequence $< -wordsize $(dotself_wordsize) \
			-graph png -goutfile $@ -gtitle "$*";

PHONY: dotself_clean
dotself_clean:
	rm -f png
