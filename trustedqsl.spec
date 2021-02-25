%undefine __cmake_in_source_build

%global srcname tqsl

%define major 2.5
%define libname %mklibname %{name} %{major}
%define devname %mklibname -d %{name}

Name:           trustedqsl
Version:        2.5.7
Release:        2%{?dist}
Summary:        Tool for digitally signing Amateur Radio QSO records
License:        BSD
URL:            http://sourceforge.net/projects/trustedqsl/

Source0:        https://sourceforge.net/projects/%{name}/files/%{srcname}-%{version}.tar.gz
Source1:        tqsl.appdata.xml

Patch0:         tqsl-2.5-rpath.patch
Patch1:         tqsl-tqsllib.patch

BuildRequires:  cmake
BuildRequires:  lmdb-devel
BuildRequires:  pkgconfig(libssl)
BuildRequires:  curl-devel
BuildRequires:  expat-devel
BuildRequires:  wxgtku3.0-devel
BuildRequires:  zlib-devel
BuildRequires:  desktop-file-utils
BuildRequires:  pkgconfig(appstream-glib)

Requires:       curl

%description
The TrustedQSL applications are used for generating digitally signed
QSO records (records of Amateur Radio contacts). This package
contains the GUI applications tqslcert and tqsl.

%package -n 	%{libname}
Summary:        TrustedQSL library
Provides:	tqsllib = %{EVRD}

%description -n %{libname}
The TrustedQSL library is used for generating digitally signed
QSO records (records of Amateur Radio contacts). This package
contains the library and configuration files needed to run
TrustedQSL applications.

%package -n	%{devname}
Summary:        Development files the for TrustedQSL library
Requires:       %{libname} = %{EVRD}
Provides:	trustedqsl-devel = %{EVRD}

%description -n %{devname}
The TrustedQSL library is used for generating digitally signed
QSO records (records of Amateur Radio contacts). This package
contains the to develop with tqsllib.


%prep
%autosetup -p1 -n %{srcname}-%{version}


%build
%cmake -DCMAKE_BUILD_TYPE=RelWithDebInfo

%make_build


%install
%make_install -C build

# Remove bundled language file that shouldn't be there.
find %{buildroot}%{_datadir}/locale/ -type f -name wxstd.mo -exec rm -f {} \;

%find_lang tqslapp

# Install desktop files
mkdir -p %{buildroot}%{_datadir}/applications
sed -i -e "s/.png//g" -e "s/Application;/Network;/g" -e "s/Utility;/GTK;/g" apps/tqsl.desktop
desktop-file-install \
        --dir=%{buildroot}%{_datadir}/applications apps/tqsl.desktop

# Install icons
for size in 16 32 48 64 128; do
    install -Dpm 0644 apps/icons/key${size}.png \
    %{buildroot}%{_datadir}/icons/hicolor/${size}x${size}/apps/TrustedQSL.png
done

# Install appdata file
mkdir -p %{buildroot}%{_datadir}/appdata
install -pm 0644 %{SOURCE1} %{buildroot}%{_datadir}/appdata/

%check
appstream-util validate-relax --nonet %{buildroot}/%{_datadir}/appdata/*.appdata.xml

%files -f tqslapp.lang
%license LICENSE.txt
%doc AUTHORS.txt README
%{_bindir}/tqsl
%{_datadir}/applications/tqsl.desktop
%{_datadir}/appdata/tqsl.appdata.xml
%{_datadir}/icons/hicolor/*/apps/TrustedQSL.png
%{_datadir}/pixmaps/TrustedQSL.png
%{_datadir}/TrustedQSL
%{_mandir}/man5/*.5*

%files -n %{libname}
%doc src/LICENSE src/ChangeLog.txt
%{_libdir}/libtqsllib.so.%{major}*

%files -n %{devname}
%{_includedir}/*
%{_libdir}/libtqsllib.so
