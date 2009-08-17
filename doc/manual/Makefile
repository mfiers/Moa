makefiles=blast blat blastdb bowtie bowtiedb clustalw dottup fasta2gff gap4export getFromNcbi gmapdb gmap lftp mummer nstretch pregap traverse varscan upload2gbrowse

all: create_main \
			create_chapters \
			create_makefiles
	pdflatex manual
	bibtex manual
	pdflatex manual
	pdflatex manual	

.PHONY: create_makefiles
create_makefiles: cm_prepare \
		$(addprefix cm__,$(sort $(makefiles)))

cm_prepare:
	cat templates.md \
		| pandoc -f markdown -t latex \
		> templates.tex

	echo 
	cat makefiles.template.tex > makefiles.tex

cm__%:
	echo "\section{$*}" >> makefiles.tex
	make -sf $$MOABASE/template/$*.mk help_latex \
		>> makefiles.tex

.PHONY: create_main
create_main:
	cat manual.template.tex 								\
		| sed "s/#DATE#/$(shell date)/" 				\
		| sed "s/#MOAVERSION#/$(shell 					\
				cat ../../VERSION)/"					\
		| sed "s/#GITVERSION#/$(shell					\
			git show | head -1 | cut -f 2 -d' ')/"		\
		| sed "s/#GITBRANCH#/$(shell					\
			git branch | head -1 | cut -f 2 -d' ')/"	\
			> manual.tex

chapters = introduction installation using
create_chapters:  $(addprefix c__, $(chapters))

c__%:
	cat $*.md \
		| pandoc -f markdown -t latex \
		> $*.tex
