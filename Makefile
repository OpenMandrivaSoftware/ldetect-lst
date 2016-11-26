include Makefile.config

NAME = ldetect-lst
VERSION := 0.1.338.2

FILES = AUTHORS Makefile Makefile.config convert lst update-ldetect-lst

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


dist:
	git archive --prefix=$(NAME)-$(VERSION)/ HEAD | xz -v -T0 >../$(NAME)-$(VERSION).tar.xz
	$(info $(shell dirname $$PWD)/$(NAME)-$(VERSION).tar.xz is ready)

# Makefile ends here
