%define name ldetect-lst
%define version 0.1.2
%define release 6mdk

Name: %{name}
Version: %{version}
Release: %{release}
Summary: Hardware list for the light detection library
Source: %{name}.tar.bz2
Group: System/Libraries
BuildArchitectures: noarch
BuildRoot: %{_tmppath}/%{name}-buildroot
Copyright: GPL
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

