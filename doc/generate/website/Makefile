
## this is to get the location of pandoc - assuming it's defined there
include $(MOABASE)/etc/moa.conf.mk

introduction_title = Introduction
installation_title = Installation
using_title = Using Moa
gbrowse_title = Using GBrowse with Moa
extending_title = Extending Moa

chapters = \
	index.html \
	introduction.html \
	installation.html \
	commands.html \
	extending.html \
	reference.html

.PHONY: test
	@echo hello

.PHONY: all
all: imagesao $(addprefix ../../html/,$(chapters))

.PHONY: imagesao
imagesao: moa.css $(shell find ../../images)
	cp moa.css ../../html/
	cp -r ../../images/ ../../html/
	cp ../../manual.pdf ../../html/moa_manual.pdf
	cp -r ../../api ../../html/api

../../html/index.html: index.template.html header.html footer.html
	cat header.html > $@
	cat index.template.html \
		| sed "s/#DATE#/$(shell date)/" \
		| sed "s/#MOAVERSION#/$(shell \
				cat ../../../VERSION)/" \
		| sed "s/#GITVERSION#/$(shell \
				git show | head -1 | cut -f 2 -d' ')/" \
		| sed "s/#GITBRANCH#/$(shell \
				git branch | head -1 | cut -f 2 -d' ')/" \
		>> $@
	cat footer.html >> $@

slash=/
template2html=$(addsuffix .html, \
		$(addprefix ../../html/t___,$(subst $(slash),___,$(1))))
html2template=$(addsuffix .mk,\
		$(addprefix $(MOABASE)/template/,\
			$(subst ___,$(slash),$(1))))
templates=$(shell moa list)
temptex=$(foreach v,$(templates),$(call template2html,$(v)))

../../html/reference.html: $(temptex)
	cat header.html > $@
	cat reference.template.html >> $@
	echo "<ul>" >> $@
	for tem in $(temptex); do \
		echo "<li><a href='./"`basename $$tem`"'>"`basename $$tem | sed "s/t___//" | sed "s/___/\//g" | sed "s/\.html$$//"`"</a></li>" >> $@ ;\
	done
	echo "</ul>" >> $@
	cat footer.html >> $@

#../../html/commands.html: $(wildcard  ../../markdown/commands/*.md)
#		for x in $(sort $^); do \
#		echo $$x;
#	done

../../html/t___%.html:
	cat header.html > $@
	echo '<h1 id="chapterTitle">'$(subst ___,$(slash),$*)'</h1>' >> $@
	$(MAKE) -s -f $(call html2template,$*) help_markdown \
		| $(pandocbin) -f markdown -t html 		\
		>> $@
	cat footer.html >> $@

../../html/%.html: ../../markdown/%.md footer.html header.html
	echo "Remaking $*"
	cat header.html > $@
	echo '<h1 id="chapterTitle">$($*_title)</h1>' >> $@
	cat $< 										\
		| $(pandocbin) -f markdown -t html 		\
		>> $@
	cat footer.html >> $@

clean:
	rm -rf ../../html/*