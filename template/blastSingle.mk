#
#    Copyright 2009 Mark Fiers
#
#    This file is part of Moa 
#
#    Moa is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    Moa is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with Moa.  If not, see <http://www.gnu.org/licenses/>.
#
#    See: http://github.com/mfiers/Moa/
#
#this is a small adaptation of the blast template, expecting one single input file
#without escaping the following line would have read:
blast_input_dir = $(shell x=$(blast_input_file); echo $${x%/*})
#without escaping the following line would have read:
## blast_input_ext = $(shell export x=$(blast_input_file); echo ${x##*.} )
blast_input_ext = $(shell x=$(blast_input_file); echo $${x\#\#*.} )

moa_must_define += blast_input_file
blast_input_file_help = Input fasta file to BLAST
blast_input_files = $(blast_input_file)

include $(shell echo $$MOABASE)/template/blast.mk
