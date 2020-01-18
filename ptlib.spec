Name:		ptlib
Summary:	Portable Tools Library
Version:	2.10.10
Release:	6%{?dist}
URL:		http://www.opalvoip.org/
License:	MPLv1.0
Group:		System Environment/Libraries

Source0:	ftp://ftp.gnome.org/pub/gnome/sources/%{name}/2.10/%{name}-%{version}.tar.xz
Patch0:		ptlib-fixcamcrash.patch
Patch1:		ptlib-multilib.patch

BuildRequires:	pkgconfig, expat-devel, flex, bison
BuildRequires:  alsa-lib-devel, libv4l-devel
BuildRequires:  openldap-devel, SDL-devel, openssl-devel 
BuildRequires:  boost-devel, pulseaudio-libs-devel

%description
PTLib (Portable Tools Library) is a moderately large class library that 
has it's genesis many years ago as PWLib (portable Windows Library), a 
method to product applications to run on both Microsoft Windows and Unix 
systems. It has also been ported to other systems such as Mac OSX, VxWorks 
and other embedded systems.

It is supplied mainly to support the OPAL project, but that shouldn't stop
you from using it in whatever project you have in mind if you so desire. 

%package devel
Summary:	Development package for ptlib
Group:		Development/Libraries
Requires:	ptlib = %{version}-%{release}
Requires:	pkgconfig

%description devel
The ptlib-devel package includes the libraries and header files for ptlib.

%prep
%setup -q 
%patch0 -p1 -b .fixcam
%patch1 -p1 -b .multilib

%build
export CFLAGS="%{optflags} -DLDAP_DEPRECATED"
%configure --prefix=%{_prefix} --disable-static --enable-plugins --disable-oss --enable-v4l2 --disable-avc --disable-v4l --enable-pulse
make %{?_smp_mflags} V=1

%install
make PREFIX=%{buildroot}%{_prefix} LIBDIR=%{buildroot}%{_libdir} install

perl -pi -e 's@PTLIBDIR.*=.*@PTLIBDIR = /usr/share/ptlib@' %{buildroot}%{_datadir}/ptlib/make/ptbuildopts.mak

# hack to fixup things for bug 197318
find %{buildroot}%{_libdir} -name '*.so*' -type f -exec chmod +x {} \;

#Remove static libs
find %{buildroot} -name '*.a' -exec rm -f {} ';'

# avoid multilib conflict
mv %{buildroot}%{_datadir}/ptlib/make/ptbuildopts.mak \
   %{buildroot}%{_datadir}/ptlib/make/ptbuildopts-%{__isa_bits}.mak

mv %{buildroot}/%{_includedir}/ptbuildopts.h \
   %{buildroot}/%{_includedir}/ptbuildopts-%{__isa_bits}.h
cat >%{buildroot}/%{_includedir}/ptbuildopts.h <<EOF
#ifndef _PT_BUILD_OPTS_H_MULTILIB
#define _PT_BUILD_OPTS_H_MULTILIB

#include <bits/wordsize.h>

#if  __WORDSIZE == 32
# include "ptbuildopts-32.h"
#elif __WORDSIZE == 64
# include "ptbuildopts-64.h"
#else
# error "unexpected value for __WORDSIZE macro"
#endif

#endif
EOF


%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%doc History.txt ReadMe.txt mpl-1.0.htm
%attr(755,root,root) %{_libdir}/libpt*.so.*
%dir %{_libdir}/%{name}-%{version}
%dir %{_libdir}/%{name}-%{version}/devices
%dir %{_libdir}/%{name}-%{version}/devices/sound
%dir %{_libdir}/%{name}-%{version}/devices/videoinput
# List these explicitly so we don't get any surprises
%attr(755,root,root) %{_libdir}/%{name}-%{version}/devices/sound/alsa_pwplugin.so
%attr(755,root,root) %{_libdir}/%{name}-%{version}/devices/sound/pulse_pwplugin.so
%attr(755,root,root) %{_libdir}/%{name}-%{version}/devices/videoinput/v4l2_pwplugin.so

