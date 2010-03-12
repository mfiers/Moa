#
# A Makefile to install moa
#

version?=HEAD

all:
	#do nothing

install:
	install -d bin $(DESTDIR)/bin
	install -d etc $(DESTDIR)/etc
	install -d doc $(DESTDIR)/doc
	install -d etc $(DESTDIR)/etc
	install -d lib $(DESTDIR)/lib
	install -d template $(DESTDIR)/template
	install README $(DESTDIR)
	install COPYING $(DESTDIR)
	install quick_init.sh $(DESTDIR)
	install Makefile $(DESTDIR)

package: source_package deb_jaunty deb_karmic 

source_package:
	mkdir -p build/src
	git archive --format=tar --prefix=moa-$(version)/ $(version)	\
		Makefile etc bin COPYING doc etc lib quick_init.sh README	\
		template | gzip > build/src/moa-$(version).tar.gz

deb_%: PACKDIR = build/deb/$*
deb_%: BUILDDIR = build/deb/$*/moa-$(version)
deb_%: source_package
	@echo "Building version $(version) for $* in $(BUILDDIR)"
	mkdir -p build/deb/$*
	cp build/src/moa-$(version).tar.gz $(PACKDIR)/moa_$(version).orig.tar.gz
	cd $(PACKDIR)*; tar xzf moa_$(version).orig.tar.gz
	git archive --format=tar --prefix=moa-$(version)/ $(version) \
		debian | tar x -C $(PACKDIR)
	cd $(BUILDDIR)/debian; cat changelog.t | sed "s/DIST/$*/g" > changelog
	cd $(BUILDDIR); dpkg-buildpackage -S -rfakeroot
	cd $(PACKDIR); lintian -i moa_$(version)-*.dsc
	cd $(PACKDIR); sudo DIST=$* pbuilder build *dsc