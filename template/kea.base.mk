SHELL := /bin/bash
.PHONY: set show help check prereqs

#see if a local variable set is defined
-include kea.local.mk

kea_targets += check help show all clean_all prereqs
check_help = Check variable definition
show_help = show defined variables
help_help = This help!
all_help = Recursively run through all subdirectories (use make all \
	action=XXX to run "make XXX" recursively) 
prereqs_help = Check if all prerequisites are present


###########################################################################
#check prerequisites
prereqlist += kea_envsettings
.PHONY: prereqs
prereqs: $(prereqlist)

#check if KEA_BASE_DIR is defined
kea_envsettings:
	@if env | grep -q KEA_BASE_DIR ; then true; else \
		echo "KEA_BASE_DIR is not defined :(" ; \
		false ;\
	fi

check: prereqs $(addprefix checkvar_, $(kea_must_define))
	@echo "Variable check: everything appears ok"
	
checkvar_%:
	@if [ "$(origin $(subst checkvar_,,$@))" == "undefined" ]; then \
		echo " *** Error $(subst checkvar_,,$@) is undefined" ;\
		exit -1; \
	fi

wset: $(addprefix storeweka_, $(kea_must_define) $(kea_may_define))

storeweka_%:		 
	@if [ "$(origin $(subst storeweka_,,$@))" == "command line" ]; then \
		echo " *** Set Weka var $(subst storeweka_,,$@) to 'weka get $($(subst storeweka_,,$@))'" ;\
		echo -n "$(subst storeweka_,,$@)=$$" >> kea.local.mk ;\
		echo "(shell weka get $($(subst storeweka_,,$@)))" >> kea.local.mk ; \
	fi

set: $(addprefix storevar_, $(kea_must_define) $(kea_may_define))

storevar_%:		 
	@if [ "$(origin $(subst storevar_,,$@))" == "command line" ]; then \
		echo " *** Set $(subst storevar_,,$@) to $($(subst storevar_,,$@))" ;\
		echo "$(subst storevar_,,$@)=$($(subst storevar_,,$@))" >> kea.local.mk ;\
	fi	
		
show: $(addprefix showvar_, $(kea_must_define) $(kea_may_define))

showvar_%:		 
	@echo "$(subst showvar_,,$@) : $($(subst showvar_,,$@))"

#dir traversing
kea_followups ?= $(shell find . -maxdepth 1 -type d -regex "\..+" -exec basename '{}' \; | sort )

.PHONY: $(kea_followups) all clean_all

all_check:
	@echo "would run make $(action)"
	@echo "in the following dirs"
	@echo $(kea_followups)
	
action ?= all
all: $(kea_followups)
	if [ "$(action)" == "all" ]; then \
		echo "running all without action, also run default action" ;\
		$(MAKE) ;\
	fi
	@echo "follows" $(kea_followups)

$(kea_followups):
	@echo "  ###########################"
	@echo "  ## Executing make $(action)"
	@echo "  ##   in $@ " 
	@echo "  ###########################"
	if [ -e $@/Makefile ]; then \
		cd $@ && $(MAKE) $(action) ;\
	fi

###############################################################################
# Help structure
help: kea_help_header \
	kea_help_target_header kea_help_target kea_help_target_footer \
	kea_help_vars_header kea_help_vars kea_help_vars_footer \
	kea_help_output_header kea_help_output kea_help_output_footer
	
kea_help_header:
	@echo -n "=="
	@echo -n "$(kea_title)" | sed "s/./=/g"
	@echo "=="
	@echo "= $(kea_title) ="
	@echo -n "=="
	@echo -n "$(kea_title)" | sed "s/./=/g"
	@echo "=="
	@echo 
	@echo "$(kea_description)" | fold -s
	@echo

## Help - output section
kea_help_output_header:
	@echo "Outputs"
	@echo "======="

kea_help_output: $(addprefix kea_output_, $(kea_outputs))

kea_output_%:
	@echo -n " - $($@)"
	@if [ "$(origin $@_help)" == "undefined" ]; then \
		echo ;\
	else \
		echo " : $($(subst helpvar_,,$@)_help)"  | fold -s ;\
	fi
	
	
kea_help_output_footer:
	@echo 
	
## Help - target section
kea_help_target_header:
	@echo "Targets"
	@echo "======="

kea_help_target: $(addprefix kea_target_, $(kea_targets))
	
	
kea_target_%:
	@echo -n " - $(subst kea_target_,,$@)"
	@if [ "$(origin $(subst kea_target_,,$@)_help)" == "undefined" ]; then \
		echo ;\
	else \
		echo " : $($(subst kea_target_,,$@)_help)" | fold -s  ;\
	fi
	
	
kea_help_target_footer:
	@echo 

## Help - output section
help_output_header:
	@echo "Output"
	@echo "======"
	
help_output_footer:
	@echo 
	
## Help - variable section
kea_help_vars_header:
	@echo "Variables"
	@echo "========="
	
kea_help_vars_footer:
	@echo "  * these vars must be defined"
	@echo 
	
kea_help_vars: kea_help_vars_must kea_help_vars_may

kea_help_vars_must: help_prefix="*"
kea_help_vars_must: $(addprefix helpvar_, $(kea_must_define))

kea_help_vars_may: help_prefix=" "
kea_help_vars_may: $(addprefix helpvar_, $(kea_may_define))


helpvar_%:
	@echo -n " - $(subst helpvar_,,$@)$(help_prefix)"
	@if [ "$(origin $(subst helpvar_,,$@)_help)" == "undefined" ]; then \
		echo ;\
	else \
		echo " - $($(subst helpvar_,,$@)_help)"  | fold -s;\
	fi
		
		