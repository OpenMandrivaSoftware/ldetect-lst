version = 0.1.0

project = ldetect-lst
prefix = /usr
datadir = $(prefix)/share
dir = $(datadir)/$(project)

build:

clean:
	rm -f *~

install: build
	install -d $(dir)
	install -m 644 pcitable $(dir)


rpm: clean $(RPM)
	(echo "# !! DON'T MODIFY HERE, MODIFY IN THE CVS !!" ; \
	 echo "%define version $(version)" ; \
         cat $(project).spec \
        ) > $(RPM)/SPECS/$(project).spec

	(cd .. ; tar cfj $(RPM)/SOURCES/$(project).tar.bz2 $(project))
	rpm -ba --clean --rmsource --rmspec $(RPM)/SPECS/$(project).spec
