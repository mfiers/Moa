today := `date`
moaversion := `cat ../VERSION`
gitversion := `git-log --pretty=oneline -n 1 manual.main.tex | cut -f 1 -d' '`
gitbranch := `git branch | grep "*" | cut -c3-`

all: *.tex
	cat manual.main.tex | sed "s/#DATE#/$(today)/" \
	    | sed "s/#GITVERSION#/$(gitversion)/" \
	    | sed "s/#MOAVERSION#/$(moaversion)/" \
	    | sed "s/#GITBRANCH#/$(gitbranch)/" \
	    > manual.tex

	pdflatex manual.tex
	bibtex manual
	pdflatex manual.tex
	pdflatex manual.tex