%define name ldetect-lst
%define version 0.1.8
%define release 10mdk

Name: %{name}
Version: %{version}
Release: %{release}
Summary: Hardware list for the light detection library
URL: http://cvs.mandrakesoft.com/cgi-bin/cvsweb.cgi/soft/ldetect-lst/
Source: %{name}-%{version}.tar.bz2
Group: System/Libraries
BuildRoot: %{_tmppath}/%{name}-buildroot
License: GPL
Prefix: %{_prefix}
PreReq: perl-base
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
%setup -q

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
* Mon Sep 22 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 0.1.8-10mdk
- nforce3 nvnet

* Mon Sep 22 2003 Nicolas Planel <nplanel@mandrakesoft.com> 0.1.8-9mdk
- some ATI Radeon card are not working with fglrx.

* Fri Sep 19 2003 Thierry Vignaud <tvignaud@mandrakesoft.com> 0.1.8-8mdk
- fix #5479

* Thu Sep 18 2003 Thierry Vignaud <tvignaud@mandrakesoft.com> 0.1.8-7mdk
- fix usbtable
- reference two more Sagem Fast 800
- reuse snd-intel8x0 for SIS 7012 (fixed in last kernel)

* Wed Sep 17 2003 Thierry Vignaud <tvignaud@mandrakesoft.com> 0.1.8-6mdk
- use right driver for ali sound card (#2203)

* Fri Sep 12 2003 Frederic Lepied <flepied@mandrakesoft.com> 0.1.8-5mdk
- added Omnikey Cardman ids

* Wed Sep 10 2003 Thierry Vignaud <tvignaud@mandrakesoft.com> 0.1.8-4mdk
- added DRIVER2 fglrx support (francois, nicolas)
- merge with kernel modules maps (pixel)
- one more usb device (Stefan Siegel)
- update scanner database for SANE 1.0.12 (till)

* Sun Sep  7 2003 Thierry Vignaud <tvignaud@mandrakesoft.com> 0.1.8-3mdk
- fix #1837: handle acx100_pci
- support more monitors (#4989, ...)
- fix some isdn usb adatators description (Steffen Barszus)
- now Mach64 cards use Utah GLX in experimental mode. (fpons)

* Fri Aug 29 2003 Thierry Vignaud <tvignaud@mandrakesoft.com> 0.1.8-2mdk
- add 3 more monitors (Bryan Whitehead)
- fix 1 cardbus controller (guillaume)
- manage one more gefore card and one more sound card
- use typhoon instead of 3c990 & 3c990fx have die (juan)

* Thu Aug 14 2003 Pixel <pixel@mandrakesoft.com> 0.1.8-1mdk
- pcitable
  o merge with modules.pcimap from kernel 2.4.22.0.3mdk-1-1mdk
  o update with pci.ids 2003-08-13 10:00:05 (pciutils-2.1.11-4mdk)
  o merge with redhat's hwdata-0.89-1.1
- MonitorsDB
  o merge with redhat's hwdata-0.89-1.1

* Tue Aug 12 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 0.1.7-17mdk
- Use "pdc-ultra" for Promise SATA150 Controllers
- Eicon cards fixes (Steffen Barszus through Pixel)
- i810 audio fixes (adelorbeau)
- XF 4.3 now add DRI for Radeon 8500 cards. (fpons)

* Thu Jul 24 2003 Thierry Vignaud <tvignaud@mandrakesoft.com> 0.1.7-16mdk
- fix incorrect driver for Envy24HT (#4257 : Eric Fernandez)
- fix one phillips saa7146 card module (Steffen Barszus)
- describe one unknown bcm card (Alastair Wiggins)

* Fri Jun 27 2003 Nicolas Planel <nplanel@mandrakesoft.com> 0.1.7-15mdk
- Add new ICH5 ID
- 3com 3c940
- Ati Radeon 9800 (ID but not declared as Card:Radeon)
- new sis ohci1394 ID (gc)

* Wed May 28 2003 Thierry Vignaud <tvignaud@mandrakesoft.com> 0.1.7-14mdk
- handle dxr3/hollywood plus cards (frederic crozat)
- manage two previously unmanaged isdn cards (Steffen Barszus)
- add one more LG Flatron monitor (Benjamin Pflugmann)
- fix #1607, #2017
- fix #2255 : add support for three more monitors (two futura and one
  sun)
- prevent freeze (#3793)
- fix #3759 (wrong refresh rate)
- fix #3915: do not list anymore 'Lucent Microelectronics Venus Modem"
  as a winmodem (poulpy)

* Sun Apr  6 2003 Pixel <pixel@mandrakesoft.com> 0.1.7-13mdk
- don't use cat(1) in update-ldetect-lst (fix bug #3678)

* Fri Mar 28 2003 Frederic Lepied <flepied@mandrakesoft.com> 0.1.7-12mdk
- activated 3D on i830, i845, i85x and i865

* Tue Mar 25 2003 Frederic Lepied <flepied@mandrakesoft.com> 0.1.7-11mdk
- Correction for the intel sound card (Arnaud)

* Thu Mar 20 2003 Pixel <pixel@mandrakesoft.com> 0.1.7-10mdk
- change the module of an intel sound card from i810_rng to i801_audio

* Wed Mar 12 2003 Pixel <pixel@mandrakesoft.com> 0.1.7-9mdk
- add a MemoryStick reader and a usb floppy drive from ghibo

* Mon Mar 10 2003 Frederic Lepied <flepied@mandrakesoft.com> 0.1.7-8mdk
- NForce1 video works with nv driver now
- NForce2 net => nvnet

* Thu Mar  6 2003 Thierry Vignaud <tvignaud@mandrakesoft.com> 0.1.7-7mdk
- fix webcam description in harddrake2

* Wed Mar  5 2003 Frederic Lepied <flepied@mandrakesoft.com> 0.1.7-6mdk
- usbtable: tagged hisax_st5481 as ISDN
- pcitable: integrated NVidia ids from XFree 4.3
- add back 3c90x for some ids (Arnaud)

* Fri Feb 28 2003 François Pons <fpons@mandrakesoft.com> 0.1.7-5mdk
- added LT:www.linmodems.org reference to supported ltmodem.

* Thu Feb 27 2003 Pixel <pixel@mandrakesoft.com> 0.1.7-4mdk
- updated pcitable (pci.ids, redhat pcitable, modules.pcimap, http://www.yourvote.com/pci/vendors.txt)

* Sun Feb 16 2003 Till Kamppeter <till@mandrakesoft.com> 0.1.7-3mdk
- Updated ScannerDB and scannerconfigs to include also the third-party
  SANE drivers.

* Thu Feb 13 2003 Thierry Vignaud <tvignaud@mandrakesoft.com> 0.1.7-2mdk
- Restructured and updated ScannerDB for scannerdrake (till)

* Wed Feb 12 2003 Frederic Lepied <flepied@mandrakesoft.com> 0.1.7-1mdk
- added ids for some Intel cards

* Tue Jan 28 2003 Thierry Vignaud <tvignaud@mandrakesoft.com> 0.1.6-1mdk
- fix doble sound card detection on nforce2 motherboards
- add various monitors & pci devices (cooker communauty)
- fix #730 (pixel)

* Wed Jan 22 2003 Pixel <pixel@mandrakesoft.com> 0.1.5-3mdk
- use option ForceInit for Savage/IX-MV (see bug #730)

* Wed Jan 22 2003 Pixel <pixel@mandrakesoft.com> 0.1.5-2mdk
- add a mouse in usbtable

* Sun Jan 12 2003 Pixel <pixel@mandrakesoft.com> 0.1.5-1mdk
  o lst/pcitable:
  - merge with modules.pcimap from kernel 2.4.21.pre2.1mdk-1-1mdk
  - merge with http://www.yourvote.com/pci/vendors.txt
  - merge with pci.ids
  - merge with redhat's hwdata 0.62
    (Radeon 9000, Radeon Mobility 9000 and Radeon 9700 use "Card:ATI Radeon"
    until someone finds they need a special entry in Cards+ (as for redhat, they
    specify the CHIPSET, why?))
  o lst/usbtable:
  - merge with usb.ids,v 1.111 
  - merge with modules.usbmap from kernel 2.4.21.pre2.1mdk-1-1mdk

* Mon Oct 21 2002 Frederic Lepied <flepied@mandrakesoft.com> 0.1.4-19mdk
 o lst/pcitable: added missing savage id
 o lst/usbtable: add support for usb video devices (Florent Beranger)
 o lst/ScannerDB: fix some Hewlett-Packard scanner from niash backend (Yves Duret)
 o lst/pcitable: move HSF/HCF modems module from "unknown" to "Bad:www.linmodems.org" (Damien)

* Tue Sep 17 2002 François Pons <fpons@mandrakesoft.com> 0.1.4-18mdk
- fix a Matrox G450 DualHead not seen as dual head.

* Thu Sep 12 2002 Damien Chaumette <dchaumette@mandrakesoft.com> 0.1.4-17mdk
- fix some isdn cards module syntax to "ISDN:module_name"

* Thu Sep 05 2002 François Pons <fpons@mandrakesoft.com> 0.1.4-16mdk
- fix for GeForce NV25 not working with nv driver (use fbdev or nvidia).

* Thu Sep  5 2002 Guillaume Cottenceau <gc@mandrakesoft.com> 0.1.4-15mdk
- snapshot for latest ieee1394 cards

* Thu Aug 29 2002 Pixel <pixel@mandrakesoft.com> 0.1.4-14mdk
- add "Removable:floppy", "Removable:memory_card", "Removable:camera"

* Tue Aug 27 2002 Pixel <pixel@mandrakesoft.com> 0.1.4-13mdk
- fix syntax error in usbtable (and prevent this to happen again)

* Mon Aug 26 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 0.1.4-12mdk
- add lots of new devices to hardware db

* Thu Aug 22 2002 Pixel <pixel@mandrakesoft.com> 0.1.4-11mdk
- use "Mouse:USB|Microsoft Explorer" for those mice

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

