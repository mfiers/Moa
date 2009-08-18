include $(shell echo $$MOABASE)/etc/moa.conf.mk

chapters =						\
	index.html					\
	introduction.html 			\
	installation.html  			\
	using.html 					\
	couchdb.html 				\
	extending.html

all: $(addprefix site/,$(chapters))

site/%.html: ../md/%.md
	cat header.html > $@
	cat $< 										\
		| $(pandocbin) -f markdown -t html 		\
		>> $@
	cat footer.html >> $@

clean:
	rm site/*