################################################################################
# Main target
maintarget: traverse_main
################################################################################
# Help
moa_ids += traverse
moa_title_traverse = Traverse
moa_description_traverse = Do noting, except be a part in executing full directory structures#Include base moa code - does variable checks & generates helpifndef dont_include_moabase
	include $(shell echo $$MOABASE)/template/moaBase.mk
endif
traverse_main:
	@echo "Traversing through `pwd`"#dummy, doesn't do anything :)
clean: