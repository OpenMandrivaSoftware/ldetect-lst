%define name ldetect-lst
%define version 0.1.4
%define release 10mdk

Name: %{name}
Version: %{version}
Release: %{release}
Summary: Hardware list for the light detection library
URL: http://cvs.mandrakesoft.com/cgi-bin/cvsweb.cgi/soft/ldetect-lst/
Source: %{name}.tar.bz2
Group: System/Libraries
BuildRoot: %{_tmppath}/%{name}-buildroot
License: GPL
Prefix: %{_prefix}
BuildRequires: perl-MDK-Common
Provides: hwdata

%package devel
Summary: Devel for ldetect-lst
Group: Development/Perl
Requires: ldetect-lst = %{version}

%description
The hardware device lists provided by this package are used as lookup 
table to get hardware autodetection

%description devel
see ldetect-lst

%prep
%setup -q -n %{name}

%build
%make

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall

%clean
rm -rf $RPM_BUILD_ROOT

# trigger is needed to upgrade from a package having
# /usr/share/ldetect-lst/pcitable in the package to the new scheme
%triggerpostun -- %{name}
if [ -x /usr/sbin/update-ldetect-lst ]; then
  /usr/sbin/update-ldetect-lst
fi

%preun -p "/usr/sbin/update-ldetect-lst --clean"

%post -p /usr/sbin/update-ldetect-lst

