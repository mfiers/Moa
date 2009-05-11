# Empty - use this to create a new makefile
################################################################################
# Main target
maintarget: check *TODO*

################################################################################
# Help
help_intro:
	@echo "*TODO*"

help_output:
	@echo "*TODO*"

################################################################################
# Variable definition (non obligatory ones)

################################################################################
# Variable help definition

################################################################################
# makea definitions
#
#targets that the enduser might want to use
kea_targets += *TODO*
#varables that NEED to be defined
kea_must_define += *TODO*
#varaibles that might be defined
kea_may_define += *TODO*		
#Include base kea code - does variable checks & generates help				 
include $(shell echo $$KEA_BASE_DIR)/template/kea.base.mk

################################################################################
# End of the generic part - from here on you're on your own :)
