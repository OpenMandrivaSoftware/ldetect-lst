FILES = xf86PciInfo2pcitable

all: $(FILES) verif

verif:
	./verify_Cards.pl

clean:
	rm -f $(FILES)

xf86PciInfo2pcitable: %: %.c xf86PciInfo.h
	gcc -o $@ $<

#do
# take new xc/programs/Xserver/hw/xfree86/common/xf86PciInfo.h in XFree86-4
# make ; ./xf86PciInfo2pcitable > /tmp/xf_pcitable ; perl rh_pcitable2pcitable /tmp/xf_pcitable ../pcitable
