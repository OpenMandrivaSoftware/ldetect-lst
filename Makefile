include Makefile.config

build: 
	make -C lst build

clean:
	rm -f *~
	make -C lst clean

install: build
	install -d $(bindir) $(sbindir) $(dir)
	make -C lst install
	install update-ldetect-lst $(sbindir)
	install convert/merge2pcitable.pl $(bindir)

rpm: clean $(RPM)
	(echo "# !! DON'T MODIFY HERE, MODIFY IN THE CVS !!" ; \
         cat $(project).spec \
        ) > $(RPM)/SPECS/$(project).spec

	(cd .. ; tar cfj $(RPM)/SOURCES/$(project).tar.bz2 $(project))
	rpm -ba --clean --rmsource --rmspec $(RPM)/SPECS/$(project).spec
