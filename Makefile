include Makefile.config

PACKAGE = ldetect-lst
VERSION := 0.1.227

SVN_URL  := $(shell svn info | grep ^URL: | cut -f2 -d\ )
SVN_BASE := $(shell svn info | sed -n '/^URL: \(.*\/$(PACKAGE)\).*/s//\1/p')

FILES = AUTHORS ChangeLog Makefile Makefile.config convert lst update-ldetect-lst

.PHONY: changelog log

build: 
	make -C lst build
	make -C dkms-modules-info build

check:
	make -C lst check

clean:
	rm -f *~
	make -C lst clean

install: build
	install -d $(bindir) $(sbindir) $(dir)
	make -C lst install
	make -C dkms-modules-info install
	install update-ldetect-lst $(sbindir)
	install convert/merge2pcitable.pl $(bindir)

# rules to build a test rpm

cleandist:
	rm -rf $(PACKAGE)-$(VERSION) $(PACKAGE)-$(VERSION).tar.lzma

localcopy:
	svn export -q -rBASE . $(PACKAGE)-$(VERSION)

tar:
	tar cfY $(PACKAGE)-$(VERSION).tar.lzma $(PACKAGE)-$(VERSION)
	rm -rf $(PACKAGE)-$(VERSION)


# rules to build a distributable rpm

dist: cleandist localcopy tar

log: changelog

changelog: ../common/username.xml
	svn2cl --authors ../common/username.xml --accum
	rm -f ChangeLog.bak
	svn commit -m "Generated by svn2cl the `LC_TIME=C date '+%d_%b'`" ChangeLog

# Makefile ends here