%files devel
%defattr(-,root,root)
%{_libdir}/libpt*.so
%{_includedir}/*
%{_datadir}/ptlib
%{_libdir}/pkgconfig/ptlib.pc
%attr(755,root,root) %{_bindir}/*

%changelog
* Tue Mar 18 2014 Benjamin Otte <otte@redhat.com> - 2.10.2-6
- Fix multilib issues

* Fri Jan 24 2014 Daniel Mach <dmach@redhat.com> - 2.10.10-5
- Mass rebuild 2014-01-24

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 2.10.10-4
- Mass rebuild 2013-12-27

* Wed Oct  9 2013 Matthias Clasen <mclasen@redhat.com> - 2.10.10-3
- Avoid multilib conflict (#884145)

* Tue Apr 30 2013 Daniel Mach <dmach@redhat.com> - 2.10.10-2.2
- Rebuild for cyrus-sasl

* Thu Mar  7 2013 Peter Robinson <pbrobinson@fedoraproject.org> 2.10.10-2
- Add patch to fix crash in webcam - RHBZ 907303

* Wed Feb 20 2013 Peter Robinson <pbrobinson@fedoraproject.org> 2.10.10-1
- New 2.10.10 stable release

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.10.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Nov 26 2012 Peter Robinson <pbrobinson@fedoraproject.org> 2.10.9-1
- New 2.10.9 stable release

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.10.2-4
* Sat Aug 25 2012 Peter Robinson <pbrobinson@fedoraproject.org> - 2.10.7-1
- New 2.10.7 stable release

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.10.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Feb 28 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.10.2-3
- Rebuilt for c++ ABI breakage

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.10.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Aug 23 2011 Peter Robinson <pbrobinson@fedoraproject.org> - 2.10.2-1
- New 2.10.2 stable release

* Sat Jul 16 2011 Peter Robinson <pbrobinson@fedoraproject.org> - 2.10.1-1
- New 2.10.1 stable release

* Wed May  4 2011 Peter Robinson <pbrobinson@fedoraproject.org> - 2.8.3-5
- Add patch to fix ptlib using internal gcc functions

* Wed Apr 20 2011 Peter Robinson <pbrobinson@fedoraproject.org> - 2.8.3-4
- Add initial upstream patch to deal with Network interfaces with names other than eth - RHBZ 682388

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.8.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Dec 27 2010 Ville Skyttä <ville.skytta@iki.fi> - 2.8.3-2
- Let rpmbuild strip binaries.

* Thu Dec 23 2010 Peter Robinson <pbrobinson@fedoraproject.org> - 2.8.3-1
- New 2.8.3 stable release

* Mon May 31 2010 Peter Robinson <pbrobinson@fedoraproject.org> - 2.6.7-1
- New 2.6.7 stable release

* Tue Sep 22 2009 Peter Robinson <pbrobinson@fedoraproject.org> - 2.6.5-1
- New 2.6.5 stable release

* Sat Aug 22 2009 Tomas Mraz <tmraz@redhat.com> - 2.6.4-5
- rebuilt with new openssl

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Jul  6 2009 Peter Robinson <pbrobinson@fedoraproject.org> - 2.6.4-1
- New 2.6.4 stable release

* Tue May 19 2009 Peter Robinson <pbrobinson@fedoraproject.org> - 2.6.2-1
- New stable release for ekiga 3.2.1

* Wed Mar 18 2009 Peter Robinson <pbrobinson@fedoraproject.org> - 2.6.1-1
- New stable release for ekiga 3.2.0

* Tue Mar  3 2009 Peter Robinson <pbrobinson@fedoraproject.org> - 2.6.0-1
- New release for ekiga 3.1.2 beta

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Jan 17 2009 Tomas Mraz <tmraz@redhat.com> - 2.5.2-4
- rebuild with new openssl

* Tue Jan 13 2009 Peter Robinson <pbrobinson@fedoraproject.org> - 2.5.2-3
- Add an extra build dep

* Tue Jan  6 2009 Peter Robinson <pbrobinson@fedoraproject.org> - 2.5.2-2
- remove --enable-opal termpoarily, ironically so opal will compile

* Tue Jan  6 2009 Peter Robinson <pbrobinson@fedoraproject.org> - 2.5.2-1
- New release for ekiga 3.1.0 beta

* Mon Oct 20 2008 Peter Robinson <pbrobinson@fedoraproject.org> - 2.4.2-1
- Update to new stable release for ekiga 3.0.1

* Tue Sep 23 2008 Peter Robinson <pbrobinson@fedoraproject.org> - 2.4.1-1
- Update to new stable release for ekiga 3, disable v4l1

* Wed Sep 10 2008 Peter Robinson <pbrobinson@fedoraproject.org> - 2.3.1-2
- Build fixes from package review

* Sun Jun 8 2008 Peter Robinson <pbrobinson@fedoraproject.org> - 2.3.1-1
- Initial version of ptlib
