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

blast_input_dir = $(shell x=$(blast_input_file); echo $${x%/*})
#without escaping the following line would have read:
## blast_input_ext = $(shell export x=$(blast_input_file); echo ${x##*.} )
blast_input_ext = $(shell x=$(blast_input_file); echo $${x\#\#*.} )

moa_must_define += blast_input_file
blast_input_file_help = Input fasta file to BLAST
blast_input_files = $(blast_input_file)
blast_input_file_type = file

include $(shell echo $$MOABASE)/template/blast.mk
