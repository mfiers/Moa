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

#Include base moa code - does variable checks & generates help
include $(MOABASE)/lib/gnumake/prepare.mk
################################################################################
# Definitions
# targets that the enduser might want to use
moa_targets += clean_fasta

# Help
moa_id = clean_fasta

# Output definition
moa_outputs += clean_fasta
moa_output_clean_fasta = ./fasta/*.fasta

#varables that NEED to be defined

#Include base moa code - does variable checks & generates help
include $(MOABASE)/lib/gnumake/core.mk
################################################################################

cf_output_files = $(wildcard $(cf_input_dir)/*.$(cf_input_extension))

.phony: clean_fasta_prepare
clean_fasta_prepare:
	-mkdir fasta

.PHONY: clean_fasta
clean_fasta: 
	$(MAKE) clean_fasta_run

clean_fasta_run: $(addprefix cfs_, $(notdir $(cf_output_files)))
	@echo $(cf_output_files)
	#@echo $(cf_input_dir)/*.$(cf_input_extension)
	touch clean_fasta_run

cfs_%:
	cat $(cf_input_dir)/$* | sed '$(sed_command)' > $(cf_input_dir)/$*.tmp
	mv $(cf_input_dir)/$*.tmp $(cf_input_dir)/$*

.PHONY: clean_fasta_clean
clean_fasta_clean:
