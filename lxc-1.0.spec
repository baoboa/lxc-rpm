%if 0%{?fedora} || 0%{?rhel} > 6
%global with_python3 1
%endif

%global with_lua 1
%if 0%{?fedora} > 19
%global luaver 5.2
%else
%global luaver 5.1
%endif
%global lualibdir %{_libdir}/lua/%{luaver}
%global luapkgdir %{_datadir}/lua/%{luaver}

Name:           lxc
Version:        1.0.1
Release:        b2%{?dist}
Summary:        Linux Resource Containers
Group:          Applications/System
License:        LGPLv2+ and GPLv2
URL:            http://lxc.sourceforge.net
Source0:        https://codeload.github.com/lxc/lxc/zip/%{name}-%{version}.tar.gz
#Source0:       http://lxc.sourceforge.net/download/lxc/%{name}-%{version}.tar.gz
BuildRequires:  docbook-utils
Buildrequires:  docbook2X
BuildRequires:  kernel-headers
BuildRequires:  libcap-devel
BuildRequires:  libtool
%if 0%{?with_python3}
BuildRequires:  python3-devel >= 3.2
%endif
%if 0%{?with_lua}
BuildRequires:  lua-devel
%endif

%{!?_pkgdocdir: %global _pkgdocdir %{_docdir}/%{name}-%{version}}

%description
Linux Resource Containers provide process and resource isolation without the
overhead of full virtualization.


%package        libs
Summary:        Runtime library files for %{name}
Group:          System Environment/Libraries

%description    libs
Linux Resource Containers provide process and resource isolation without the
overhead of full virtualization.

The %{name}-libs package contains libraries for running %{name} applications.


%if 0%{?with_python3}
%package        -n python3-%{name}
Summary:        Python binding for %{name}
Group:          System Environment/Libraries

%description    -n python3-%{name}
Linux Resource Containers provide process and resource isolation without the
overhead of full virtualization.

The python3-%{name} package contains the Python3 binding for %{name}.

%global __provides_exclude %{?__provides_exclude:%__provides_exclude|}_lxc\\..*\\.so


%package        extra
Summary:        Extra tools for %{name}
Group:          Applications/System
Requires:       python3-%{name}%{?_isa} = %{version}-%{release}

%description    extra
Linux Resource Containers provide process and resource isolation without the
overhead of full virtualization.

This package contains tools needing the Python3 bindings.
%endif


%if 0%{?with_lua}
%package        -n lua-%{name}
Summary:        Lua binding for %{name}
Group:          System Environment/Libraries
Requires:       lua-filesystem

%description    -n lua-%{name}
Linux Resource Containers provide process and resource isolation without the
overhead of full virtualization.

The lua-%{name} package contains the Lua binding for %{name}.

%global __provides_exclude %{?__provides_exclude:%__provides_exclude|}core\\.so\\.0
%endif


%package        templates
Summary:        Templates for %{name}
Group:          System Environment/Libraries
Requires:       %{name}-libs%{?_isa} = %{version}-%{release}
# needed for lxc-busybox
Requires:       busybox
# needed for lxc-debian
Requires:       dpkg
# needed for lxc-debian, lxc-ubuntu:
Requires:       debootstrap rsync
# needed for lxc-sshd
Requires:       openssh-server dhclient


%description    templates
Linux Resource Containers provide process and resource isolation without the
overhead of full virtualization.

The %{name}-templates package contains templates for creating containers.


%package        devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name}-libs%{?_isa} = %{version}-%{release}
Requires:       pkgconfig

%description    devel
Linux Resource Containers provide process and resource isolation without the
overhead of full virtualization.

The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%package        doc
Summary:        Documentation for %{name}
Group:          Documentation
BuildArch:      noarch

%description    doc
This package contains documentation for %{name}.

%prep
%setup -q -n %{name}-%{version}


%build
%configure --with-distro=fedora \
           --enable-doc \
           --docdir=%{_pkgdocdir} \
           --disable-rpath \
           --disable-apparmor \
%if 0%{?with_python3}
           --enable-python \
%endif
%if 0%{?with_lua}
           --enable-lua \
%endif
# intentionally blank line
make %{?_smp_mflags}


%install
%{make_install}
make DESTDIR=%{buildroot} install
mkdir -p %{buildroot}%{_sharedstatedir}/%{name}
%if 0%{?with_lua}
chmod -x %{buildroot}%{luapkgdir}/lxc.lua
%endif

mkdir -p %{buildroot}%{_pkgdocdir}
cp -a AUTHORS COPYING README %{buildroot}%{_pkgdocdir}


%check
make check


%post libs -p /sbin/ldconfig


%postun libs -p /sbin/ldconfig


%files
%{_sysconfdir}/bash_completion.d/lxc
%{_prefix}/lib/systemd/system/lxc.service
%{_bindir}/%{name}-*
%{_mandir}/ja/man1/%{name}*
%{_mandir}/man1/%{name}*
%{_datadir}/%{name}/lxc.functions
%if 0%{?with_python3}
%exclude %{_bindir}/%{name}-device
%exclude %{_bindir}/%{name}-ls
%exclude %{_bindir}/%{name}-start-ephemeral
%exclude %{_mandir}/man1/%{name}-device*
%exclude %{_mandir}/man1/%{name}-ls*
%exclude %{_mandir}/man1/%{name}-start-ephemeral*
%else
%{_bindir}/%{name}-ls
%{_mandir}/man1/%{name}-ls*
%endif


