%define name ldetect-lst
%define version 0.1.56
%define release 1mdk

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
%doc AUTHORS ChangeLog
%{_datadir}/%{name}
%{_sbindir}/*

%files devel
%defattr(-,root,root)
%doc convert/README.pcitable
%{_bindir}/*

%changelog
* Mon Feb  7 2005 Thierry Vignaud <tvignaud@mandrakesoft.com> 0.1.56-1mdk
- add one new ATI graphic card
- add one new Intel graphic card
- add E-Tech/Amigo AMX-CA80U ADSL modem (pablo)
- handle quite a few more Intel & ALI AGP bridges
- handle new vrc4173_cardu PCMCIA driver (from kernel-2.6.11-rc3)
- replace uli526x by tulip driver
- handle new ISDN USB driver hfc4s8s_l1
- fix support for some ISDN drivers in drakconnect (namely c4, divas,
  hysdn and one hisax)
- sync with kernel-2.6.11-rc3

* Wed Feb  2 2005 Thierry Vignaud <tvignaud@mandrakesoft.com> 0.1.55-1mdk
- add 2 new intel sata controllers
- sync with kernel-multimedia-2.6.10-1.mm.9mdk

* Fri Jan 28 2005 Thierry Vignaud <tvignaud@mandrakesoft.com> 0.1.54-1mdk
- add one intel ide controller (from lkml)
- add a new LG monitor (Angelo Naselli)
- add 2 new apple monitors (danny)
- sync with kernel-2.6.11-rc2-mm1

* Tue Jan 25 2005 Thierry Vignaud <tvignaud@mandrakesoft.com> 0.1.53-1mdk
- fix support for SB Live! Value EMU10k1X

* Mon Jan 24 2005 Thierry Vignaud <tvignaud@mandrakesoft.com> 0.1.52-1mdk
- add support for one ATI and two ICH7 SATA controllers
- add a new Samsung monitor (Albert Astals Cid)

* Thu Jan 20 2005 Thierry Vignaud <tvignaud@mandrakesoft.com> 0.1.51-1mdk
- "snd-audigyls" ALSA driver was renamed "snd-ca0106"
- add SATA support for ICH7

* Thu Jan 20 2005 Thierry Vignaud <tvignaud@mandrakesoft.com> 0.1.50-1mdk
- fix conflict between 8139cp and 8139too
- add AC'97 Audio support for Intel ICH7
- add eisa id for Panasonic E70i monitor (neoclust)
- add 2 new monitors (one ADI and one Hyundai) (Neoclust)

* Thu Jan 13 2005 Thierry Vignaud <tvignaud@mandrakesoft.com> 0.1.49-1mdk
- add a new Sony monitor (Neoclust)
- switch a realtek driver (#12982)

* Tue Jan 11 2005 Thierry Vignaud <tvignaud@mandrakesoft.com> 0.1.48-1mdk
- add another zaptel device (Stefan van der Eijk)
- switch from ata_piix to ahci

* Tue Jan 11 2005 Thierry Vignaud <tvignaud@mandrakesoft.com> 0.1.47-1mdk
- list zd1201 driver
- manually merge driver that don't export ids of devices they managed

* Tue Jan 11 2005 Thierry Vignaud <tvignaud@mandrakesoft.com> 0.1.46-1mdk
- sync with ide drivers from 2.6.10-ac8
- add a new Samsung monitor (Albert Astals Cid)
- add 2 zaptel devices (Stefan van der Eijk)

* Mon Jan 10 2005 Thierry Vignaud <tvignaud@mandrakesoft.com> 0.1.45-1mdk
- add a new Philips monitor (Albert Astals Cid)
- add limited/partial support for zaptel
- list ivtv driver

* Mon Jan 10 2005 Thierry Vignaud <tvignaud@mandrakesoft.com> 0.1.44-1mdk
- add a new Lite-On monitor (Berthy)
- add a new Princeton monitor (Thomas Spuhler)
- add a new Sony monitor (Angelo Naselli)

* Fri Jan  7 2005 Thierry Vignaud <tvignaud@mandrakesoft.com> 0.1.43-1mdk
- add a Belinea monitor (Michael Braun)
- add two LG monitors (Neoclust)
- add support for Intel ICH7 sound card

* Fri Jan  7 2005 Thierry Vignaud <tvignaud@mandrakesoft.com> 0.1.42-1mdk
- add a Samsung monitor (Andres Kaaber)

* Fri Jan  7 2005 Thierry Vignaud <tvignaud@mandrakesoft.com> 0.1.41-1mdk
- sync with kernel-2.6.9-1mdk
- add a LG monitor (Andres Kaaber)

* Thu Jan  6 2005 Thierry Vignaud <tvignaud@mandrakesoft.com> 0.1.40-1mdk
- add a new monitor (Marek Laane)
- pcitable: fix wrong driver for a wifi card (#11393)
- usbtable: sync with latest usb.ids

* Wed Jan  5 2005 Thierry Vignaud <tvignaud@mandrakesoft.com> 0.1.39-1mdk
- sync with kernel-2.6.10-mm1
- clean DVB entries
- remove bogus usbcore entries
- solve a few conflicts regarding devices claimed by modules
- fix a wrongly identified card (pixel, #12871)

* Thu Dec 23 2004 Thierry Vignaud <tvignaud@mandrakesoft.com> 0.1.38-1mdk
- add support for Digigram PCXHR sound cards
- fix description of a couple DELL cards and a couple Digigram cards
- sync with kernels 2.6.10-rc3-mm1 and 2.6.8-10-rc3-bk16

* Fri Dec  3 2004 Thierry Vignaud <tvignaud@mandrakesoft.com> 0.1.37-1mdk
- disambiguate names of media devices (eg: DVB vs TV cards)
- update incomplete descriptions from {pci,usb}.ids
- sync i2c with 2.6.10-rc2-mm4
- one extra sound card from pci-26.lst file from debian's
  discover1-data

* Thu Dec  2 2004 Thierry Vignaud <tvignaud@mandrakesoft.com> 0.1.36-1mdk
- sync with debian's discover

* Thu Dec  2 2004 Thierry Vignaud <tvignaud@mandrakesoft.com> 0.1.35-1mdk
- add two new geforce cards and a score of fiber channel cards

* Thu Dec  2 2004 Thierry Vignaud <tvignaud@mandrakesoft.com> 0.1.34-1mdk
- sync with pci.ids, usb.ids, kernel-2.6.9-ac12, kernel-2.6.10-rc2-mm4

* Thu Dec  2 2004 Thierry Vignaud <tvignaud@mandrakesoft.com> 0.1.33-1mdk
- enable DRI on i915 and onMach64 since it is now supported in X.org-6.8.x

* Wed Dec  1 2004 Thierry Vignaud <tvignaud@mandrakesoft.com> 0.1.32-1mdk
- handle Alan Cox's new "voodoo" driver from x.org-6.8.x

* Fri Nov 26 2004 Thierry Vignaud <tvignaud@mandrakesoft.com> 0.1.31-1mdk
- since yenta_socket driver claims to support any pci card whose class
  is PCI_CLASS_BRIDGE_CARDBUS, assign it to all pcmcia/cardbus
  controllers

* Fri Nov 26 2004 Thierry Vignaud <tvignaud@mandrakesoft.com> 0.1.30-1mdk
- handle PCI device IDs set to PCI_ANY_ID in kernel's pcimap:
  o this especially fix PCMCIA support on O2 Micro controllers
  o this also add support for a couple of Adaptec SCSI controllers

* Thu Nov 25 2004 Thierry Vignaud <tvignaud@mandrakesoft.com> 0.1.29-1mdk
- MonitorsDB:
  o update, sync with hwdata-0.148
  o fix a few entry
  o add "Samsung SyncMaster 910N/912N" (pablo)
- pcitable:
  o fill in a few descriptions
  o sync with serial, DVB and SMB Host controllers drivers from
    kernel-2.6.10-rc2-mm3
  o add support for Intel's High Definition Audio Controller
  o sync with ALSA's CVS
- usbtable:
  o sync with usb.ids and with kernel-2.6.8.1.22mdk's usbmap
  o add "Pinnacle Systems, Inc.|Pinnacle Bungee (PAL)" (Stefan Siegel)

* Fri Nov 19 2004 Thierry Vignaud <tvignaud@mandrakesoft.com> 0.1.28-1mdk
- ALI SATA controllers:
  o fill in descriptions
  o fix duplicated entry

* Fri Nov 19 2004 Thierry Vignaud <tvignaud@mandrakesoft.com> 0.1.27-1mdk
- pcitable:
  o sync with:
    * ALSA-1.0.7 as in kernel-2.6.10-rc2-mm1
    * pci.ids from kernel-2.6.10-rc2-mm1
    * userland pci.ids
  o update/fill in ATI sound-cards description from ALSA sound driver
  o add two new controllers from ULI & VIA SATA controllers (from
    bk-sata)
- usbtable: add "Logitech Inc.|QuickCam Communicate" (Stefan Siegel)

* Wed Nov 17 2004 Thierry Vignaud <tvignaud@mandrakesoft.com> 0.1.26-1mdk
- sync with hwdata-0.147
- sync with latest usb.ids
- sync with latest pci.ids

* Wed Nov 17 2004 Thierry Vignaud <tvignaud@mandrakesoft.com> 0.1.25-1mdk
- pcitable:
  o sync with kernel-tmb-2.6.7-2.tmb.6mdk
  o sync with 2.8.10-rc1-mm5's libata & serial driver
  o fill driver field for EIDE/ATA controllers
  o s/3c90x/3c59x/ since the former is dead for years
  o fix a couble of bogus entries
	* lst/pcitable: sync with 2.8.10-rc1-mm5's 

* Wed Nov 10 2004 Thierry Vignaud <tvignaud@mandrakesoft.com> 0.1.24-1mdk
- disambiguate media devices (eg: TV cards vs SAT cards)
- add I2C modules
- workaround sound on some VIA VT8233 (#10859)
- sync with pci.ids, hwdata-0.145 and kernel-2.6.8.1.21mdk
- use yenta_socket for PCI7420 CardBus Controller

* Thu Oct 28 2004 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 0.1.23-1mdk
- add Philips Semiconductors DSL card (blino)
- use new megaraid_mbox for the following cards:
  + 0x1000 0x0408  "megaraid_mbox" "LSI Logic / Symbios Logic|MegaRAID"
  + 0x1000 0x0409  "megaraid_mbox" "LSI Logic / Symbios Logic|MegaRAID"
  + 0x1028 0x0013  "megaraid_mbox" "Dell|PowerEdge Expandable RAID controller 4"

* Thu Oct 28 2004 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 0.1.22-1mdk
- add nVidia Quadro FX 1100 card ID
- add support for FreeBox v4 via USB link (buggy device make kernel
  failed to map usbnet to it) [ Thierry Vignaud ]

* Thu Oct 21 2004 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 0.1.21-1mdk
- add nVidia Quadro FX 3400 PCI-Express card ID

* Mon Oct 11 2004 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 0.1.20-1mdk
- speculatively use aic79xx for Adaptec ASC-39320[AB] cards

* Mon Oct 11 2004 Thierry Vignaud <tvignaud@mandrakesoft.com> 0.1.19-1mdk
- fix sound on one ensoniq sound card

* Tue Sep 28 2004 Frederic Lepied <flepied@mandrakesoft.com> 0.1.18-1mdk
- added ath_pci entries

* Fri Sep 24 2004 Frederic Lepied <flepied@mandrakesoft.com> 0.1.17-1mdk
- lst/usbtable: merged kernel 2.6.8.1.10mdk entries to be able to
 list them during install.
- lst/pcitable: o update ATI pciids (Nicolas)
                o add new NVidia 6800 (Nicolas)

* Tue Sep 14 2004 Thierry Vignaud <tvignaud@mandrakesoft.com> 0.1.16-6mdk
- fix some CAPI entries (blino)

* Tue Sep 14 2004 Thierry Vignaud <tvignaud@mandrakesoft.com> 0.1.16-5mdk
- add support for xDSL over CAPI (eg: AVM cards) (blino)
- add some Apple hardware (Christiaan Welvaar)
- sync pcitable with kernel-2.6.8.1.10mdk

* Wed Sep  8 2004 Frederic Lepied <flepied@mandrakesoft.com> 0.1.16-4mdk
 o pcitable:
	* added entries for slamr and rt2500
	* added entries for IPW2200
	* Intel Corporation => Intel Corp.
 o usbtable:
	* added slusb
	* added driver for NetGear MA111
	* put newhidups driver for MGE UPS entries.
	* fixed wacom entries.

* Tue Aug 31 2004 Thierry Vignaud <tvignaud@mandrakesoft.com> 0.1.16-3mdk
- pcitable:
  o sync with kernel-2.6.8.1.5mdk
  o switch one nForce2 from OSS to ALSA
  o in 2.6.x kernel, pwcd was splited between pcwd_pci and pcwd_usb
  o in both 2.4.x and 2.6.x kernels:
    * 3c359 replaced 3c559
    * donauboe replaced toshoboe
    * hw_random replaced both amd7xx_tco, amd768_rng and i810_rngb
    * pc300 replaced pc300too
    * tmspci replaced sktr
    * tulip replaced tulip_old (#10965)
  o remove bogus 0xffff 0xffff entry
  o introduce bt878
  o introduce sata_sx4 instead of sata_promise for one controller
  o fix a few wrong entries (according to kernel's pcimap):
    * one s/dmfe/tulip/
    * one s/qla2200/qla2100/
    * one s/tulip/de2104x/
    * one s/yenta_socket/i82092/
    * one s/yenta_socket/pd6729/

* Fri Aug 27 2004 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 0.1.16-2mdk
- use 3w-9xxx for 3ware 9XXX-series ATA-RAID

* Thu Aug 26 2004 Thierry Vignaud <tvignaud@mandrakesoft.com> 0.1.16-1mdk
- usbtable: sync with kernel-2.6.8.1.1mdk (kernel-2.6.8.1.3mdk equals
  1mdk regarding pcitable & usbtable)
- switch Intel/ICH6 sound card from OSS to ALSA b/c of sound recording
  issues

* Wed Aug 18 2004 Thierry Vignaud <tvignaud@mandrakesoft.com> 0.1.15-1mdk
- sync pcitable with kernel-2.6.8.1.1mdk
- fill some empty strings (Erwan Velu)
- add support for several ati & nvidia gfx cards (greg)

* Wed Aug  4 2004 Thierry Vignaud <tvignaud@mandrakesoft.com> 0.1.14-1mdk
- usbtable: 
  o sync with kernel-2.6.8-0.rc2.2mdk
  o merge descriptions with usbutils

* Tue Aug  3 2004 Thierry Vignaud <tvignaud@mandrakesoft.com> 0.1.13-1mdk
- pcitable: 
  o merge with kernel-2.6.8-0.rc2.2mdk
  o merge with pciids.sf.net
  o update missing descriptions

* Thu Jul 29 2004 Frederic Lepied <flepied@mandrakesoft.com> 0.1.12-1mdk
- usbtable: updated descriptions

* Mon Jul 26 2004 Thierry Vignaud <tvignaud@mandrakesoft.com> 0.1.11-1mdk
- monitor DB:
  o add a Princeton monitor (#2633)
  o add a LCD monitor (Sylvain Vignaud)
  o fix a typo
  o sync with rh's hwdata-0.123 (new monitors, ...)
  o increase a few DELL monitors frequency ranges (from hwdata-0.123)
  o remove a few old duplicated entries
- use b44 rather than bcm4400 (nicolas, #9742)
- use tg3 rather than bcm5700  (nicolas, #9742)
- add NVIDIA PCI-express 5750 Card Add Matrox P750 Add NVIDIA GO 5600 (greg)
- fix #8295 (no ADSL over Accton Ethernet card)

* Tue Jun 15 2004 Thierry Vignaud <tvignaud@mandrakesoft.com> 0.1.10-1mdk
- add madwifi_pci for 16c8 0013 (arnaud)
- add module yenta_socket for the 0x1217 0x7114 (arnaud)
- add slamr (slmodem) for 10b9 5457 (arnaud)
- adding usb modules for dell PE750 (erwan)
- CB1410 Cardbus Controller works with yenta_socket (arnaud)
- default to tg3 instead of bcm5700 for a few chip names (arnaud)
- list some cardbus controlers from pciids.sourceforge.net (arnaud)
- rename "NeoMagic (laptop/notebook)" to "NeoMagic MagicGraph
  (laptop/notebook)" (pixel) (#4686)

* Mon May 24 2004 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 0.1.9-16mdk
- Add Quadro FX 1300 entry
- Fix module loading initio -> a100u2w (nicolas)
- Updating cciss & cpqarray pci ids (erwan)
- Adding some aacraid missing entries (erwan)
- pcitable: remove the few remaining "Server:SVGA" since we don't have XF3 anymore (Pixel)
- Cards+: drop XFree3 related data (Pixel)

* Mon Apr 26 2004 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 0.1.9-15mdk
- add Tatung C7BZR monitor specs
- revert GeForce FX 5700 change as XFree86 4.3 "nv" driver doesn't get it right
- sync with kernel-2.6.3-10mdk and rh's hwdata-0.117 (tv)

* Fri Apr 16 2004 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 0.1.9-14mdk
- add "iteraid" (IT8212) controller
- fix GeForce FX 5700/5950, Quadro FX 1100 entries
- fix empty strings (Erwan)
- add a new samsung monitor (Alojz Stanich)
- GeForce 4 => FX (cosmetic change from Thierry)

* Thu Mar 25 2004 Thierry Vignaud <tvignaud@mandrakesoft.com> 0.1.9-13mdk
- fix support for some mach64
- fix wrong module for DECchip 21041 [Tulip Pass 3] (#9159)

* Wed Mar 24 2004 Thierry Vignaud <tvignaud@mandrakesoft.com> 0.1.9-12mdk
- add support for warly laptop geforce card
- sync with rh's hwdata-0.113, thus adding support for:
  o one Syskonnect SK-98xx gigabit ethernet,
  o one intel ich5 sata controller
  o two voodoo gfx cards

* Thu Mar 18 2004 Thierry Vignaud <tvignaud@mandrakesoft.com> 0.1.9-11mdk
- audigy does not works but snd-emu10k1 does works smoothly (#4512)
- sync with kernel-2.6.3-7mdk
- add LG Flatron 995FT Plus (Bruno Thomsen)
- switch all broadcom from b44 to bcm4400
- update entries for "avision" backend and for Kodak digicam backends (till)

* Tue Mar 16 2004 Thierry Vignaud <tvignaud@mandrakesoft.com> 0.1.9-10mdk
- add MSI WLAN PC2PC usb adapter (nplanel)
- fix Sil3512A description (#8579)
- switch a broadcom from b44 to bcm4400 on arnaud/hp request

* Tue Mar  2 2004 Thierry Vignaud <tvignaud@mandrakesoft.com> 0.1.9-9mdk
- add missing realtek 8139 (#8012)
- merge 2.6.3-4mdk kernel pcimap (planel)
- sanitize intel bridges naming scheme

* Mon Mar  1 2004 Thierry Vignaud <tvignaud@mandrakesoft.com> 0.1.9-8mdk
- add Samsung SyncMaster 765MB (Kozak Daniel)
- fix entry for AGFA SnapScan Touch (#8441) (till)

* Fri Feb 20 2004 Frederic Lepied <flepied@mandrakesoft.com> 0.1.9-7mdk
- pcitable: o updated ATI entries for radeon cards
            o standardize ATI name use

* Thu Feb 19 2004 Thierry Vignaud <tvignaud@mandrakesoft.com> 0.1.9-6mdk
- fix firmware configurationç templates for SANE backend
  "artec_eplus48u" (till)
- update some nvidia card descriptions (gregory)
- update some ati radeon card descriptions (arnaud)
- mark some ati radeon card as managed by fglrx instead of fbdev
  (arnaud)

* Thu Feb 12 2004 Thierry Vignaud <tvignaud@mandrakesoft.com> 0.1.9-5mdk
- monitor db:
  o sync with rh's hwdata-0.105
  o add support for CTL 910TF monitor (#7664)
- fixes:
  o use right module for Zoran ZR36057PQC device (#7654)
  o do not use ata_piix for ich5 since it failled to handle some ATAPI
    device in combined mode (planel)
  o airo_mpi is dead, viva el airo (planel)
- add support for:
  o SiS Real256E (flepied)
  o bluetooth USB key (arnaud delorbeau)
  o support newer ATI (planel)

* Mon Feb  9 2004 Pixel <pixel@mandrakesoft.com> 0.1.9-4mdk
- all graphic cards now have a DRIVER

* Sun Feb  8 2004 Thierry Vignaud <tvignaud@mandrakesoft.com> 0.1.9-3mdk
- sync with kernel-2.6.2.1mdk, rh's hwdata-0.105 and http://www.pcidatabase.com

* Mon Feb  2 2004 Thierry Vignaud <tvignaud@mandrakesoft.com> 0.1.9-2mdk
- merge kernel 2.6.2-0.rc3.1mdk pcimap

* Mon Feb  2 2004 Nicolas Planel <nplanel@mandrakesoft.com> 0.1.9-1mdk
- add prism54 wireless cards support
- add aureal sound cards support

* Thu Jan 29 2004 Pixel <pixel@mandrakesoft.com> 0.1.8-15mdk
- support more sata controller sata_svw ata_piix sata_promise (nplanel)
- philippe.harrand tells his Davicom card works with dmfe module, not tulip (gc)

* Mon Jan 26 2004 Thierry Vignaud <tvignaud@mandrakesoft.com> 0.1.8-14mdk
- add one alcor device (Jaco Greeff <jaco@puxedo.org>)
- add 2 monitors (thanks to Frederik Himpe, bugzilla #6710)
- convert agpgart 24 style to splitted agpgart module (intel-agp,...).
- s/nvnet/forcedeth/
- add sata_sil, sk98lin, NVidia GForce FX 5950

* Fri Dec 12 2003 Pixel <pixel@mandrakesoft.com> 0.1.8-13mdk
- use fbdev for some radeon's
- added new usbid for compatible adiusbadsl modem. (fpons)

* Fri Oct 17 2003 Nicolas Planel <nplanel@mandrakesoft.com> 0.1.8-12mdk
- Add/Update id for Emulex Fibre Channel Host adapter support.

* Tue Oct 14 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 0.1.8-11mdk
- Updates for new libata drivers:
  - VIA 8237 SATA controller (sata_via)
  - Promise SATA150 TX4 controllers (sata_promise)

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

