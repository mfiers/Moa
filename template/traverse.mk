# Empty - use this to create a new makefile
################################################################################
# Main target
maintarget:

################################################################################
# Help
moa_title = Traverse
moa_description = Do noting, except be a part in executing full directory structures

################################################################################
# Variable definition (non obligatory ones)

################################################################################
# Variable help definition

################################################################################
# moa definitions
#
#targets that the enduser might want to use
moa_targets += 
#varables that NEED to be defined
moa_must_define += 
#varaibles that might be defined
moa_may_define += 		

#Include base moa code - does variable checks & generates help				 
include $(shell echo $$MOABASE)/template/moaBase.mk

################################################################################
# End of the generic part - from here on you're on your own :)
