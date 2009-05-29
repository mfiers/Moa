# Run Mummer between two sequences
#
##### Main target
maintarget: check mummer

################################################################################
# Variable checks & definition & help
moa_ids += mummer
moa_title_mummer = mummer
moa_description_mummer = Run mummer between two sequences
	
#targets
moa_targets += mummer clean 
mummer2seq_help = run Mummer

#variables
moa_must_define += input_dir 
moa_may_define += input_extension

ifndef dont_include_moabase
	include $(shell echo $$MOABASE)/template/moaBase.mk
endif


input_files = $(wildcard $(input_dir)/*.$(input_extension))

mummer: $(input_files)
	for f1 in $^; do \
		for f2 in $^; do \
			echo "considering $$f1 and $$f2 " ;\
			export prefix=`basename $$f1 .$(input_extension)`_`basename $$f2 .$(input_extension)` ;\
			echo "prefix is $$prefix" ;\
			nucmer --prefix=$$prefix $$f1 $$f2 ;\
			show-coords -rcl $$prefix.delta > $$prefix.coords ;\
			mummerplot -t png --large -p $$prefix $$prefix.delta ;\
		done ;\
	done
	
clean: mummer_clean

mummer_clean:
	-rm *delta