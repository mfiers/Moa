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
maintarget: check mummer

################################################################################
# Variable checks & definition & help
moa_id = clustalw

#targets

#variables

include $(MOABASE)/lib/gnumake/core.mk
ix = $(input_extension)
input_files_a = $(addprefix a__,$(wildcard $(input_dir_a)/*.$(input_extension)))
input_files_b = $(wildcard $(input_dir_b)/*.$(input_extension))

.PHONY: clustalw_prepare
clustalw_prepare:

.PHONY: clustalw_post
clustalw_post:

.PHONY: clustalw
clustalw: $(input_files_a)

$(input_files_a): a__%: $(input_files_b)
	for against in $?; do \
		$(call echo, clustalling $* against $$against) ;\
	done

clean: clustalw_clean

clustalw_clean:
	-rm *delta *coords *fplot *gp *png *rplot *cluster \
		*.hplot *.ps *.pdf
