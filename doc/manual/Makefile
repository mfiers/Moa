include $(shell echo $$MOABASE)/etc/moa.conf.mk

notemplate=__moaBase.mk moaBase.mk __upload2gbrowse.mk
#templates=$(filter-out $notemplate,$(notdir $(wildcard $$MOABASE/template/*.mk)))
templates=$(sort $(filter-out $(notemplate),$(notdir $(wildcard $(shell echo $$MOABASE)/template/*.mk))))
temptex=$(addprefix ./templates/,$(patsubst %.mk,%.tex,$(templates)))

chapters = 						\
	manual.tex 					\
	introduction.tex 			\
	installation.tex  			\
	using.tex 					\
	couchdb.tex 				\
	extending.tex				\
	reference.tex				


.PHONY: manual
manual: $(chapters)
	pdflatex manual
	bibtex manual
	pdflatex manual
	pdflatex manual	

templates.tex:  $(temptex)
	cat ../md/templates_header.md \
		| pandoc -f markdown -t latex \
		> templates.tex
	for f in $(temptex); do \
		cat $$f >> templates.tex ;\
	done

./templates/%.tex: $(shell echo $$MOABASE)/template/%.mk
	echo "\section{$*}" > $@
	make -sf $$MOABASE/template/$*.mk help_latex >> $@

manual.tex:
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
	cat ../md/$*.md \
		| pandoc -f markdown -t latex \
		> $*.tex

clean:
	-rm *.aux *.bbl *.log *.blg *~ *.toc
	-rm templates/*.tex
	-rm configuration.tex  	\
		creating.tex   		\
		execution.tex		\
		introduction.tex	\
		makefiles.tex 		\
		manual.tex			\
		templates.tex		\
		couchdb.tex 		\
		executing.tex		\
		installation.tex 	\
		extending.tex  		\
		using.tex