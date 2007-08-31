include ../Makefile.config

FILES=dkms-modules.alias dkms-modules.description

build: 
	./merge_dkms_info.pl

install: $(FILES)
	mkdir -p $(dir)
	install -m 644 $(FILES) $(dir)
