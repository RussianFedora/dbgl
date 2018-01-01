%global debug_package %{nil}

Name:           dbgl
Summary:        DOSBox Game Launcher
URL:            http://home.quicknet.nl/qn/prive/blankendaalr/dbgl/
Version:        0.82
Release:        1%{?dist}
License:        GPLv2
BuildRequires:  ant
BuildRequires:  eclipse-swt
BuildRequires:  hsqldb
#BuildRequires:  jpackage-utils
#BuildRequires:  p7zip
#BuildRequires:  unzip
#BuildRequires:  xerces-j2
#BuildRequires:  liboil
BuildRequires:  desktop-file-utils
BuildRequires:  java-devel
BuildRequires:  apache-commons-lang3
BuildRequires:  apache-commons-io
BuildRequires:  libappstream-glib
#BuildRequires:  jersey
#BuildRequires:  glassfish-jax-rs-api
#BuildRequires:  glassfish-hk2-utils
#BuildRequires:  glassfish-hk2-configuration
#BuildRequires:  glassfish-hk2-metadata-generator
#BuildRequires:  glassfish-hk2-hk2
Requires:       dosbox >= 0.70
Requires:       eclipse-swt
Requires:       hsqldb
Requires:       java >= 1:1.7.0
Requires:       java-headless >= 1:1.7.0
Requires:       jpackage-utils
Requires:       SDL_net
Requires:       SDL_sound
Source0:        http://members.quicknet.nl/blankendaalr/dbgl/download/src082.zip
Source1:        dbgl.desktop
Source2:        dbgl.appdata.xml

%description
DBGL is a Java front-end for DOSBox, based largely upon the proven
interface of D-Fend.
The front-end is by no means finished. It is a work in progress
and lacking many features, but the core is working, and I think
the product is somewhat usable as it is. Please bear in mind that
the interface is still quite rough around the edges.

%prep
%setup -qc
# remove bundles
# swt
rm -rf ./src/dist/linuxshared/lib
rm -rf ./src/dist/*/DOSBox-0.74
rm -r ./src/dist/shared/lib/hsqldb.jar
rm -r ./src/dist/shared/lib/commons-lang3-3.5.jar
rm -r ./src/dist/shared/lib/commons-io-2.5.jar
# not easy unbundle jersey-2.13.jar fedora have jersey-2.18 and 2.23 seems that
# haven't org.glassfish.jersey.core.jersey-server
#rm -r ./src/dist/shared/lib/jersey-2.13.jar


%build
mkdir -p lib
build-jar-repository -p lib commons-lang3 hsqldb swt \
    commons-io
#    glassfish-jax-rs-api jersey glassfish-hk2-utils \
#    glassfish-hk2-configuration glassfish-hk2/hk2-metadata-generator \
#    glassfish-hk2-hk2

# fix build.xml to set jar classpath with (unbundle) system libraries
sed -i build.xml -e s'#excludes="swt\*.jar"#excludes="swt*.jar \
    commons-io*.jar commons-lang3*.jar hsqldb*.jar"#'
sed -i build.xml -e s'#class-path}#class-path} /usr/share/java/commons-io.jar \
    /usr/share/java/commons-lang3.jar /usr/share/java/hsqldb.jar \
    /usr/lib/java/swt.jar#'
#cat build.xml
ant distlinux

%install
install -dm 755 %{buildroot}%{_javadir}/%{name}/
%ifarch x86_64
    tar xvf dist/dbgl082_64bit.tar.gz -C %{buildroot}%{_javadir}/%{name}/
%else
    %ifarch %{ix86}
        tar xvf dist/dbgl082.tar.gz -C %{buildroot}%{_javadir}/%{name}/
    %else
        tar xvf dist/dbgl082_generic.tar.gz -C %{buildroot}%{_javadir}/%{name}/
    %endif
%endif

# use symbol links to system libraries
#build-jar-repository -s -p %{buildroot}/%{_javadir}/%{name}/lib commons-io \
#    commons-lang3 hsqldb swt

# startscript
mkdir -p %{buildroot}%{_bindir}
pushd %{buildroot}%{_bindir}
ln -s %{_javadir}/%{name}/dbgl
popd

# icons
mkdir %{buildroot}%{_datadir}/pixmaps
mv %{buildroot}%{_javadir}/%{name}/dbgl.png %{buildroot}%{_datadir}/pixmaps/

# menu
mkdir -p %{buildroot}%{_datadir}/applications
desktop-file-install                               \
--dir=%{buildroot}%{_datadir}/applications         \
%{SOURCE1}

install -D -p -m 0644 %{SOURCE2} \
    %{buildroot}%{_datadir}/appdata/%{name}.appdata.xml

%check
appstream-util validate-relax --nonet \
    %{buildroot}%{_datadir}/appdata/%{name}.appdata.xml

%files
%{_bindir}/%{name}
%{_javadir}/%{name}
%{_datadir}/pixmaps/*.png
%{_datadir}/applications/%{name}.desktop
%{_datadir}/appdata/%{name}.appdata.xml

%changelog
* Mon Nov 06 2017 Sérgio Basto <sergio@serjux.com> - 0.82-1
- Updated to 0.82

* Thu Mar 09 2017 Sérgio Basto <sergio@serjux.com> - 0.81-1
- Update to 0.81

* Fri Dec 23 2016 Sérgio Basto <sergio@serjux.com> - 0.80-3
- set jar classpath with (unbundle) system libraries (instead use symbol links)
- gnatenkobrain review:
  - btw, you can remove / between %{buildroot} and others.
  - probably you meant %{ix86}
  - to %check please

* Mon Dec 19 2016 Sérgio Basto <sergio@serjux.com> - 0.80-2
- Bump release
- Use external .desktop file easier to send to upstream
- Add Packaging:AppData

* Fri Jun 17 2016 Oleg Kishinskiy <legunt@yandex.ru> - 0.80-1
- Update for new vertion

* Fri Mar 20 2015 Oleg Kishinskiy <legunt@yandex.ru> - 0.79-3
- add ant for BuildRequires

* Fri Mar 20 2015 Oleg Kishinskiy <legunt@yandex.ru> - 0.79-2
- FIX change category

* Fri Mar 20 2015 Oleg Kishinskiy <legunt@yandex.ru> - 0.79-1
- update for new vertion
- change category

* Tue Dec 23 2014 Oleg Kishinskiy <legunt@yandex.ru> - 0.78-3
- fix spec to install from source

* Wed Dec 10 2014 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 0.78-2
- spec cleanup

* Wed Dec 10 2014 Oleg Kishinskiy <legunt@yandex.ru> - 0.78-1
- Update for new vertion

* Mon Jul 29 2013 David Vásquez <davidjeremias82 AT gmail DOT com> - 0.76-2
- Initial build rpm 
