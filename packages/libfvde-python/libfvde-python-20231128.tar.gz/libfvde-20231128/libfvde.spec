Name: libfvde
Version: 20231128
Release: 1
Summary: Library to access the FileVault Drive Encryption (FVDE) format
Group: System Environment/Libraries
License: LGPL-3.0-or-later
Source: %{name}-%{version}.tar.gz
URL: https://github.com/libyal/libfvde
Requires:         openssl          zlib
BuildRequires: gcc         openssl-devel          zlib-devel

%description -n libfvde
Library to access the FileVault Drive Encryption (FVDE) format

%package -n libfvde-static
Summary: Library to access the FileVault Drive Encryption (FVDE) format
Group: Development/Libraries
Requires: libfvde = %{version}-%{release}

%description -n libfvde-static
Static library version of libfvde.

%package -n libfvde-devel
Summary: Header files and libraries for developing applications for libfvde
Group: Development/Libraries
Requires: libfvde = %{version}-%{release}

%description -n libfvde-devel
Header files and libraries for developing applications for libfvde.

%package -n libfvde-python3
Summary: Python 3 bindings for libfvde
Group: System Environment/Libraries
Requires: libfvde = %{version}-%{release} python3
BuildRequires: python3-devel python3-setuptools

%description -n libfvde-python3
Python 3 bindings for libfvde

%package -n libfvde-tools
Summary: Several tools for reading FileVault Drive Encryption volumes
Group: Applications/System
Requires: libfvde = %{version}-%{release} fuse-libs
BuildRequires: fuse-devel

%description -n libfvde-tools
Several tools for reading FileVault Drive Encryption volumes

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

%files -n libfvde
%license COPYING COPYING.LESSER
%doc AUTHORS README
%{_libdir}/*.so.*

%files -n libfvde-static
%license COPYING COPYING.LESSER
%doc AUTHORS README
%{_libdir}/*.a

%files -n libfvde-devel
%license COPYING COPYING.LESSER
%doc AUTHORS README
%{_libdir}/*.so
%{_libdir}/pkgconfig/libfvde.pc
%{_includedir}/*
%{_mandir}/man3/*

%files -n libfvde-python3
%license COPYING COPYING.LESSER
%doc AUTHORS README
%{_libdir}/python3*/site-packages/*.a
%{_libdir}/python3*/site-packages/*.so

%files -n libfvde-tools
%license COPYING COPYING.LESSER
%doc AUTHORS README
%{_bindir}/*
%{_mandir}/man1/*

%changelog
* Tue Nov 28 2023 Joachim Metz <joachim.metz@gmail.com> 20231128-1
- Auto-generated

