#
# A Makefile to install moa
#

version?=HEAD

all:
	#do nothing

install:
	-rm bin/wmoa
	install -d $(DESTDIR)/bin
	install -d $(DESTDIR)/etc
	install -d $(DESTDIR)/doc/api
	install -d $(DESTDIR)/doc/html
	install -d $(DESTDIR)/doc/images
	install -d $(DESTDIR)/doc/markdown
	install -d $(DESTDIR)/template/moa/plugins
	install id $(DESTDIR)/lib/python/moa/plugins
	install bin/* $(DESTDIR)/bin
	install etc/* $(DESTDIR)/etc
	install template/* $(DESTDIR)/template
	install template/moa/* $(DESTDIR)/template/moa
	install template/moa/plugins/* $(DESTDIR)/template/moa/plugins
	install lib/python/* $(DESTDIR)/lib/python/
	install lib/python/moa/* $(DESTDIR)/lib/python/moa/
	install lib/python/moa/plugin/* $(DESTDIR)/lib/python/moa/plugin
	install -v README $(DESTDIR)
	install -v COPYING $(DESTDIR)
	install -v quick_init.sh $(DESTDIR)
	install -v Makefile $(DESTDIR)

package: source_package deb_jaunty

source_package:
	mkdir -p build/src
	git archive --format=tar --prefix=moa-$(version)/ $(version)	\
		Makefile etc bin COPYING doc etc lib quick_init.sh	\
		README template | gzip >				\
		build/src/moa-$(version).tar.gz

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
	#cd $(PACKDIR); sudo DIST=$* pbuilder build *dsc