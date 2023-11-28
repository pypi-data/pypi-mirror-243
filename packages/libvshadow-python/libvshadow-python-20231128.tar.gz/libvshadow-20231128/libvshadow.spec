Name: libvshadow
Version: 20231128
Release: 1
Summary: Library to access the Windows NT Volume Shadow Snapshot (VSS) format
Group: System Environment/Libraries
License: LGPL-3.0-or-later
Source: %{name}-%{version}.tar.gz
URL: https://github.com/libyal/libvshadow
            
BuildRequires: gcc            

%description -n libvshadow
Library to access the Windows NT Volume Shadow Snapshot (VSS) format

%package -n libvshadow-static
Summary: Library to access the Windows NT Volume Shadow Snapshot (VSS) format
Group: Development/Libraries
Requires: libvshadow = %{version}-%{release}

%description -n libvshadow-static
Static library version of libvshadow.

%package -n libvshadow-devel
Summary: Header files and libraries for developing applications for libvshadow
Group: Development/Libraries
Requires: libvshadow = %{version}-%{release}

%description -n libvshadow-devel
Header files and libraries for developing applications for libvshadow.

%package -n libvshadow-python3
Summary: Python 3 bindings for libvshadow
Group: System Environment/Libraries
Requires: libvshadow = %{version}-%{release} python3
BuildRequires: python3-devel python3-setuptools

%description -n libvshadow-python3
Python 3 bindings for libvshadow

%package -n libvshadow-tools
Summary: Several tools for reading Windows NT Volume Shadow Snapshots (VSS)
Group: Applications/System
Requires: libvshadow = %{version}-%{release} fuse-libs
BuildRequires: fuse-devel

%description -n libvshadow-tools
Several tools for reading Windows NT Volume Shadow Snapshots (VSS)

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

%files -n libvshadow
%license COPYING COPYING.LESSER
%doc AUTHORS README
%{_libdir}/*.so.*

%files -n libvshadow-static
%license COPYING COPYING.LESSER
%doc AUTHORS README
%{_libdir}/*.a

%files -n libvshadow-devel
%license COPYING COPYING.LESSER
%doc AUTHORS README
%{_libdir}/*.so
%{_libdir}/pkgconfig/libvshadow.pc
%{_includedir}/*
%{_mandir}/man3/*

%files -n libvshadow-python3
%license COPYING COPYING.LESSER
%doc AUTHORS README
%{_libdir}/python3*/site-packages/*.a
%{_libdir}/python3*/site-packages/*.so

%files -n libvshadow-tools
%license COPYING COPYING.LESSER
%doc AUTHORS README
%{_bindir}/*
%{_mandir}/man1/*

%changelog
* Tue Nov 28 2023 Joachim Metz <joachim.metz@gmail.com> 20231128-1
- Auto-generated

