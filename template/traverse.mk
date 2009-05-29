#@+leo-ver=4-thin
#@+node:mf.20090529153542.1:@thin template/traverse.mk
#@@language makefile 
#@@tabwidth 4
#@+all
#@+node:mf.20090529202612.4:maintarget
################################################################################
# Main target
maintarget: traverse_main
#@nonl
#@-node:mf.20090529202612.4:maintarget
#@+node:mf.20090529202612.5:moa definitions
################################################################################
# Help
moa_ids += traverse
moa_title_traverse = Traverse
moa_description_traverse = Do noting, except be a part in executing full directory structures
#@nonl
#@-node:mf.20090529202612.5:moa definitions
#@+node:mf.20090529202612.6:include
#Include base moa code - does variable checks & generates help
ifndef dont_include_moabase
	include $(shell echo $$MOABASE)/template/moaBase.mk
endif
#@nonl
#@-node:mf.20090529202612.6:include
#@+node:mf.20090529202612.7:traverse_main
traverse_main:
	@echo "Traversing through `pwd`"
#@nonl
#@-node:mf.20090529202612.7:traverse_main
#@-all
#@-node:mf.20090529153542.1:@thin template/traverse.mk
#@-leo
