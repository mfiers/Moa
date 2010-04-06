include $(shell echo $$MOABASE)/etc/moa.conf.mk

template2html=$(addsuffix .tex,$(addprefix t___,$(subst /,___,$(1))))
html2template=$(addsuffix .mk,\
		$(addprefix $(MOABASE)/template/,\
			$(subst ___,/,$(1))))
templates=$(shell moa list)
temptex=$(foreach v,$(templates),$(call template2html,$(v)))
#temptex=$(addprefix ./templates/,$(patsubst %.mk,%.tex,$(templates)))

chapters = 						\
	introduction.tex 			\
	installation.tex  			\
	using.tex 					\
	extending.tex				\
	reference.tex				\
	manual.tex 					

.PHONY: manual
manual: prepare $(chapters)
	pdflatex manual
	bibtex manual
	pdflatex manual
	pdflatex manual	
	mv manual.pdf ../..

.PHONY: prepare
prepare:

$(warning $(temptex))
reference.tex:  $(temptex)
	#cat ../../markdown/templates_header.md \
	#		| $(pandocbin) -f markdown -t latex \
	#	> reference.tex
	for f in $(temptex); do \
		cat $$f >> reference.tex ;\
	done

slash=/
t___%.tex: 
	template=$(MOABASE)/template/$(subst ___,$(slash),$*).mk; \
	 	echo "\section{${subst _,\_,${subst ___,/,$*}}}" > $@ ;\
		make -sf $$template help_latex >> $@

manual.tex: manual.template.tex
	cat manual.template.tex 							\
		| sed "s/#DATE#/$(shell date)/" 				\
		| sed "s/#MOAVERSION#/$(shell 					\
				cat ../../VERSION)/"					\
		| sed "s/#GITVERSION#/$(shell					\
			git show | head -1 | cut -f 2 -d' ')/"		\
		| sed "s/#GITBRANCH#/$(shell					\
			git branch | head -1 | cut -f 2 -d' ')/"	\
			> manual.tex

%.tex: ../../markdown/%.md
	cat $< | $(pandocbin) -f markdown -t latex > $@

clean:
	-rm *.aux *.bbl *.log *.blg *~ *.toc
	-rm -rf templates
	-rm t___*
	-rm configuration.tex  	\
		creating.tex   		\
		execution.tex		\
		introduction.tex	\
		makefiles.tex 		\
		manual.tex			\
		reference.tex		\
		executing.tex		\
		installation.tex 	\
		extending.tex  		\
		using.tex