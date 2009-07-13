# gather a set of files using linkgs

################################################################################
# Definitions
# targets that the enduser might want to use
#moa_targets += gather_link clean
gather_help = gather files
clean_help = Remove anything that is not called Makefile or moa.mk 

# Help
moa_ids += gather
moa_title_gather = gather files
moa_description_gather = gather a set of files and create hardlinks to. Hardlinks have \
 as advantage that updates are noticed via the timestamp. Hence, make recognizes \
 them. 
 
# Output definition
moa_outputs += gather
moa_output_gather = *
moa_output_gather_help = Gathered files - can be anything you define.

#varables that NEED to be defined
moa_must_define += g_input_dir g_input_pattern 
g_input_dir_help = list of directories with the input files
g_input_pattern_help = glob pattern to download

moa_may_define += g_name_sed g_output_dir
name_sed_help = Sed substitution command that alters the filename, \
  defaults to leaving the names untouched.
g_output_dir_help = Output subdirectory, defaults to '.'

moa_may_define += g_process
g_process_help = Command to process the files. If undefined, hardlink the files. 

moa_may_define += g_limit
g_limit_help = limit the number of files gathered (with the most recent \
 files first, defaults to 1mln)

#Include base moa code - does variable checks & generates help
include $(shell echo $$MOABASE)/template/moaBase.mk


#########################################################################

#this is a dummy command, replaces every a with an a - hence nothing happens

g_name_sed ?= 's/a/a/'
#name_sed ?= s/\.genbank\.htg\.[0-9]/.fasta/
g_output_dir ?= .
g_limit ?= 1000000
g_process ?= ln -f $< $(g_target)
gather_link_noclean ?= Makefile moa.mk 
.PHONY: gather_link_run
vpath % $(g_input_dir)

.PHONY: gather_prepare
gather_prepare:
	-mkdir touch
	-mkdir $(g_output_dir)	

.PHONY: gather_post
gather_post:

.NOTPARALLEL: gather
.PHONY: gather
gather: $(addprefix touch/,$(notdir $(foreach dir, $(g_input_dir), $(shell find $(dir) -name "$(g_input_pattern)" -printf "%A@\t%p\n" | sort -nr | head -$(g_limit) | cut -f 2 ))))

touch/%: g_target=$(shell echo "$(g_output_dir)/$*" | sed $(g_name_sed))
touch/%: %
	@echo considering $< - $(g_target)
	$(g_process)
	@touch $@

gather_clean:
	if [ ! "$(g_output_dir)" == "." ]; then rm -rf $(g_output_dir); fi
	-rm -rf touch
