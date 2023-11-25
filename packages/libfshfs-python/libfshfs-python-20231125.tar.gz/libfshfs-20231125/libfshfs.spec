Name: libfshfs
Version: 20231125
Release: 1
Summary: Library to access the Hierarchical File System (HFS) format
Group: System Environment/Libraries
License: LGPL-3.0-or-later
Source: %{name}-%{version}.tar.gz
URL: https://github.com/libyal/libfshfs
Requires:                zlib
BuildRequires: gcc                zlib-devel

%description -n libfshfs
Library to access the Hierarchical File System (HFS) format

%package -n libfshfs-static
Summary: Library to access the Hierarchical File System (HFS) format
Group: Development/Libraries
Requires: libfshfs = %{version}-%{release}

%description -n libfshfs-static
Static library version of libfshfs.

%package -n libfshfs-devel
Summary: Header files and libraries for developing applications for libfshfs
Group: Development/Libraries
Requires: libfshfs = %{version}-%{release}

%description -n libfshfs-devel
Header files and libraries for developing applications for libfshfs.

%package -n libfshfs-python3
Summary: Python 3 bindings for libfshfs
Group: System Environment/Libraries
Requires: libfshfs = %{version}-%{release} python3
BuildRequires: python3-devel python3-setuptools

%description -n libfshfs-python3
Python 3 bindings for libfshfs

%package -n libfshfs-tools
Summary: Several tools for reading Hierarchical File System (HFS) volumes
Group: Applications/System
Requires: libfshfs = %{version}-%{release} openssl fuse-libs 
BuildRequires: openssl-devel fuse-devel 

%description -n libfshfs-tools
Several tools for reading Hierarchical File System (HFS) volumes

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

%files -n libfshfs
%license COPYING COPYING.LESSER
%doc AUTHORS README
%{_libdir}/*.so.*

%files -n libfshfs-static
%license COPYING COPYING.LESSER
%doc AUTHORS README
%{_libdir}/*.a

%files -n libfshfs-devel
%license COPYING COPYING.LESSER
%doc AUTHORS README
%{_libdir}/*.so
%{_libdir}/pkgconfig/libfshfs.pc
%{_includedir}/*
%{_mandir}/man3/*

%files -n libfshfs-python3
%license COPYING COPYING.LESSER
%doc AUTHORS README
%{_libdir}/python3*/site-packages/*.a
%{_libdir}/python3*/site-packages/*.so

%files -n libfshfs-tools
%license COPYING COPYING.LESSER
%doc AUTHORS README
%{_bindir}/*
%{_mandir}/man1/*

%changelog
* Sat Nov 25 2023 Joachim Metz <joachim.metz@gmail.com> 20231125-1
- Auto-generated

