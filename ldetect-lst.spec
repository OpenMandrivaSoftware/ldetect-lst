%define name ldetect-lst
%define version 0.1.2
%define release 19mdk

Name: %{name}
Version: %{version}
Release: %{release}
Summary: Hardware list for the light detection library
Source: %{name}.tar.bz2
Group: System/Libraries
BuildArchitectures: noarch
BuildRoot: %{_tmppath}/%{name}-buildroot
License: GPL
Prefix: %{_prefix}

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
%setup -n %{name}

%build
%make

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%{_datadir}/%{name}

%files devel
%defattr(-,root,root)
%doc convert/README.pcitable
%{_bindir}/*

%changelog
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

