include Makefile.config

NAME = ldetect-lst
VERSION := 0.1.323

FILES = AUTHORS ChangeLog Makefile Makefile.config convert lst update-ldetect-lst

.PHONY: changelog log ChangeLog

build: 
	$(MAKE) -C lst build
	$(MAKE) -C dkms-modules-info build

check:
	$(MAKE) -C lst check

clean:
	rm -f *~
	$(MAKE) -C lst clean

install: build
	install -d $(bindir) $(sbindir) $(dir)
	$(MAKE) -C lst install
	$(MAKE) -C dkms-modules-info install
	install update-ldetect-lst $(sbindir)
	install convert/merge2pcitable.pl $(bindir)

# rules to build a distributable rpm

dist-svn: 
	svn export -q -rBASE . $(NAME)-$(VERSION)
	tar cfJ ../$(NAME)-$(VERSION).tar.xz $(NAME)-$(VERSION) 
	rm -rf $(NAME)-$(VERSION) 
				 
dist-git: 
	git archive --prefix=$(NAME)-$(VERSION)/ HEAD | xz -v > $(NAME)-$(VERSION).tar.xz;


dist: dist-git
	$(info $(NAME)-$(VERSION).tar.xz is ready)

dis: clean
	rm -rf ../$(NAME)-$(VERSION)*.tar* $(NAME)-$(VERSION)
	@if [ -e ".svn" ]; then \
		$(MAKE) dist-svn; \
	elif [ -e ".git" ]; then \
		$(MAKE) dist-git; \
	else \
		echo "Unknown SCM (not SVN nor GIT)";\
		exit 1; \
	fi;

	$(info $(shell dirname $$PWD)/$(NAME)-$(VERSION).tar.xz is ready)

log: changelog

changelog: ChangeLog

ChangeLog: ../common/username.xml
	@if test -d "$$PWD/.git"; then \
		../common/gitlog-to-changelog > $@.tmp \
	  && mv -f $@.tmp $@ \
	  || (rm -f  $@.tmp; \
	 echo Failed to generate ChangeLog, your ChangeLog may be outdated >&2; \
	 (test -f $@ || echo git-log is required to generate this file >> $@)); \
	else \
	 svn2cl --accum --authors ../common/username.xml; \
	 rm -f *.bak;  \
	 svn commit -m "Generated by svn2cl the `LC_TIME=C date '+%d_%b'`" ChangeLog; \
	fi;

# Makefile ends here