%files libs
%dir %{_datadir}/%{name}
%dir %{_datadir}/%{name}/templates
%{_datadir}/%{name}/hooks
%{_libdir}/liblxc.so.*
%{_libdir}/%{name}
%{_libexecdir}/%{name}
%{_sharedstatedir}/%{name}
%dir %{_sysconfdir}/%{name}
%config(noreplace) %{_sysconfdir}/%{name}/default.conf
%{_mandir}/ja/man5/%{name}*
%{_mandir}/man5/%{name}*
%{_mandir}/ja/man7/%{name}*
%{_mandir}/man7/%{name}*
%dir %{_pkgdocdir}
%{_pkgdocdir}/AUTHORS
%{_pkgdocdir}/COPYING
%{_pkgdocdir}/README


%if 0%{?with_python3}
%files -n python3-%{name}
%{python3_sitearch}/*


%files extra
%{_bindir}/%{name}-device
%{_bindir}/%{name}-ls
%{_bindir}/%{name}-start-ephemeral
%{_mandir}/man1/%{name}-device*
%{_mandir}/man1/%{name}-ls*
%{_mandir}/man1/%{name}-start-ephemeral*
%endif


%if 0%{?with_lua}
%files -n lua-%{name}
%{lualibdir}/%{name}
%{luapkgdir}/%{name}.lua
%endif


%files templates
%{_datadir}/lxc/templates/lxc-*
%{_datadir}/lxc/config/*.conf
# needs apt
%exclude %{_datadir}/lxc/templates/lxc-altlinux
# needs pacman
%exclude %{_datadir}/lxc/templates/lxc-archlinux
# needs zypper
%exclude %{_datadir}/lxc/templates/lxc-opensuse
# needs ubuntu-cloudimg-query
%exclude %{_datadir}/lxc/templates/lxc-ubuntu-cloud


%files devel
%{_libdir}/pkgconfig/%{name}.pc
%{_includedir}/lxc
%{_libdir}/liblxc.so


%files doc
%dir %{_pkgdocdir}
# README, AUTHORS and COPYING intentionally duplicated because -doc
# can be installed on its own.
%{_pkgdocdir}/*


%changelog

* Wed Mar  5 2014 baoboa <baobab874@gmail.com> - 1.0.1
- initial porting to 1.0 from upstream 

* Wed Sep  4 2013 Thomas Moschny <thomas.moschny@gmx.de> - 0.9.0-2
- Small fix to the included Fedora template.

* Sun Sep  1 2013 Thomas Moschny <thomas.moschny@gmx.de> - 0.9.0-1
- Update to 0.9.0.
- Make the -libs subpackage installable on its own:
  - Move files needed by the libraries to the subpackage.
  - Let packages depend on -libs.
- Add rsync as dependency to the templates package.
- Add (optional) subpackages for Python3 and Lua bindings.
- Add upstream patches for the Fedora template.
- Define and use the _pkgdocdir macro, also fixing rhbz#1001235.
- Update License tag.

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sat Mar  2 2013 Thomas Moschny <thomas.moschny@gmx.de> - 0.8.0-2
- Add upstream patch fixing the release url in the Fedora template.

* Fri Feb 15 2013 Thomas Moschny <thomas.moschny@gmx.de> - 0.8.0-1
- Update to 0.8.0.
- Modernize spec file.
- Include more templates.

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Mar 26 2012 Thomas Moschny <thomas.moschny@gmx.de> - 0.7.5-1
- Update to upstream 0.7.5
- No need to run autogen.sh
- Fix: kernel header asm/unistd.h was not found
- Specfile cleanups

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.4.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Jul 06 2011 Adam Miller <maxamillion@fedoraproject.org> - 0.7.4.2-1
- Update to upstream 0.7.4.2

* Fri Mar 25 2011 Silas Sewell <silas@sewell.ch> - 0.7.4.1-1
- Update to 0.7.4.1

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Jul 26 2010 Silas Sewell <silas@sewell.ch> - 0.7.2-1
- Update to 0.7.2
- Remove templates

* Tue Jul 06 2010 Silas Sewell <silas@sewell.ch> - 0.7.1-1
- Update to 0.7.1

* Wed Feb 17 2010 Silas Sewell <silas@sewell.ch> - 0.6.5-1
- Update to latest release
- Add /var/lib/lxc directory
- Patch for sys/stat.h

* Fri Nov 27 2009 Silas Sewell <silas@sewell.ch> - 0.6.4-1
- Update to latest release
- Add documentation sub-package

* Mon Jul 27 2009 Silas Sewell <silas@sewell.ch> - 0.6.3-2
- Apply patch for rawhide kernel

* Sat Jul 25 2009 Silas Sewell <silas@sewell.ch> - 0.6.3-1
- Initial package
