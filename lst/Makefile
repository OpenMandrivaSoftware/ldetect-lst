include ../Makefile.config


build: CardsNames

clean:
	rm -f *~ CardsNames

CardsNames: Cards+ ../convert/Cards2CardsNames.pl
	rm -f $@
	../convert/Cards2CardsNames.pl $< > $@
	chmod a-w $@


install:
	for i in pcitable pcmciatable usbtable; do \
	(echo "# !! The original version is available in CVS at" ; \
         echo "# export CVSROOT=:pserver:anoncvs@cvs.mandrakesoft.com:/home/cvs/cooker" ; \
	 echo "# cvs login    (password \`\`cvs'')" ; \
         echo "# cvs checkout soft/$(project)" ; \
	 echo "#   or" ; \
         echo "# export CVSROOT=:ext:LOGIN@cvs.mandrakesoft.com:/home/cvs/cooker" ; \
         echo "# export CVS_RSH=ssh" ; \
         echo "# cvs checkout soft/$(project)" ; \
	 cat $$i \
	) > $(dir)/$$i; done

	install -m 644 Cards+ CardsNames MonitorsDB isdn.db $(dir)
