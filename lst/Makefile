include ../Makefile.config

ARCH := $(patsubst i%86,i386,$(shell uname -m))
ARCH := $(patsubst sparc%,sparc,$(ARCH))

TABLES1 = pcitable usbtable
TABLES2 = isatable pcmciatable
TABLES3 = ScannerDB.gz
TABLES = $(TABLES1) $(TABLES2)
TMP_TABLES1 = $(TABLES1:%=%.tmp)
TMP_TABLES2 = $(TABLES2:%=%.tmp)
TMP_TABLES  = $(TABLES:%=%.tmp)

build: 

clean:
	rm -f *~ *.tmp ScannerDB.gz

check:
	@../convert/merge2pcitable.pl pcitable pcitable pcitable > .pcitable
	@diff -u pcitable .pcitable
	@../convert/merge2pcitable.pl pcitable usbtable usbtable > .usbtable
	@diff -u usbtable .usbtable
	@cd ../convert; ./verify_Cards.pl
	@rm -f .pcitable .usbtable

$(TMP_TABLES1): %.tmp: %
	../convert/merge2pcitable.pl pcitable $< $<.$(ARCH) > $@

$(TMP_TABLES2): %.tmp: %
	cp -f $< $@

$(TABLES3):
	gzip -vc9 ScannerDB > ScannerDB.gz

install: $(TMP_TABLES) $(TABLES3)
	for i in $(TABLES); do \
	mkdir -p $(dir)/$$i.d ; \
	(echo "# !! The original version is available in CVS at" ; \
         echo "# export CVS_RSH=ssh" ; \
         echo "# export CVSROOT=:ext:anoncvs@cvs.mandrakesoft.com:/cooker" ; \
         echo "# cvs checkout soft/$(project)    (password \`\`cvs'')" ; \
	 cat $$i.tmp \
	) > $(dir)/$$i.d/90default.lst; done

	install -m 644 ScannerDB.gz Cards+ MonitorsDB isdn.db $(dir)
