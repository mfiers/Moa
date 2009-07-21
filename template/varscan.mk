# Run Varscan
################################################################################

# Variable checks & definition & help
moa_ids += varscan 
moa_title_varscan = Varscan
moa_description_varscan = Run VARSCAN to detect snps

#variables
moa_must_define += varscan_input_file
varscan_input_file_help = Varscan input alignments file

moa_may_define += varscan_extra_params
varscan_extra_params_help = extra parameters to feed varscan

moa_may_define += varscan_output_name
varscan_output_name_help = Base name of the output files

moa_may_define += varscan_perl_file
varscan_extra_params_help = location of varscan.pl, defaults to \
  '/usr/lib/perl5/site_perl/5.8.8/varscan.pl'

ifndef dont_include_moabase
	include $(shell echo $$MOABASE)/template/moaBase.mk
endif

##### Derived variables for this run

#moa_register_extra += varscan_output
#moa_register_varscanout = $(shell echo `pwd`)/$(varscan_output_name)
varscan_perl_file ?= /usr/lib/perl5/site_perl/5.8.8/varscan.pl

.PHONY: varscan_prepare
varscan_prepare:

.PHONY: varscan_post
varscan_post: 

.PHONY: varscan
varscan:
	perl $(varscan_perl_file) easyrun \
		$(varscan_input_file) \
		--sample $(varscan_output_name)

$(varscan_output_name): $(varscan_input_files)
	varscan $(varscan_input_format_param) \
		-p $(MOA_PROCESSORS) \
		$(varscan_extra_params) \
		$(varscan_db) \
		$(call merge,$(comma),$^) \
		output

varscan_clean:
	-rm -f $(varscan_output_name)


