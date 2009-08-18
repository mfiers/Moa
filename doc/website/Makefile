include $(shell echo $$MOABASE)/etc/moa.conf.mk

introduction_title = Introduction
installation_title = Installation
using_title = Using Moa
couchdb_title = Using Couchdb with Moa
extending_title = Extending Moa

chapters =						\
	index.html					\
	introduction.html 			\
	installation.html  			\
	using.html 					\
	couchdb.html 				\
	extending.html				\
	reference.html

.PHONY: all
all: imagesao $(addprefix site/,$(chapters))

.PHONY: imagesao
imagesao: moa.css ../images/moa_logo_small.png  ../images/moa_logo_smaller.png
	cp moa.css site/
	cp ../images/moa_logo_small.png site/
	cp ../images/moa_logo_smaller.png site/

site/index.html: index.template.html header.html footer.html
	cp ../images/moa_logo_medium.png site/
	cat header.html > $@
	cat index.template.html 								\
		| sed "s/#DATE#/$(shell date)/" 					\
		| sed "s/#MOAVERSION#/$(shell 						\
				cat ../../VERSION)/" 						\
		| sed "s/#GITVERSION#/$(shell 						\
				git show | head -1 | cut -f 2 -d' ')/" 		\
		| sed "s/#GITBRANCH#/$(shell 						\
				git branch | head -1 | cut -f 2 -d' ')/" 	\
		>> $@
	cat footer.html >> $@

notemplate=__moaBase.mk moaBase.mk __upload2gbrowse.mk
templates=$(patsubst %.mk,%,								\
				$(sort $(filter-out $(notemplate),			\
					$(notdir $(wildcard 					\
						$(shell echo $$MOABASE)/template/*.mk)))))

temptex=$(addprefix ./site/t__,$(addsuffix .html,$(templates)))

site/reference.html: $(temptex)
	cat header.html > $@
	cat reference.template.html >> $@
	echo "<ul>" >> $@
	for tem in $(templates); do \
		echo "<li><a href='./t__$$tem.html'>$$tem</a></li>" >> $@ ;\
	done
	echo "</ul>" >> $@
	cat footer.html >> $@

site/t__%.html: $(shell echo $$MOABASE)/template/%.mk
	cat header.html > $@
	echo '<h1 id="chapterTitle">$*.mk</h1>' >> $@
	$(MAKE) -s -f $< help_markdown \
		| $(pandocbin) -f markdown -t html 		\
		>> $@
	cat footer.html >> $@

site/%.html: ../md/%.md footer.html header.html
	cat header.html > $@
	echo '<h1 id="chapterTitle">$($*_title)</h1>' >> $@
	cat $< 										\
		| $(pandocbin) -f markdown -t html 		\
		>> $@
	cat footer.html >> $@

clean:
	rm site/*