Name: libsmraw
Version: 20231127
Release: 1
Summary: Library to access the storage media (SM) (split) RAW format
Group: System Environment/Libraries
License: LGPL-3.0-or-later
Source: %{name}-%{version}.tar.gz
URL: https://github.com/libyal/libsmraw
             
BuildRequires: gcc             

%description -n libsmraw
Library to access the storage media (SM) (split) RAW format

%package -n libsmraw-static
Summary: Library to access the storage media (SM) (split) RAW format
Group: Development/Libraries
Requires: libsmraw = %{version}-%{release}

%description -n libsmraw-static
Static library version of libsmraw.

%package -n libsmraw-devel
Summary: Header files and libraries for developing applications for libsmraw
Group: Development/Libraries
Requires: libsmraw = %{version}-%{release}

%description -n libsmraw-devel
Header files and libraries for developing applications for libsmraw.

%package -n libsmraw-python3
Summary: Python 3 bindings for libsmraw
Group: System Environment/Libraries
Requires: libsmraw = %{version}-%{release} python3
BuildRequires: python3-devel python3-setuptools

%description -n libsmraw-python3
Python 3 bindings for libsmraw

%package -n libsmraw-tools
Summary: Several tools for reading and writing storage media (SM) (split) RAW files
Group: Applications/System
Requires: libsmraw = %{version}-%{release} openssl fuse-libs 
BuildRequires: openssl-devel fuse-devel 

%description -n libsmraw-tools
Several tools for reading and writing storage media (SM) (split) RAW files

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

%files -n libsmraw
%license COPYING COPYING.LESSER
%doc AUTHORS README
%{_libdir}/*.so.*

%files -n libsmraw-static
%license COPYING COPYING.LESSER
%doc AUTHORS README
%{_libdir}/*.a

%files -n libsmraw-devel
%license COPYING COPYING.LESSER
%doc AUTHORS README
%{_libdir}/*.so
%{_libdir}/pkgconfig/libsmraw.pc
%{_includedir}/*
%{_mandir}/man3/*

%files -n libsmraw-python3
%license COPYING COPYING.LESSER
%doc AUTHORS README
%{_libdir}/python3*/site-packages/*.a
%{_libdir}/python3*/site-packages/*.so

%files -n libsmraw-tools
%license COPYING COPYING.LESSER
%doc AUTHORS README
%{_bindir}/*
%{_mandir}/man1/*

%changelog
* Mon Nov 27 2023 Joachim Metz <joachim.metz@gmail.com> 20231127-1
- Auto-generated

