# Define ndiswrapper_version only if it is not already defined.
%{!?ndiswrapper_version: %define ndiswrapper_version 1.53}
%{!?ndiswrapper_release: %define ndiswrapper_release 1}

# Define kernel version if not already defined
%{!?kernel: %define kernel %(uname -r)}
%{!?ksrc: %define ksrc /lib/modules/%{kernel}/source}
%{!?_inst_dir: %define _inst_dir /lib/modules/%{kernel}/misc}

%define _sbinrootdir /sbin

Summary: ndiswrapper allows you to use windows XP drivers for that WLAN card without proper Linux drivers.
Name: ndiswrapper
Version: %{ndiswrapper_version}
Release: %{ndiswrapper_release}
License: GPL
Group: System Environment/Base
URL: http://ndiswrapper.sourceforge.net
Source: %{name}-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: %{ksrc}/Makefile

%description
Some wireless LAN vendors refuse to release hardware specifications or
drivers for their products for operating systems other than Microsoft
Windows. The ndiswrapper project makes it possible to use such
hardware with Linux by means of a loadable kernel module that "wraps
around" NDIS (Windows network driver API) drivers.  This rpm contains
just the userspace tools. You will also need the kernel module rpm.

%package -n kernel-module-%{name}-%{kernel}
Summary: Ndiswrapper kernel module
Group: System Environment/Base
Requires: /boot/vmlinuz-%{kernel}, modutils
Requires: %{name} = %{version}-%{release}
BuildRequires: %{ksrc}/Makefile

%description -n kernel-module-%{name}-%{kernel}
Kernel module for ndiswrapper.

%prep
%setup -q

%build
make all KVERS=%{kernel} KSRC=%{ksrc}

%install

%define inst_dir $RPM_BUILD_ROOT%{_inst_dir}
%define sbindir $RPM_BUILD_ROOT%{_sbinrootdir}
%define usrsbindir $RPM_BUILD_ROOT%{_sbindir}
%define mandir $RPM_BUILD_ROOT%{_mandir}

rm -rf $RPM_BUILD_ROOT
make install DIST_DESTDIR=$RPM_BUILD_ROOT INST_DIR=%{inst_dir} KVERS=%{kernel} KSRC=%{ksrc} sbindir=%{sbindir} usrsbindir=%{usrsbindir} mandir=%{mandir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(0755,root,root)
%{_sbinrootdir}/loadndisdriver
%{_sbindir}/ndiswrapper*
%{_mandir}/man8/*
%doc README AUTHORS ChangeLog INSTALL

%files -n kernel-module-%{name}-%{kernel}
%{_inst_dir}/ndiswrapper.*

%post -n kernel-module-%{name}-%{kernel}
if [ "`uname -r`" = "%{kernel}" ] ; then
  depmod -a >/dev/null 2>&1 || :
fi

%postun -n kernel-module-%{name}-%{kernel}
if [ "`uname -r`" = "%{kernel}" ] ; then
  depmod -a >/dev/null 2>&1 || :
fi

%changelog
* Mon Jan 10 2005 David Kaplan <dmk@localhost.localdomain> - 
- Got rid of makeinstall macro as it asks for problems and use naming convention of make files.

* Tue Jan  4 2005 David Kaplan <dmk@localhost.localdomain> - 
- Updated spec file so that it is closer to kernel module standard spec
- Made ndiswrapper_version a configurable macro

* Tue Feb  3 2004  <abennett@olin.edu> - 
- Initial build.

