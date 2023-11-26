Name: libqcow
Version: 20231125
Release: 1
Summary: Library to access the QEMU Copy-On-Write (QCOW) image file format
Group: System Environment/Libraries
License: LGPL-3.0-or-later
Source: %{name}-%{version}.tar.gz
URL: https://github.com/libyal/libqcow
Requires:         openssl      zlib
BuildRequires: gcc         openssl-devel      zlib-devel

%description -n libqcow
Library to access the QEMU Copy-On-Write (QCOW) image file format

%package -n libqcow-static
Summary: Library to access the QEMU Copy-On-Write (QCOW) image file format
Group: Development/Libraries
Requires: libqcow = %{version}-%{release}

%description -n libqcow-static
Static library version of libqcow.

%package -n libqcow-devel
Summary: Header files and libraries for developing applications for libqcow
Group: Development/Libraries
Requires: libqcow = %{version}-%{release}

%description -n libqcow-devel
Header files and libraries for developing applications for libqcow.

%package -n libqcow-python3
Summary: Python 3 bindings for libqcow
Group: System Environment/Libraries
Requires: libqcow = %{version}-%{release} python3
BuildRequires: python3-devel python3-setuptools

%description -n libqcow-python3
Python 3 bindings for libqcow

%package -n libqcow-tools
Summary: Several tools for reading QEMU Copy-On-Write (QCOW) image files
Group: Applications/System
Requires: libqcow = %{version}-%{release} fuse-libs
BuildRequires: fuse-devel

%description -n libqcow-tools
Several tools for reading QEMU Copy-On-Write (QCOW) image files

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

%files -n libqcow
%license COPYING COPYING.LESSER
%doc AUTHORS README
%{_libdir}/*.so.*

%files -n libqcow-static
%license COPYING COPYING.LESSER
%doc AUTHORS README
%{_libdir}/*.a

%files -n libqcow-devel
%license COPYING COPYING.LESSER
%doc AUTHORS README
%{_libdir}/*.so
%{_libdir}/pkgconfig/libqcow.pc
%{_includedir}/*
%{_mandir}/man3/*

%files -n libqcow-python3
%license COPYING COPYING.LESSER
%doc AUTHORS README
%{_libdir}/python3*/site-packages/*.a
%{_libdir}/python3*/site-packages/*.so

%files -n libqcow-tools
%license COPYING COPYING.LESSER
%doc AUTHORS README
%{_bindir}/*
%{_mandir}/man1/*

%changelog
* Sat Nov 25 2023 Joachim Metz <joachim.metz@gmail.com> 20231125-1
- Auto-generated

