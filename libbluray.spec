%define major 2
%define libname %mklibname bluray %{major}
%define devname %mklibname bluray -d

Summary:	Blu-Ray Disc playback library for media players
Name:		libbluray
Version:	1.3.1
Release:	1
License:	LGPLv2+
Group:		System/Libraries
Url:		http://www.videolan.org/developers/libbluray.html
# git://git.videolan.org/libbluray.git
# git archive --prefix=libbluray-$(date +%Y%m%d)/ --format=tar HEAD | xz > libbluray-$(date +%Y%m%d).tar.xz
Source0:	http://ftp.videolan.org/pub/videolan/libbluray/%{version}/%{name}-%{version}.tar.bz2
# From OpenJDK source tarball, src/java.desktop/share/classes/sun/awt/ConstrainableGraphics.java
Source1:	ConstrainableGraphics.java
# use our default java home if $JAVA_HOME not set at runtime
#Patch1:		libbluray-default-java-home.patch
#Patch2:		libbluray-1.1.2-java12.patch

%ifnarch %{armx}
BuildRequires:	ant
BuildRequires:	java-rpmbuild
BuildRequires:	jdk-current
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

%ifnarch %{armx}
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
%endif

%package -n %{devname}
Summary:	libbluray development files
Group:		Development/C
Provides:	%{name}-devel = %{version}-%{release}
Requires:	%{libname} = %{version}-%{release}

%description -n %{devname}
These are the files needed for building programs using libbluray.
This package does not contain any DRM circumvention functionality.

%prep
%autosetup -p1

%ifnarch %{armx}
# First steps to make --enable-bdjava-jar work, but doesn't work
# because bdj.awt.* calls into java.awt.* private stuff
mkdir -p src/libbluray/bdj/java/sun/awt
cp %{S:1} src/libbluray/bdj/java/sun/awt/

mv src/libbluray/bdj/java/java src/libbluray/bdj/java/bdj
mv src/libbluray/bdj/java-j2se/java src/libbluray/bdj/java-j2se/bdj
mv src/libbluray/bdj/java-j2me/java src/libbluray/bdj/java-j2me/bdj
find src/libbluray/bdj -name "*.java" |while read r; do
	P="`grep '^package java\.' $r |cut -d' ' -f2 |cut -d';' -f1`"
	if [ -n "$P" ]; then
		echo "Need to move $r from $P"
		sed -i -e "/^package java/aimport $P.*;" $r
		sed -i -e "s/^package java/package bdj/" $r
	fi
done

. %{_sysconfdir}/profile.d/90java.sh

# for ant
./bootstrap
%endif

%build
%ifnarch %{armx}
. %{_sysconfdir}/profile.d/90java.sh
%endif

%configure \
	--disable-bdjava-jar \
	--with-java9 \
	--with-jdk="$JAVA_HOME"

%make_build

%install
%make_install

%files -n %{libname}
%{_libdir}/%{name}.so.%{major}*

%files -n %{devname}
%doc README.txt
%{_includedir}/%{name}
%{_bindir}/bd_info
%{_bindir}/bd_list_titles
%{_bindir}/bd_splice
%{_libdir}/%{name}.so
%{_libdir}/pkgconfig/%{name}.pc
