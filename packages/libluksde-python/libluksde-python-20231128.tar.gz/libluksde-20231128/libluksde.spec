Name: libluksde
Version: 20231128
Release: 1
Summary: Library to access the Linux Unified Key Setup (LUKS) Disk Encryption format
Group: System Environment/Libraries
License: LGPL-3.0-or-later
Source: %{name}-%{version}.tar.gz
URL: https://github.com/libyal/libluksde
Requires:         openssl       
BuildRequires: gcc         openssl-devel       

%description -n libluksde
Library to access the Linux Unified Key Setup (LUKS) Disk Encryption format

%package -n libluksde-static
Summary: Library to access the Linux Unified Key Setup (LUKS) Disk Encryption format
Group: Development/Libraries
Requires: libluksde = %{version}-%{release}

%description -n libluksde-static
Static library version of libluksde.

%package -n libluksde-devel
Summary: Header files and libraries for developing applications for libluksde
Group: Development/Libraries
Requires: libluksde = %{version}-%{release}

%description -n libluksde-devel
Header files and libraries for developing applications for libluksde.

%package -n libluksde-python3
Summary: Python 3 bindings for libluksde
Group: System Environment/Libraries
Requires: libluksde = %{version}-%{release} python3
BuildRequires: python3-devel python3-setuptools

%description -n libluksde-python3
Python 3 bindings for libluksde

%package -n libluksde-tools
Summary: Several tools for reading Linux Unified Key Setup (LUKS) Disk Encryption volumes
Group: Applications/System
Requires: libluksde = %{version}-%{release} fuse-libs
BuildRequires: fuse-devel

%description -n libluksde-tools
Several tools for reading Linux Unified Key Setup (LUKS) Disk Encryption volumes

%prep
%setup -q

%build
%configure --prefix=/usr --libdir=%{_libdir} --mandir=%{_mandir} --enable-python
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
%make_install

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files -n libluksde
%license COPYING COPYING.LESSER
%doc AUTHORS README
%{_libdir}/*.so.*

%files -n libluksde-static
%license COPYING COPYING.LESSER
%doc AUTHORS README
%{_libdir}/*.a

%files -n libluksde-devel
%license COPYING COPYING.LESSER
%doc AUTHORS README
%{_libdir}/*.so
%{_libdir}/pkgconfig/libluksde.pc
%{_includedir}/*
%{_mandir}/man3/*

%files -n libluksde-python3
%license COPYING COPYING.LESSER
%doc AUTHORS README
%{_libdir}/python3*/site-packages/*.a
%{_libdir}/python3*/site-packages/*.so

%files -n libluksde-tools
%license COPYING COPYING.LESSER
%doc AUTHORS README
%{_bindir}/*
%{_mandir}/man1/*

%changelog
* Tue Nov 28 2023 Joachim Metz <joachim.metz@gmail.com> 20231128-1
- Auto-generated