%files
%defattr(-,root,root)
%doc ChangeLog
%{_datadir}/%{name}
%{_sbindir}/*

%files devel
%defattr(-,root,root)
%doc convert/README.pcitable
%{_bindir}/*

%changelog
* Tue Aug 20 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 0.1.4-10mdk
- homogenize seiko/epson into epson for scanner owners

* Tue Aug 20 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 0.1.4-9mdk
- 2 unknown cards were in fact "Media Vision" (reported by Danny
  Tholen)
- till:
	o add new Epson models to scanner database for scannerdrake :
	  Epson Perfection 660, 1660 Photo, 2400 Photo Added photo card
	  readers of Epson Stylus Photo 915/915
	o alter description of USB vendor 0x04b8 model 0x0005 to "Epson
	  Corp.|USB Printer", nearly all Epson printers have this ID
	  pair, so no program should report "Epson Stylus Color 760"
	  then.

* Sat Aug 17 2002 Pixel <pixel@mandrakesoft.com> 0.1.4-8mdk
- G550 *are* DualHead

* Tue Aug 13 2002 Pixel <pixel@mandrakesoft.com> 0.1.4-7mdk
- add entry "Intel 845" using driver i810 (fix bug #60)
- use accel for SiS 86C326 (tested on a box here)

* Tue Aug  6 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 0.1.4-6mdk
- lst/pcitable: fix vendor for a megaraid (s/Dell/AMI/)
- lst/pcitable: bcm5700 is story.  Great live to tg3
- lst/Cards+: add XaaNoPixmapCache for i815 too (per Mattias Dahlberg request)
- lst/pcitable: switch Danny Tholen sound card from oss to alsa

* Thu Aug  1 2002 Pixel <pixel@mandrakesoft.com> 0.1.4-5mdk
- Cards+ & pcitable: add "ATI Rage 128 TVout" with flag FB_TVOUT

* Sun Jul 28 2002 Pixel <pixel@mandrakesoft.com> 0.1.4-4mdk
- drop CardsNames (not used anymore by drakx)
- Cards+: add Option "XaaNoPixmapCache" for i810 as suggested on cooker.
          to be removed when the kernel works ok
- Cards+ (and pcitable): to cleanup the tree in XFdrake
  - remove "Spacewalker HOT", "Octek", "Creative Blaster Exxtreme",
    "Atrend", "ATrend", "SPEA", "Spider", "Actix", "Canopus", "Cardex"
    entries
  - remove "Generic VGA compatible" and entries using it
  - remove "Unsupported VGA compatible"
  - replace "SMI" by "Silicon Motion"
  - replace "ELSA" by "Elsa"
  - replace "LeadTek" by "Leadtek"

* Sun Jul 21 2002 Pixel <pixel@mandrakesoft.com> 0.1.4-3mdk
- pcitable
  - bttc -> bttv (typo fix)
  - snd-cs461x -> snd-cs46xx (since snd-cs461x doesn't exist)
  - fix many typos (please use make test!!)
  - all new rh id're merged (titi)
  - new eepro100 IDs (nplanel)
  - new Promise 20276 (nplanel)

* Wed Jul 17 2002 Pixel <pixel@mandrakesoft.com> 0.1.4-2mdk
- pcitable: update with www.begent.co.uk/pcids.htm
  especially interesting are the G200,G400,G450 multi head categorisation
- Cards+: new entries for DualHead & QuadHead matrox

* Wed Jul 17 2002 Pixel <pixel@mandrakesoft.com> 0.1.4-1mdk
- Cards+ + pcitable:
  - add "ATI Radeon 8500" with no DRI_GLX
  - add "SiS 6326 no_accel" with Option "no_accel"
  - add "NeoMagic 128XD" with special XaaNoScanline* options
  - add "NeoMagic MagicMedia 256XL+" with Option "sw_cursor"
  - add NEEDVIDEORAM for cards corresponding to /86c368|S3 Inc|Tseng.*ET6\d00/
    (hoping it will work: since the regexp was broken, it was never done.
     (it was applied on the module field of pcitable, instead of the description))
  - remove CHIPSET except for cards which had needChipset
  - add UTAH_GLX, UTAH_GLX_EXPERIMENTAL 
    (which card have them come from Xconfigurator.pm)
  - add BAD_FB_RESTORE & BAD_FB_RESTORE_XF3

* Fri Jun 21 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 0.1.3-9mdk
- Add nForce things from Damien.
- s/de4x5/tulip/ thanks to juan
- Restore via8233 sound support (tv)
- fpons: added various HP hardware.

* Fri Mar  1 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 0.1.3-8mdk
- fpons: fixed doubles and typo.
- Thierry:
	* 1 new card
	* 3 old card that hadn't any modules have one now
	* fix one typo (s!snd-es1938!snd-card-es1938)
	* merge all isapnp ids from alsa

* Fri Mar  1 2002 Pixel <pixel@mandrakesoft.com> 0.1.3-7mdk
- various s3 changes (Erwan)
- Thierry:
	* fix typos
	* add 17 new pci sound & TV cards
	* add a lot of new sound isapnp cards
	* update some descriptions
	* resort the {pci,isa} db

* Thu Feb 28 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 0.1.3-6mdk
- yduret sucks and has forgotten to commit in cvs his package uploae
- Thierry Vignaud:
	* fix 10 incorrect TV card names
	* add 15 new TV cards
	* add ChangeLog
- Pixel:
	* add 3 usb mice
	* s/53c7,8xx/sym53c8xx/
- Guillaume:
	* remove duplicate entry (quintela sucks)
	* be sure to have \t everywhere
	* three other O2 Micro CardBus controllers
- Yves Duret:
	* fix Connectix entries (qcam server)
	* added support for Hewlett-Packard OfficeJet series
	* fix Bell and Howell entries
	* sync with scanner.{c,h} version 0.47 from david nelson
	* sync with sane 1.0.7
	* ci before big merge
	* fix HP scanner entry
	* added some HP models
	* added more snapscan escanners + some add in usbtable (kbd..)
	* mustek_pp updated
	* one more HP escanner..
	* some HP escanners added (but in UNSUPPORTED :(
- François Pons:
	* KYRO uses fbdev instead of vesa.
	* added GD5480 as working under XF 4.2 (Juan)
- Juan Quintela
	*  use new qlogic drivers by default

* Tue Feb 19 2002 Yves Duret <yduret@mandrakesoft.com> 0.1.3-5mdk

- ScannerDB, usbtable updated


* Thu Feb 14 2002 Pixel <pixel@mandrakesoft.com> 0.1.3-4mdk
- add BuildRequires: perl-MDK-Common
- GeForce Integrated use fbdev driver instead of nv (freeze).

* Mon Feb 11 2002 Pixel <pixel@mandrakesoft.com> 0.1.3-3mdk
- fix the comment for accessing the CVS version

* Thu Feb  7 2002 Pixel <pixel@mandrakesoft.com> 0.1.3-2mdk
- upgrading the package should now work... using trigger :-(

* Thu Feb  7 2002 Pixel <pixel@mandrakesoft.com> 0.1.3-1mdk
- allow third party entries (using update-ldetect-lst)

* Tue Feb  5 2002 Pixel <pixel@mandrakesoft.com> 0.1.2-39mdk
- fix usbtable merge with kernel usbmap

* Wed Jan 30 2002 Pixel <pixel@mandrakesoft.com> 0.1.2-38mdk
- replace a de4x5 with tulip

* Mon Jan 28 2002 Pixel <pixel@mandrakesoft.com> 0.1.2-37mdk
- pcitable: merge with redhat's pcitable, XFree86, vendors.txt, modules.pcimap
- usbtable: merge with modules.usbmap, usb.ids

* Fri Jan 25 2002 Pixel <pixel@mandrakesoft.com> 0.1.2-36mdk
- s/ncr53c8xx/sym53c8xx/

* Tue Jan 22 2002 François Pons <fpons@mandrakesoft.com> 0.1.2-35mdk
- added i830 support (Card:Intel 830).
- added Alliance AT25 card support (Card:AT25).
- updated 3DLabs, NeoMagic card not supported by XF 3.3.6.
- fixed typos.

* Sat Jan 12 2002 Pixel <pixel@mandrakesoft.com> 0.1.2-34mdk
- various

* Mon Nov 19 2001 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 0.1.2-33mdk
- Add IBM|ServeRAID-4Lx and IBM|ServeRAID-4Mx PCI IDs
- On IA-64, suggest "qlogicfc" for Q Logic { 2100, 2200 } cards

* Mon Nov 12 2001 Yves Duret <yduret@mandrakesoft.com> 0.1.2-32mdk
- the really big fat heavy ScannerDB update (~320 scanners added)

* Wed Oct 10 2001 Yves Duret <yduret@mandrakesoft.com> 0.1.2-31mdk
- really add ScannerDB (i suck)

* Wed Oct 10 2001 Yves Duret <yduret@mandrakesoft.com> 0.1.2-30mdk
- added ScannerDB
- fix scanner entry in usbtable

* Mon Oct  8 2001 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 0.1.2-29mdk
- Arch-dependent pcitable and usbtable
- On IA-64, suggest "e100" driver for devices = { 0x1229, 0x2449 }

* Tue Oct 02 2001 Yves Duret <yduret@mandrakesoft.com> 0.1.2-28mdk
- fix typo in usb scanner

* Mon Sep 24 2001 Pixel <pixel@mandrakesoft.com> 0.1.2-27mdk
- replace ns558 by emu10k1-gp (Planel Nicolas)

* Fri Sep 21 2001 Francois Pons <fpons@mandrakesoft.com> 0.1.2-26mdk
- added GeForce 3 Integrated (Xbox).

* Thu Sep 20 2001 Guillaume Cottenceau <gc@mandrakesoft.com> 0.1.2-25mdk
- remove (yet again) tulip for some DEC cards, and ensure the bug in
  redhat pcitable won't both us again

* Thu Sep 13 2001 Frederic Lepied <flepied@mandrakesoft.com> 0.1.2-24mdk
- corrected wacom entries to support the PL500 and the Graphire2.

* Wed Sep 12 2001 Frederic Lepied <flepied@mandrakesoft.com> 0.1.2-23mdk
- added matrox G550 pci id

* Wed Sep  5 2001 Pixel <pixel@mandrakesoft.com> 0.1.2-22mdk
- replace AM53C974 with tmscsim

* Wed Sep  5 2001 Pixel <pixel@mandrakesoft.com> 0.1.2-21mdk
- merge with latest redhat pcitable & kernel modules.pcimap

* Thu Aug 30 2001 Pixel <pixel@mandrakesoft.com> 0.1.2-20mdk
- cleanup some bttv
- Matrox Millenium card are supported by XF4 (fpons)

* Wed Aug 29 2001 Frederic Lepied <flepied@mandrakesoft.com> 0.1.2-19mdk
- updated wacom usb entries.

* Tue Aug 21 2001 Pixel <pixel@mandrakesoft.com> 0.1.2-18mdk
- various updates

* Tue Aug 14 2001 Pixel <pixel@mandrakesoft.com> 0.1.2-17mdk
- updated usbtable and pcitable
- added Kyro series and a few other

* Tue Jul 31 2001 Guillaume Cottenceau <gc@mandrakesoft.com> 0.1.2-16mdk
- merge with 2.4.6-5mdk pcitable and usbtable

* Wed Jul  4 2001 François Pons <fpons@mandrakesoft.com> 0.1.2-15mdk
- fixed support for SiS 300.
- synced pcitable and Cards+ with XFree86 4.1.0.
- another people do the following:
- es1370 doesn't work for "Ensoniq|ES1370 [AudioPCI]" (ID 0x12745000)
  replace it by "snd-card-ens1370" wich operates smoothly
- add a new Pinnacle PCTV
- add support for ALS4000

* Thu Jun 14 2001 Pixel <pixel@mandrakesoft.com> 0.1.2-14mdk
- adds some ATI cards

* Tue Apr 10 2001 Frederic Lepied <flepied@mandrakesoft.com> 0.1.2-13mdk
- added GeForce3 and CyberBlade/Xpm entries

* Tue Apr 10 2001 François Pons <fpons@mandrakesoft.com> 0.1.2-12mdk
- added Trident CyberBladeXP.

* Mon Apr  9 2001 Pixel <pixel@mandrakesoft.com> 0.1.2-11mdk
- added some usb stuff

* Sat Mar 24 2001 Pixel <pixel@mandrakesoft.com> 0.1.2-10mdk
- cleaned pcitable

* Fri Mar 23 2001 François Pons <fpons@mandrakesoft.com> 0.1.2-9mdk
- added Tablet:wacom for USB Wacom tablet.

* Wed Mar 21 2001 François Pons <fpons@mandrakesoft.com> 0.1.2-8mdk
- fixed wrong Matrox G450 reference.

* Thu Mar 15 2001 François Pons <fpons@mandrakesoft.com> 0.1.2-7mdk
- updated, removed matrox memory reference.

* Tue Mar 13 2001 Pixel <pixel@mandrakesoft.com> 0.1.2-6mdk
- updated

* Tue Mar  6 2001 Pixel <pixel@mandrakesoft.com> 0.1.2-5mdk
- merge with /lib/modules/2.4.2-7mdk/modules.pcimap, anaconda-7.1-1.200102051925's
pcitable, kudzu-0.92.1-1's pcitable

* Thu Jan 25 2001 Guillaume Cottenceau <gc@mandrakesoft.com> 0.1.2-4mdk
- snd-card-intel8x0 -> i810_audio

* Thu Jan 25 2001 Guillaume Cottenceau <gc@mandrakesoft.com> 0.1.2-3mdk
- snapshot (for pcitable updates)

* Thu Dec 21 2000 Pixel <pixel@mandrakesoft.com> 0.1.2-2mdk
- add ldetect-lst-devel

* Sat Dec 16 2000 Pixel <pixel@mandrakesoft.com> 0.1.2-1mdk
- add usbtable

* Fri Dec 15 2000 Pixel <pixel@mandrakesoft.com> 0.1.1-1mdk
- add Cards+, MonitorsDB, isdn.db

* Fri Dec 15 2000 Pixel <pixel@mandrakesoft.com> 0.1.0-1mdk
- first release

