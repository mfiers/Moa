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
include $(MOABASE)/template/moa/prepare.mk

moa_id = bamextract
template_title = Bamextract
template_description = Extract one sequence from a bam file

moa_must_define += bamextract_bam_input
bamextract_bam_input_help = BAM input file
bamextract_bam_input_type = file

moa_must_define += bamextract_seq_id
bamextract_seq_id_help = List of sequence ids to extract
bamextract_seq_id_type = string

moa_must_define += bamextract_fasta_file
bamextract_fasta_file_help = Fasta file with the reference sequence data
bamextract_fasta_file_type = file

moa_may_define += bamextract_gff_file
bamextract_gff_file_help = GFF annotation file to extract data from
bamextract_gff_file_type = file
bamextract_gff_file_default = 

moa_may_define += bamextract_haplotypes
bamextract_haplotypes_help = No of haplotypes in the sample
bamextract_haplotypes_type = integer
bamextract_haplotypes_default = 2

#########################################################################
# Prerequisite testing
moa_prereq_simple += samtools fastaExtract

include $(shell echo $$MOABASE)/template/moa/core.mk

input_basename=$(shell basename $(bamextract_bam_input) .bam)

bam_output_files=$(addprefix ./$(input_basename).,\
		$(addsuffix .bam,$(bamextract_seq_id)))	

bai_output_files=$(addprefix ./$(input_basename).,\
		$(addsuffix .bam.bai, $(bamextract_seq_id)))	

pileup_output_files=$(addprefix ./$(input_basename).,\
		$(addsuffix .pileup, $(bamextract_seq_id)))

fasta_output_files=$(addsuffix .fasta,$(bamextract_seq_id))

fai_output_files=$(addsuffix .fasta.fai,$(bamextract_seq_id))

gff_output_files=$(addsuffix .gff,$(bamextract_seq_id))


bamextract: $(fasta_output_files) \
		$(fai_output_files) \
		$(bam_output_files) \
		$(bai_output_files) \
		$(gff_output_files) \
		$(pileup_output_files)

$(fasta_output_files): %.fasta: $(bamextract_fasta_file)
	$e $(call warn,Fasta extracting $*)
	echo $* | fastaExtract -l - -f $< > $@

$(fai_output_files): %.fasta.fai: %.fasta
	$e $(call warn,Fasta indexing $*)
	samtools faidx $<

#
# this two step extraction removes all headers - many programs seem
# unable to deal with these.
./$(input_basename).%.bam: $(bamextract_bam_input)
	$e $(call warn,Bam extracting $*)
	samtools view -b $< $* > $@

#| samtools view -bt ./$(input_basename).$*.fasta.fai - > $@

./$(input_basename).%.bam.bai: ./$(input_basename).%.bam
	$e $(call warn,Bam indexing $*)
	samtools index $<

$(gff_output_files): %.gff: $(bamextract_gff_file)
	$e $(call warn,Extracting GFF for $*)
	grep "^$*" $< > $@

$(pileup_output_files): $(input_basename).%.pileup: %.fasta $(input_basename).%.bam
	$e $(call warn,Genering pileup for $*)
	samtools pileup -N $(bamextract_haplotypes) -vcf $^ | samtools.pl varFilter | awk '$$6>=20' > $@


bamextract_clean:
	-rm *.fai *.fasta *.bam *.bai *.gff 2>/dev/null || true