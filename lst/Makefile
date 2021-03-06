include ../Makefile.config

ARCH := $(patsubst i%86,i386,$(shell uname -m))
ARCH := $(patsubst sparc%,sparc,$(ARCH))

TABLES1 = pcitable usbtable
TABLES2 = isatable pcmciatable dmitable
TABLES3 = ScannerDB.gz
TABLES4 = scannerconfigs
TABLES = $(TABLES1) $(TABLES2)
TMP_TABLES1 = $(TABLES1:%=%.tmp)
TMP_TABLES2 = $(TABLES2:%=%.tmp)
TMP_TABLES  = $(TABLES:%=%.tmp)

build: preferred-modules.alias

update-ids: new-usb-ids new-pci-ids new-oui-txt

clean:
	rm -f *~ *.tmp ScannerDB.gz preferred-modules.alias fallback-modules.alias

check: 
	@../convert/merge2pcitable.pl pcitable pcitable.x86_64 pcitable.x86_64 > .pcitable
	@diff -u pcitable.x86_64 .pcitable
	@../convert/merge2pcitable.pl pcitable pcitable pcitable > .pcitable
	@diff -u pcitable .pcitable
	@../convert/merge2pcitable.pl pcitable usbtable usbtable > .usbtable
	@LC_ALL=C.iso-8859-1 sed -e 's!\s"[^"]*"$$!!' < usbtable > .usbtable2
	@diff -u .usbtable2 .usbtable
	@cd ../convert; ./verify_Cards.pl
	@rm -f .pcitable .usbtable*

fallback-modules.alias:
	cp `ls -tr /lib/modules/*/modules.alias | tail -1` fallback-modules.alias

preferred-modules.alias: hardcoded-modules.alias fallback-modules.alias
	@../convert/uniquify-modalias.pl > $@ 2>undecided.alias
	@cat hardcoded-modules.alias >> $@

$(TMP_TABLES1): %.tmp: %
	../convert/merge2pcitable.pl pcitable $< $<.$(ARCH) > $@

$(TMP_TABLES2): %.tmp: %
	cp -f $< $@

$(TABLES3):
	gzip -vc9 ScannerDB > ScannerDB.gz

new-usb-ids:
	@curl --compressed -O http://www.linux-usb.org/usb.ids

new-pci-ids:
	@curl --compressed -O http://pciids.sourceforge.net/pci.ids

new-oui-txt:
	@curl --compressed -O http://standards-oui.ieee.org/oui.txt

install: $(TMP_TABLES) $(TABLES3)
	for i in $(TABLES); do \
	mkdir -p $(dir)/$$i.d ; \
	(echo "# This file was created:" `date '+%Y-%m-%d %H:%M:%S (%z)'` ; \
	 echo "# !! The latest version is available via GIT at" ; \
	 echo "# https://abf.rosalinux.ru/omv_software/ldetect-lst" ; \
	 cat $$i.tmp \
	) > $(dir)/$$i.d/90default.lst; done

	gzip -9 $(dir)/{pcitable,usbtable,dmitable}.d/90default.lst

	install -m 644 ScannerDB.gz scannerconfigs Cards+ MonitorsDB isdn.db $(dir)
	# make MonitorDB looks fine for XFdrake (b/c of sync with RH):
	perl -pi -e 's!^Generic CRT Display; Monitor !Generic; !; s!Generic LCD Display; LCD Panel !Generic; Flat Panel !' $(dir)/MonitorsDB

	install -m 644 fallback-modules.alias $(dir)/fallback-modules.alias
	install -D -m 644 preferred-modules.alias $(slibdir)/module-init-tools/ldetect-lst-modules.alias
	install -D -m 644 oui.txt usb.ids pci.ids $(prefix)/share
	mkdir -p $(prefix)/share/misc
	install -D -m 644 pnp.ids $(prefix)/share/misc
