%define major	1
%define libname	%mklibname bluray %{major}
%define devname %mklibname bluray -d

Summary:	Blu-Ray Disc playback library for media players
Name:		libbluray
Version:	0.2.3
Release:	11
License:	LGPLv2+
Group:		System/Libraries
Url:		http://www.videolan.org/developers/libbluray.html
# git://git.videolan.org/libbluray.git
# git archive --prefix=libbluray-$(date +%Y%m%d)/ --format=tar HEAD | xz > libbluray-$(date +%Y%m%d).tar.xz
Source0:	ftp://ftp.videolan.org/pub/videolan/libbluray/%{version}/%{name}-%{version}.tar.bz2
# use our default java home if $JAVA_HOME not set at runtime
Patch1:		libbluray-default-java-home.patch

BuildRequires:	ant
BuildRequires:	java-rpmbuild
BuildRequires:	jaxp
BuildRequires:	xerces-j2

%description
libbluray is an open-source library designed for Blu-Ray Discs playback for
media players, like VLC or MPlayer.

The library has support for navigation, playlist parsing, menus and BD-J.

For BD-J support, you need to install libbluray-java.

This package does not contain any DRM circumvention functionality, so you can
only play unprotected Blu-Ray discs with it as is.

%package -n %{libname}
Summary:	Blu-Ray Disc playback library for media players
Group:		System/Libraries

%description -n %{libname}
libbluray is an open-source library designed for Blu-Ray Discs playback for
media players, like VLC or MPlayer.

For BD-J support, you need to install libbluray-java.

This package does not contain any DRM circumvention functionality, so you can
only play unprotected Blu-Ray discs with it as is.

%package java
Summary:	BD-J support for libbluray
Group:		System/Libraries
# Maybe switch to suggesting/requiring libbluray-java in the main lib,
# and dropping these below reqs instead?
Requires:	java >= 1.6
Requires:	jpackage-utils

%description java
libbluray is an open-source library designed for Blu-Ray Discs playback for
media players, like VLC or MPlayer.

This package contains the BD-J support for libbluray.

This package does not contain any DRM circumvention functionality.

%package -n %{devname}
Summary:	libbluray development files
Group:		Development/C
Provides:	%{name}-devel = %{version}-%{release}
Requires:	%{libname} = %{version}-%{release}

%description -n %{devname}
These are the files needed for building programs using libbluray.
This package does not contain any DRM circumvention functionality.

%prep
%setup -q
%apply_patches

sed -i 's/AM_CONFIG_HEADER/AC_CONFIG_HEADER/g' configure.ac
sed -i 's/AM_PROG_CC_STDC/AC_PROG_CC/g' configure.ac
# for ant
export JAVA_HOME=%{java_home}
./bootstrap

%build
%configure2_5x \
	--disable-static \
	--with-jdk=%{java_home} \
	--enable-bdjava
%make

%install
%makeinstall_std

install -d -m755 %{buildroot}%{_javadir}
install -m644 src/.libs/libbluray.jar %{buildroot}%{_javadir}

%files -n %{libname}
%{_libdir}/%{name}.so.%{major}*

%files java
%{_javadir}/%{name}.jar

%files -n %{devname}
%doc README.txt
%{_includedir}/%{name}
%{_bindir}/bd_info
%{_libdir}/%{name}.so
%{_libdir}/pkgconfig/%{name}.pc

