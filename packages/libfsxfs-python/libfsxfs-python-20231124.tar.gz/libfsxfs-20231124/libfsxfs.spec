Name: libfsxfs
Version: 20231124
Release: 1
Summary: Library to support the X File System (XFS) format
Group: System Environment/Libraries
License: LGPL-3.0-or-later
Source: %{name}-%{version}.tar.gz
URL: https://github.com/libyal/libfsxfs
              
BuildRequires: gcc              

%description -n libfsxfs
Library to support the X File System (XFS) format

%package -n libfsxfs-static
Summary: Library to support the X File System (XFS) format
Group: Development/Libraries
Requires: libfsxfs = %{version}-%{release}

%description -n libfsxfs-static
Static library version of libfsxfs.

%package -n libfsxfs-devel
Summary: Header files and libraries for developing applications for libfsxfs
Group: Development/Libraries
Requires: libfsxfs = %{version}-%{release}

%description -n libfsxfs-devel
Header files and libraries for developing applications for libfsxfs.

%package -n libfsxfs-python3
Summary: Python 3 bindings for libfsxfs
Group: System Environment/Libraries
Requires: libfsxfs = %{version}-%{release} python3
BuildRequires: python3-devel python3-setuptools

%description -n libfsxfs-python3
Python 3 bindings for libfsxfs

%package -n libfsxfs-tools
Summary: Several tools for reading X File System (XFS) volumes
Group: Applications/System
Requires: libfsxfs = %{version}-%{release} openssl fuse-libs 
BuildRequires: openssl-devel fuse-devel 

%description -n libfsxfs-tools
Several tools for reading X File System (XFS) volumes

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

%files -n libfsxfs
%license COPYING COPYING.LESSER
%doc AUTHORS README
%{_libdir}/*.so.*

%files -n libfsxfs-static
%license COPYING COPYING.LESSER
%doc AUTHORS README
%{_libdir}/*.a

%files -n libfsxfs-devel
%license COPYING COPYING.LESSER
%doc AUTHORS README
%{_libdir}/*.so
%{_libdir}/pkgconfig/libfsxfs.pc
%{_includedir}/*
%{_mandir}/man3/*

%files -n libfsxfs-python3
%license COPYING COPYING.LESSER
%doc AUTHORS README
%{_libdir}/python3*/site-packages/*.a
%{_libdir}/python3*/site-packages/*.so

%files -n libfsxfs-tools
%license COPYING COPYING.LESSER
%doc AUTHORS README
%{_bindir}/*
%{_mandir}/man1/*

%changelog
* Fri Nov 24 2023 Joachim Metz <joachim.metz@gmail.com> 20231124-1
- Auto-generated

