
## this is to get the location of pandoc - assuming it's defined there
include $(shell echo $$MOABASE)/etc/moa.conf.mk

introduction_title = Introduction
installation_title = Installation
using_title = Using Moa
couchdb_title = Using Couchdb with Moa
gbrowse_title = Using GBrowse with Moa
extending_title = Extending Moa

chapters =						\
	index.html					\
	introduction.html 			\
	installation.html  			\
	using.html 					\
	couchdb.html 				\
	gbrowse.html 				\
	extending.html				\
	reference.html

.PHONY: all
all: imagesao $(addprefix ../../html/,$(chapters))

.PHONY: imagesao
imagesao: moa.css images/moa_logo_small.png  images/moa_logo_smaller.png
	cp moa.css ../../html/
	cp images/moa_logo_small.png ../../html/
	cp images/moa_logo_smaller.png ../../html/
	cp images/pfr_logo.jpg ../../html/
	cp ../../manual.pdf ../../html/

moa.css:
	cp moa.css site
site/index.html: index.template.html header.html footer.html
	cp ../images/moa_logo_medium.png ../../html/
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

temptex=$(addprefix ../../html/t__,$(addsuffix .html,$(templates)))

../../html/reference.html: $(temptex)
	cat header.html > $@
	cat reference.template.html >> $@
	echo "<ul>" >> $@
	for tem in $(templates); do \
		echo "<li><a href='./t__$$tem.html'>$$tem</a></li>" >> $@ ;\
	done
	echo "</ul>" >> $@
	cat footer.html >> $@

../../html/t__%.html: $(shell echo $$MOABASE)/template/%.mk
	cat header.html > $@
	echo '<h1 id="chapterTitle">$*.mk</h1>' >> $@
	$(MAKE) -s -f $< help_markdown \
		| $(pandocbin) -f markdown -t html 		\
		>> $@
	cat footer.html >> $@

../../html/%.html: ../md/%.md footer.html header.html
	cat header.html > $@
	echo '<h1 id="chapterTitle">$($*_title)</h1>' >> $@
	cat $< 										\
		| $(pandocbin) -f markdown -t html 		\
		>> $@
	cat footer.html >> $@

clean:
	rm ../../html/*