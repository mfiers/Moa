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

moa_ids += newbler
moa_title_newbler = Newbler
moa_description_newbler = Run a simple, out of the box, newbler					\
assembly

#variables
$(call moa_fileset_define,newbler_input,sff,input SFF files)

################################################################################
## Include MOABASE
include $(MOABASE)/template/moaBase.mk
################################################################################

.PHONY: newbler_prepare
newbler_prepare:

.PHONY: newbler_post
newbler_post:

.PHONY: newbler
newbler: 454AllContigs.fna 454LargeContigs.all.png 

#454AllContigs.fna is one of the files generated
454AllContigs.fna:
	runAssembly -ace -o . -consed $(newbler_input_files)

454LargeContigs.all.png:
	fastaInfo -i 454LargeContigs.fna length gcfrac -b 20 -s > 454LargeContigs.stats
	fastaInfo -i 454AllContigs.fna length gcfrac -b 20 -s > 454AllContigs.stats

newbler_clean:
	$e -rm -rf 454* sff/

