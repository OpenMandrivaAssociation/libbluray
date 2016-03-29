%define major 1
%define libname %mklibname bluray %{major}
%define devname %mklibname bluray -d

Summary:	Blu-Ray Disc playback library for media players
Name:		libbluray
Version:	0.9.2
Release:	1
License:	LGPLv2+
Group:		System/Libraries
Url:		http://www.videolan.org/developers/libbluray.html
# git://git.videolan.org/libbluray.git
# git archive --prefix=libbluray-$(date +%Y%m%d)/ --format=tar HEAD | xz > libbluray-$(date +%Y%m%d).tar.xz
Source0:	http://ftp.videolan.org/pub/videolan/libbluray/%{version}/%{name}-%{version}.tar.bz2
# use our default java home if $JAVA_HOME not set at runtime
#Patch1:		libbluray-default-java-home.patch

%ifnarch %{armx}
BuildRequires:	ant
BuildRequires:	java-rpmbuild
BuildRequires:	xerces-j2
%endif
BuildRequires:	pkgconfig(fontconfig)
BuildRequires:	pkgconfig(freetype2)
BuildRequires:	pkgconfig(libxml-2.0)

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
Requires:	javapackages-tools

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
%ifnarch %{armx}
# for ant
export JAVA_HOME=%{java_home}
./bootstrap
%endif

%build
%configure \
%ifarch %{armx}
	--disable-bdjava
%else
	--with-jdk=%{java_home} \
	--enable-bdjava
%endif

%make

%install
%makeinstall_std

%files -n %{libname}
%{_libdir}/%{name}.so.%{major}*

%ifnarch %{armx}
%files java
%{_javadir}/%{name}*.jar
%endif

%files -n %{devname}
%doc README.txt
%{_includedir}/%{name}
%{_bindir}/bd_info
%{_libdir}/%{name}.so
%{_libdir}/pkgconfig/%{name}.pc

