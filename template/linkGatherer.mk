# gather a set of files using linkgs

# Main target - should be first in the file
moa_main_target: check gather_link

################################################################################
# Definitions
# targets that the enduser might want to use
moa_targets += gather_link clean
gather_link_help = Link-gather
clean_help = Remove anything that is not called Makefile or moa.mk 

# Help
moa_title =  Gather & link
moa_description = gather a set of files and create hardlinks to. Hardlinks have \
 as advantage that updates are noticed via the timestamp. Hence, make recognizes \
 them. 
 
# Output definition
moa_outputs += gather
moa_output_gather = *
moa_output_gather_help = Gathered files - can be anything you define.

#varables that NEED to be defined
moa_must_define += input_dirs input_pattern 
input_dirs_help = list of directories with the input files
input_pattern_help = glob pattern to download

moa_may_define += name_sed output_dir
name_sed_help = Sed substitution command that alters the filename, defaults \
  to leaving the names untouched.
output_dir_help = Output subdirectory, defaults to '.'


#Include base moa code - does variable checks & generates help				 
include $(shell echo $$MOABASE)/template/moaBase.mk

################################################################################

#this is a dummy command, replaces every a with an a - hence nothing happens
#name_sed ?= 's/a/a/'
name_sed ?= s/\.genbank\.htg\.[0-9]/.fasta/
output_dir ?= .
gather_link_noclean ?= Makefile moa.mk 

vpath % $(input_dirs)
input_files := $(foreach dir, $(input_dirs), $(wildcard $(dir)/$(input_pattern)))
touch_files = $(addprefix touch/, $(notdir $(input_files)))

gather_link: gather_link_prep gather_link_run 
		
gather_link_prep:
	-mkdir touch
	-mkdir $(output_dir)
	
gather_link_run: $(touch_files)

touch/%: %
	@echo considering $@
	@newname=$(output_dir)/$(shell echo "$(notdir $<)" | sed "$(name_sed)"); \
		ln -f $< $$newname ;\
		touch $@
		

#CLEAN
clean: gather_link_clean

gather_link_clean: fexcl=$(addprefix -not -name , $(gather_link_noclean))
gather_link_clean:
	if [ ! "$(output_dir)" == "." ]; then rm -rf $(output_dir); done
	for x in `find . -maxdepth 1 -type f $(fexcl)`; do \
		rm $$x ;\
	done
	