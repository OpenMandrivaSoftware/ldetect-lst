include Makefile.config

NAME = ldetect-lst
VERSION := 0.1.327.8

FILES = AUTHORS ChangeLog Makefile Makefile.config convert lst update-ldetect-lst

# Please do *not* just simply do "sync with mageia commits", but rather merge
# their individual commits in stead. See 'git format-patch' & 'git am' :)

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
	git archive --prefix=$(NAME)-$(VERSION)/ HEAD | xz -v -T0 > $(NAME)-$(VERSION).tar.xz;


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

ChangeLog:
	@if test -d "$$PWD/.git"; then \
	  git --no-pager log --format="%ai %aN %n%n%x09* %s%d%n" > $@.tmp \
	  && mv -f $@.tmp $@ \
	  && git commit ChangeLog -m 'generated changelog' \
	  && if [ -e ".git/svn" ]; then \
	    git svn dcommit ; \
	    fi \
	  || (rm -f  $@.tmp; \
	 echo Failed to generate ChangeLog, your ChangeLog may be outdated >&2; \
	 (test -f $@ || echo git-log is required to generate this file >> $@)); \
	else \
	 svn2cl --accum --authors ../common/username.xml; \
	 rm -f *.bak;  \
	fi;

# Makefile ends here
