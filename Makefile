#
# A Makefile to install moa
#

version?=$(shell git tag | sort -r | head -1 | cut -c2-)

all:
	#do nothing


INSTALLDIRS = etc doc/api doc/html doc/images doc/markdown template/	\
	template/moa template/moa/plugins lib/python lib/python/moa	\
	lib/python/moa/plugin template/util

install: DESTDIR2 = $(DESTDIR)/usr/share/moa
install:
	install -d $(DESTDIR2)/bin
	install -v -m 555 `find  bin/ -maxdepth 1 -type f ` $(DESTDIR2)/bin
	for i in $(INSTALLDIRS); do \
		install -d $(DESTDIR2)/$$i; \
		install -v -m 444 \
			`find  $$i  -maxdepth 1 -type f` \
			$(DESTDIR2)/$$i; \
	done			
	install -v README $(DESTDIR2)
	install -v COPYING $(DESTDIR2)
	install -v Makefile $(DESTDIR2)
	echo "Installing bash configuration to /etc/profile.d/moa.sh"
	echo "MOABASE=$(DESTDIR2)s"
	if [ "$$(id -u)" != "0" ]; then \
		echo "We're not root - installing locally"; \
		if grep -q "moainit.sh" ~/.bashrc; then \
			perl -pi'*.bak' -e 's|^.*moainit.sh.*$$|. $(DESTDIR2)/bin/moainit.sh|' ~/.bashrc; \
		else \
			echo >> ~/.bashrc ;\
			echo ". $(DESTDIR2)/bin/moainit.sh" >> ~/.bashrc; \
			echo >> ~/.bashrc ;\
		fi; \
	else \
		install -d $(DESTDIR)/etc/profile.d ;\
		echo "we're root: install moa conf in /etc/profile.d" ;\
		echo ". $(DESTDIR2)/bin/moainit.sh" > $(DESTDIR)/etc/profile.d/moa.sh;\
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
	cd $(BUILDDIR)/debian; cat changelog.t 			\
		| sed "s/DIST/$*/g" 				\
		| sed "s/VERSION/$(version)/g" > changelog
	cd $(BUILDDIR)/debian; cp control.$* control
	cd $(BUILDDIR); dpkg-buildpackage -S -rfakeroot
	cd $(PACKDIR); lintian -i moa_$(version)-*.dsc

	echo "to build the binary packages, execute:"
	echo cd $(BUILDDIR)
	echo sudo DIST=$* pbuilder build ../*dsc


tag_version: version=$(shell cat VERSION)
tag_version:
	@echo "setting  git tag to version v$(version)"
	-@git tag -d v$(version)  || true
	@git tag v$(version)
	@git tag -l