include Makefile.config

PACKAGE = ldetect-lst
VERSION := $(shell rpm -q --qf '%{VERSION}\n' --specfile $(PACKAGE).spec | head -1)
RELEASE := $(shell rpm -q --qf '%{RELEASE}\n' --specfile $(PACKAGE).spec | head -1)
TAG := $(shell echo "V$(VERSION)_$(RELEASE)" | tr -- '-.' '__')

FILES = AUTHORS ChangeLog Makefile Makefile.config convert err ldetect-lst.spec lst update-ldetect-lst

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

localrpm: localdist buildrpm

localdist: cleandist dir localcopy tar

cleandist:
	rm -rf $(PACKAGE)-$(VERSION) $(PACKAGE)-$(VERSION).tar.bz2

dir:
	mkdir $(PACKAGE)-$(VERSION)

localcopy:
	tar c $(FILES) | tar x -C $(PACKAGE)-$(VERSION)

tar:
	tar cvf $(PACKAGE)-$(VERSION).tar $(PACKAGE)-$(VERSION)
	bzip2 -9vf $(PACKAGE)-$(VERSION).tar
	rm -rf $(PACKAGE)-$(VERSION)

buildrpm:
	rpm -ta $(PACKAGE)-$(VERSION).tar.bz2

# rules to build a distributable rpm

rpm: changelog cvstag dist buildrpm

dist: cleandist dir export tar

export:
	cvs export -d $(PACKAGE)-$(VERSION) -r $(TAG) $(PACKAGE)

cvstag:
	cvs tag $(CVSTAGOPT) $(TAG)

changelog: ../common/username
	cvs2cl -U ../common/username -I ChangeLog 
	rm -f ChangeLog.bak
	cvs commit -m "Generated by cvs2cl the `date '+%d_%b'`" ChangeLog

# Makefile ends here
