project = ldetect-lst
prefix = /usr
datadir = $(prefix)/share
dir = $(datadir)/$(project)

build: CardsNames

clean:
	rm -f *~ CardsNames

CardsNames: Cards+ Cards2CardsNames.pl
	./Cards2CardsNames.pl $< > $@

install: build
	install -d $(dir)
	(echo "# !! The original version is available in CVS at" ; \
         echo "# export CVSROOT=:pserver:anoncvs@cvs.mandrakesoft.com:/home/cvs/cooker" ; \
	 echo "# cvs login    (password ``cvs'')" ; \
         echo "# cvs checkout soft/$(project)" ; \
	 echo "#   or" ; \
         echo "# export CVSROOT=:ext:LOGIN@cvs.mandrakesoft.com:/home/cvs/cooker" ; \
         echo "# export CVS_RSH=ssh" ; \
         echo "# cvs checkout soft/$(project)" ; \
	 cat pcitable \
	) > $(dir)/pcitable

	install -m 644 Cards+ CardsNames MonitorsDB isdn.db $(dir)

rpm: clean $(RPM)
	(echo "# !! DON'T MODIFY HERE, MODIFY IN THE CVS !!" ; \
         cat $(project).spec \
        ) > $(RPM)/SPECS/$(project).spec

	(cd .. ; tar cfj $(RPM)/SOURCES/$(project).tar.bz2 $(project))
	rpm -ba --clean --rmsource --rmspec $(RPM)/SPECS/$(project).spec
