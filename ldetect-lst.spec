%define name ldetect-lst
%define version 0.1.2
%define release 1mdk

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

%description
The hardware device lists provided by this package are used as lookup 
table to get hardware autodetection

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

%changelog
* Sat Dec 16 2000 Pixel <pixel@mandrakesoft.com> 0.1.2-1mdk
- add usbtable

* Fri Dec 15 2000 Pixel <pixel@mandrakesoft.com> 0.1.1-1mdk
- add Cards+, MonitorsDB, isdn.db

* Fri Dec 15 2000 Pixel <pixel@mandrakesoft.com> 0.1.0-1mdk
- first release

