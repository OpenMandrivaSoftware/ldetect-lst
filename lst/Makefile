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

build: CardsNames

clean:
	rm -f *~ CardsNames *.tmp ScannerDB.gz

check:
	@../convert/merge2pcitable.pl pcitable pcitable pcitable > /dev/null
	@../convert/merge2pcitable.pl pcitable usbtable usbtable > /dev/null

CardsNames: Cards+ ../convert/Cards2CardsNames.pl
	rm -f $@
	../convert/Cards2CardsNames.pl $< > $@
	chmod a-w $@

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

	install -m 644 ScannerDB.gz Cards+ CardsNames MonitorsDB isdn.db $(dir)
