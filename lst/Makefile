include ../Makefile.config

ARCH := $(patsubst i%86,i386,$(shell uname -m))
ARCH := $(patsubst sparc%,sparc,$(ARCH))

TABLES1 = pcitable usbtable
TABLES2 = isatable pcmciatable
TABLES3 = ScannerDB
TABLES = $(TABLES1) $(TABLES2) $(TABLES3)
TMP_TABLES1 = $(TABLES1:%=%.tmp)
TMP_TABLES2 = $(TABLES2:%=%.tmp)
TMP_TABLES  = $(TABLES:%=%.tmp)

build: CardsNames

clean:
	rm -f *~ CardsNames *.tmp ScannerDB.gz

CardsNames: Cards+ ../convert/Cards2CardsNames.pl
	rm -f $@
	../convert/Cards2CardsNames.pl $< > $@
	chmod a-w $@

$(TMP_TABLES1): %.tmp: %
	../convert/merge2pcitable.pl pcitable $< $<.$(ARCH) > $@

$(TMP_TABLES2): %.tmp: %
	cp -f $< $@

$(TMP_TABLES3): %.tmp: %
	gzip -vc9 ScannerDB > ScannerDB.gz

install: $(TMP_TABLES)
	for i in $(TABLES); do \
	(echo "# !! The original version is available in CVS at" ; \
         echo "# export CVSROOT=:pserver:anoncvs@cvs.mandrakesoft.com:/home/cvs/cooker" ; \
	 echo "# cvs login    (password \`\`cvs'')" ; \
         echo "# cvs checkout soft/$(project)" ; \
	 echo "#   or" ; \
         echo "# export CVSROOT=:ext:LOGIN@cvs.mandrakesoft.com:/home/cvs/cooker" ; \
         echo "# export CVS_RSH=ssh" ; \
         echo "# cvs checkout soft/$(project)" ; \
	 cat $$i.tmp \
	) > $(dir)/$$i; done

	install -m 644 ScannerDB.gz Cards+ CardsNames MonitorsDB isdn.db $(dir)
