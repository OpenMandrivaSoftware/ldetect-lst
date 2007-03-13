include Makefile.config

PACKAGE = ldetect-lst
VERSION := 0.1.158

SVN_URL  := $(shell svn info | grep ^URL: | cut -f2 -d\ )
SVN_BASE := $(shell svn info | sed -n '/^URL: \(.*\/$(PACKAGE)\).*/s//\1/p')

FILES = AUTHORS ChangeLog Makefile Makefile.config convert lst update-ldetect-lst

.PHONY: changelog log

build: 
	make -C lst build

check:
	make -C lst check

clean:
	rm -f *~
	make -C lst clean

install: build
	install -d $(bindir) $(sbindir) $(dir)
	make -C lst install
	install update-ldetect-lst $(sbindir)
	install convert/merge2pcitable.pl $(bindir)

# rules to build a test rpm

cleandist:
	rm -rf $(PACKAGE)-$(VERSION) $(PACKAGE)-$(VERSION).tar.bz2

localcopy:
	svn export -q . $(PACKAGE)-$(VERSION)

tar:
	tar cvf $(PACKAGE)-$(VERSION).tar $(PACKAGE)-$(VERSION)
	bzip2 -9vf $(PACKAGE)-$(VERSION).tar
	rm -rf $(PACKAGE)-$(VERSION)


# rules to build a distributable rpm

dist: cleandist localcopy tar

log: changelog

changelog: ../common/username.xml
	svn2cl --authors ../common/username.xml --accum
	rm -f ChangeLog.bak
	svn commit -m "Generated by svn2cl the `LC_TIME=C date '+%d_%b'`" ChangeLog

# Makefile ends here
