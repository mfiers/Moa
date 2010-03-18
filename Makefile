#
# A Makefile to create moa debian packages
#

version?=$(shell git tag | sort -r | head -1 | cut -c2-)

all:


package: source_package deb_jaunty

source_package:
	mkdir -p build/src
	git archive --format=tar --prefix=moa-$(version)/ v$(version)	\
		Makefile etc bin COPYING doc etc lib README template 	\
		| gzip > build/src/moa-$(version).tar.gz

deb_%: PACKDIR = build/deb/$*
deb_%: BUILDDIR = build/deb/$*/moa-$(version)
deb_%: source_package
	@echo "Building version $(version) for $* in $(BUILDDIR)"
	mkdir -p build/deb/$*
	cp build/src/moa-$(version).tar.gz $(PACKDIR)/moa_$(version).orig.tar.gz
	cd $(PACKDIR)*; tar xzf moa_$(version).orig.tar.gz
	git archive --format=tar --prefix=moa-$(version)/ v$(version) \
		debian | tar x -C $(PACKDIR)
	#create an /etc/profile.d file t
	cd $(BUILDDIR); mkdir etc/profile.d; \
		echo ". /usr/share/moa/bin/moainit.sh || true" > etc/profile.d/moa.sh
	#fix the changelog for this version
	cd $(BUILDDIR)/debian; cat changelog.t 			\
		| sed "s/DIST/$*/g" 				\
		| sed "s/VERSION/$(version)/g" > changelog
	#create distro specific files 
	cd $(BUILDDIR)/debian; \
		for x in *.$*; do \
			echo "$$x to `basename $$x .$*`" ;\
			cp $$x `basename $$x .$*`; \
		done
	#build the source package
	cd $(BUILDDIR); dpkg-buildpackage -S -rfakeroot
	#and run a lintian check
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