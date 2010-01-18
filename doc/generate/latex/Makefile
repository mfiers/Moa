include $(shell echo $$MOABASE)/etc/moa.conf.mk

notemplate=__moaBase.mk moaBase.mk __upload2gbrowse.mk __moaBasePre.mk __moaBaseTest.mk\
	__moaBaseHelp.mk moaBasePre.mk __moaBaseVar.mk moaBasePre.mk

#templates=$(filter-out $notemplate,$(notdir $(wildcard $$MOABASE/template/*.mk)))
templates=$(sort $(filter-out $(notemplate),$(notdir $(wildcard $(shell echo $$MOABASE)/template/*.mk))))
temptex=$(addprefix ./templates/,$(patsubst %.mk,%.tex,$(templates)))

chapters = 						\
	introduction.tex 			\
	installation.tex  			\
	using.tex 					\
	gbrowse.tex 				\
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
	-mkdir templates

reference.tex:  $(temptex)
	cat ../../markdown/templates_header.md \
		| pandoc -f markdown -t latex \
		> reference.tex
	for f in $(temptex); do \
		cat $$f >> reference.tex ;\
	done

./templates/%.tex: $(shell echo $$MOABASE)/template/%.mk
	echo "\section{${subst _,\_,$*}}" > $@
	make -sf $$MOABASE/template/$*.mk help_latex >> $@

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

%.tex:
	cat ../../markdown/$*.md \
		| pandoc -f markdown -t latex \
		> $*.tex

clean:
	-rm *.aux *.bbl *.log *.blg *~ *.toc
	-rm -rf templates
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