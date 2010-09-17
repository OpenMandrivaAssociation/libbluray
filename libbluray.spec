
%define name	libbluray
%define version	0.0.1
%define pre	pre
%define snap	20100917
%define rel	1

%define major	0
%define libname	%mklibname bluray %major
%define devname %mklibname bluray -d

Summary:	Blu-Ray Disc playback library for media players
Name:		%{name}
Version:	%{version}
Release:	%mkrel 0.%pre.git%snap.%rel
License:	LGPLv2+
Group:		System/Libraries
URL:		http://www.videolan.org/developers/libbluray.html
# git://git.videolan.org/libbluray.git
# git archive --prefix=libbluray-$(date +%Y%m%d)/ --format=tar HEAD | xz > libbluray-$(date +%Y%m%d).tar.xz
Source:		%{name}-%{snap}.tar.xz
# use our default java home if $JAVA_HOME not set at runtime
Patch1:		libbluray-default-java-home.patch
BuildRoot:	%{_tmppath}/%{name}-root
BuildRequires:	java-rpmbuild
BuildRequires:	ant

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
Provides:	bluray-devel = %{version}-%{release}
Requires:	%{libname} = %{version}-%{release}

%description -n %{devname}
libbluray is an open-source library designed for Blu-Ray Discs playback for
media players, like VLC or MPlayer.

These are the files needed for building programs using libbluray.
This package does not contain any DRM circumvention functionality.

%prep
%setup -q -n %{name}-%{snap}
%apply_patches

%build
# for ant
export JAVA_HOME=%{java_home}
./bootstrap
%configure2_5x \
	--with-jdk=%{java_home} \
	--enable-bdjava
%make

%install
rm -rf %{buildroot}
%makeinstall_std
install -d -m755 %{buildroot}%{_javadir}
install -m644 src/.libs/libbluray.jar %{buildroot}%{_javadir}

rm %{buildroot}%{_libdir}/*.*a

%clean
rm -rf %{buildroot}

%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/%{name}.so.%{major}*

%files java
%defattr(-,root,root)
%{_javadir}/%{name}.jar

%files -n %{devname}
%defattr(-,root,root)
%doc README.txt TODO.txt
%{_includedir}/%{name}
%{_libdir}/%{name}.so
%{_libdir}/pkgconfig/%{name}.pc
