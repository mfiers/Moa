#
# A Makefile to install moa
#

version?=HEAD

all:
	#do nothing


INSTALLDIRS = etc doc/api doc/html doc/images doc/markdown \
	template/ template/moa template/moa/plugins \
	lib/python lib/python/moa lib/python/moa/plugin

install:
	install -d $(DESTDIR)/bin
	install -v -m 555 `find  bin/ -maxdepth 1 -type f ` $(DESTDIR)/bin
	for i in $(INSTALLDIRS); do \
		install -d $(DESTDIR)/$$i; \
		install -v -m 444 \
			`find  $$i  -maxdepth 1 -type f` \
			$(DESTDIR)/$$i; \
	done			
	install -v README $(DESTDIR)
	install -v COPYING $(DESTDIR)
	install -v Makefile $(DESTDIR)
	echo "Installing bash configuration to /etc/profile.d/moa.sh"
	echo "MOABASE=$(DESTDIR)s"
	if [ "$$(id -u)" != "0" ]; then \
		echo "We're not root - installing locally"; \
		if grep -q "moainit.sh" ~/.bashrc; then \
			perl -pi'*.bak' -e 's|^.*moainit.sh.*$$|. $(DESTDIR)/bin/moainit.sh|' ~/.bashrc; \
		else \
			echo >> ~/.bashrc ;\
			echo ". $(DESTDIR)/bin/moainit.sh" >> ~/.bashrc; \
			echo >> ~/.bashrc ;\
		fi; \
	else \
		install -d etc/profile.d ;\
		echo "we're root: install moa conf in /etc/profile.d" ;\
		echo ". $(DESTDIR)/bin/moainit.sh" > /tmp/moa_etc_profile;\
		install -v /tmp/moa_etc_profile etc/profile.d/moa.sh ;\
	fi

package: source_package deb_jaunty

source_package:
	mkdir -p build/src
	git archive --format=tar --prefix=moa-$(version)/ v$(version)	\
		Makefile etc bin COPYING doc etc lib README template 	\
		| gzip >						\
		build/src/moa-$(version).tar.gz

deb_%: PACKDIR = build/deb/$*
deb_%: BUILDDIR = build/deb/$*/moa-$(version)
deb_%: source_package
	@echo "Building version $(version) for $* in $(BUILDDIR)"
	mkdir -p build/deb/$*
	cp build/src/moa-$(version).tar.gz $(PACKDIR)/moa_$(version).orig.tar.gz
	cd $(PACKDIR)*; tar xzf moa_$(version).orig.tar.gz
	git archive --format=tar --prefix=moa-$(version)/ v$(version) \
		debian | tar x -C $(PACKDIR)
	cd $(BUILDDIR)/debian; cat changelog.t | sed "s/DIST/$*/g" > changelog
	cd $(BUILDDIR); dpkg-buildpackage -S -rfakeroot
	cd $(PACKDIR); lintian -i moa_$(version)-*.dsc
	cd $(BUILDDIR); sudo DIST=$* pbuilder build ../*dsc