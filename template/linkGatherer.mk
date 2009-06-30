# gather a set of files using linkgs

################################################################################
# Definitions
# targets that the enduser might want to use
#moa_targets += gather_link clean
gather_link_help = Link-gather
clean_help = Remove anything that is not called Makefile or moa.mk 

# Help
moa_ids += gatherlink
moa_title_gatherlink = gather and link
moa_description_gatherlink = gather a set of files and create hardlinks to. Hardlinks have \
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

moa_may_define += glprocess
glprocess_help = Command to process the files. If undefined, hardlink the files. 

moa_may_define += limit_gather
limit_gather_help = limit the number of files gathered (with the most recent \
 files first, defaults to 1mln)

#Include base moa code - does variable checks & generates help
ifndef dont_include_moabase
	include $(shell echo $$MOABASE)/template/moaBase.mk
endif
################################################################################

#this is a dummy command, replaces every a with an a - hence nothing happens
#name_sed ?= 's/a/a/'
name_sed ?= s/\.genbank\.htg\.[0-9]/.fasta/
output_dir ?= .
limit_gather ?= 1000000
glprocess ?= ln -f $< $$target
gather_link_noclean ?= Makefile moa.mk 
.PHONY: gather_link_run
vpath % $(input_dirs)

.PHONY: gatherlink_prepare
gatherlink_prepare:
	-mkdir touch
	-mkdir $(output_dir)	

.PHONY: gatherlink_post
gatherlink_post:

#gather_link_run: $(addprefix touch/,$(notdir $(foreach dir, $(input_dirs), $(wildcard $(dir)/$(input_pattern))))) 	
gatherlink: $(addprefix touch/,$(notdir $(foreach dir, $(input_dirs), $(shell find $(dir) -name "$(input_pattern)" -printf "%A@\t%p\n" | sort -nr | head -$(limit_gather) | cut -f 2 ))))
# $(addprefix touch/,$(notdir 
# ))



touch/%: %
	@echo considering $<
	@target=$(output_dir)/$(shell echo "$(notdir $<)" | sed "$(name_sed)"); \
		echo target file is $$target ;\
		echo 'executing $(glprocess) ';\
		$(glprocess)
	@touch $@
#CLEAN
clean: gather_link_clean

gather_link_clean: fexcl=$(addprefix -not -name , $(gather_link_noclean))
gather_link_clean:
	if [ ! "$(output_dir)" == "." ]; then rm -rf $(output_dir); fi
	-rm -rf touch
	for x in `find . -maxdepth 1 -type f $(fexcl)`; do \
		rm $$x ;\
	done	