%global		debug_package %{nil}
# The location of the installed extension
%global		loextdir %{_libdir}/libreoffice/share/extensions/Mendeley

Name:		mendeleydesktop
Version:	1.19.8
Release:	3%{?dist}
Epoch:		1
Summary:	Academic reference management software for researchers

License:	LGPLv2+ and Mendeley and MIT and CC-BY-SA and (CPAL or AGPLv3) and BSD
URL:		https://www.mendeley.com/
Source0:	https://desktop-download.mendeley.com/download/linux/%{name}-%{version}-linux-x86_64.tar.bz2
Source1:	https://desktop-download.mendeley.com/download/linux/%{name}-%{version}-linux-i486.tar.bz2
Source2:	%{name}.appdata.xml		
Source3:	%{name}-libreoffice.metainfo.xml
Patch0:		%{name}-desktopfile.patch

# Bundled Libraries
# share/mendeleydesktop/citationLocales CC-BY-SA 3.0 -> https://github.com/citation-style-language/locales
# share/mendeleydesktop/citationStyles-1.0 CC-BY-SA 3.0 -> https://github.com/citation-style-language/styles
Provides: bundled(citation-style-language)
# share/mendeleydesktop/citeproc-js/external/{citeproc,xmldom}.js CPAL/AGPLv3 -> https://bitbucket.org/fbennett/citeproc-js/wiki/Home
Provides: bundled(citeproc-js)
# share/mendeleydesktop/citeproc-js/external/md5.js BSD -> https://code.google.com/p/crypto-js/
Provides: bundled(crypto-js) = 3.1.2
# share/mendeleydesktop/citeproc-js/external/underscore-min.js MIT -> http://underscorejs.org
Provides: bundled(underscore-js) = 1.7.0
# share/mendeleydesktop/webContent/external/js/ICanHaz.js MIT -> http://icanhazjs.com
Provides: bundled(ICanHaz.js) = 0.10
# share/mendeleydesktop/webContent/external/js/jquery-1.9.0.min.js MIT -> https://jquery.com/
Provides: bundled(js-jquery1) = 1.9.0
# share/mendeleydesktop/webContent/external/js/jquery.dropdown.* MIT -> http://labs.abeautifulsite.net/jquery-dropdown/
Provides: bundled(js-jquery-dropdown) = 1.9.0
# share/mendeleydesktop/webContent/external/js/jquery.ioslist.js MIT -> https://brianhadaway.github.io/iOSList/
Provides: bundled(js-jquery-ioslist) = 1.9.0
# share/mendeleydesktop/webContent/external/js/throbber.js MIT -> https://aino.github.io/throbber.js/
Provides: bundled(throbber.js) = 0.1
# share/mendeleydesktop/citeproc-js/test/external/qunit-1.15.0.* MIT -> https://qunitjs.com/
Provides: bundled(qunit.js) = 1.15.0
# https://www.pdftron.com/pdfnet/downloads.html
Provides: bundled(PDFNetC) = 5.1
# bundled in libPDFNetC.so:
Provides: bundled(libpng) = 1.2.29
Provides: bundled(zlib) = 1.2.3
# bundled qt5 libraries otherwise conflicts occur
Provides: bundled(qt5-qtbase)

# Appstream data
BuildRequires: libappstream-glib

# Required to run the ui
BuildRequires:	desktop-file-utils
Requires:	hicolor-icon-theme
Requires:	qt5-qtbase-gui



# Needed to resolve shebang issue
BuildRequires:	pkgconfig(python3)

# Set exclusivity for x86 based architecture
ExclusiveArch:	x86_64

%description
Mendeley is a combination of a desktop application and a website which
helps you manage, share and discover both content and contacts in research.

Our software, Mendeley Desktop, offers you:
* Automatic extraction of document details (authors, title, journal etc.)
  from academic papers into a library database, which saves you a lot of
  manual typing! As more people use Mendeley, the quality of the data
  extraction improves.
* Super-efficient management of your papers: "Live" full-text search across
  all your papers – the results start to appear as you type! Mendeley
  Desktop also lets you filter your library by authors, journals or keywords.
  You can also use document collections, notes and tags to organize your
  knowledge, and export the document details in different citation styles.
* Sharing and synchronization of your library (or parts of it) with
  selected colleagues. This is perfect for jointly managing all the papers in
  your lab!
* More great features: A plug-in for citing your articles in Microsoft
  Word, OCR (image-to-text conversion, so you can full-text search all your
  scanned PDFs) and lots more new features being worked upon.

%package -n libreoffice-Mendeley
Summary: Insert citations and generate bibliography from Mendeley
License: ECL 1.0
Requires: %{name}%{?_isa} = %{?epoch}:%{version}-%{release}
Requires: libreoffice-core%{_isa}

%description -n libreoffice-Mendeley
This extension provides integration between Mendeley Desktop and
OpenOffice/LibreOffice, providing the ability to insert citations
from your Mendeley library into OpenOffice documents and generated
a bibliography automatically.

%prep
%ifarch i686
%autosetup -p1 -n %{name}-%{version}-linux-i486
%else
%autosetup -p1 -n %{name}-%{version}-linux-x86_64
%endif

#sed -i 's/Exec=/&env LD_LIBRARY_PATH=\/lib\/mendeleydesktop\/plugins\/platforms /' %%{_bindir}/install-mendeley-link-handler.sh

%build
# Remove the problematic icons 48x48 and 64x64 look bad because they have a white border
rm  -rf share/icons/hicolor/48x48
rm  -rf share/icons/hicolor/64x64

%install
mkdir -p %{buildroot}{%{_bindir},%{_datadir},%{_libdir}}

install -pm755 lib/lib{Mendeley.so.%{version},PDFNetC.so} %{buildroot}%{_libdir}/
install -Dpm755 lib/%{name}/libexec/%{name}.%{_target_cpu} %{buildroot}%{_bindir}/%{name}

cp -pr share/%{name} %{buildroot}%{_datadir}

ln -s /bin/true %{buildroot}%{_bindir}/install-mendeley-link-handler.sh

# Install hicolor icons
for s in `ls share/icons/hicolor` ; do
  install -Dpm644 {share/icons/hicolor,%{buildroot}%{_datadir}/icons/hicolor}/${s}/apps/%{name}.png
done

desktop-file-install  --vendor "" --dir %{buildroot}%{_datadir}/applications \
   --add-mime-type=application/pdf --add-mime-type=text/x-bibtex \
   share/applications/%{name}.desktop

# AppData
install -p -m 644 -D %{SOURCE2} %{buildroot}/%{_metainfodir}/%{name}.appdata.xml
install -p -m 644 -D %{SOURCE3} %{buildroot}/%{_metainfodir}/%{name}-libreoffice.metainfo.xml

# Libre office plugins
mkdir -p %{buildroot}%{loextdir}
pushd %{buildroot}%{_datadir}/%{name}
unzip -qq openOfficePlugin/Mendeley-%{version}.oxt -d %{buildroot}%{loextdir}
chmod 644 %{buildroot}%{loextdir}/{description.xml,Mendeley/*.xba}
chmod 755 %{buildroot}%{loextdir}/Scripts/MendeleyDesktopAPI.py
# Fix Python shebangs 
%py3_shebang_fix %{buildroot}%{loextdir}/Scripts/MendeleyDesktopAPI.py
rm -r openOfficePlugin
popd

%ldconfig_scriptlets

%check
appstream-util validate-relax --nonet %{buildroot}/%{_metainfodir}/%{name}.appdata.xml
appstream-util validate-relax --nonet %{buildroot}/%{_metainfodir}/%{name}-libreoffice.metainfo.xml

%files
%license LICENSE
%doc README
%{_bindir}/%{name}
%{_bindir}/install-mendeley-link-handler.sh
%{_libdir}/libPDFNetC.so
%{_libdir}/libMendeley.so.*
%{_datadir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/*/apps/%{name}.png
%{_metainfodir}/%{name}.appdata.xml

%files -n libreoffice-Mendeley
%license share/%{name}/openOfficePlugin/EducationalCommunityLicense.txt
%{loextdir}
%{_metainfodir}/%{name}-libreoffice.metainfo.xml

%changelog
* Sun Feb 04 2024 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 1:1.19.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Aug 03 2023 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 1:1.19.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Sat Dec 10 2022 Sérgio Basto <sergio@serjux.com> - 1:1.19.8-1
- Update mendeleydesktop to 1.19.8

* Mon Aug 08 2022 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 1:1.19.4-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild and ffmpeg
  5.1

* Thu Feb 10 2022 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 1:1.19.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Aug 04 2021 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 1:1.19.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Thu Feb 04 2021 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 1:1.19.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Thu Aug 27 2020 Leigh Scott <leigh123linux@gmail.com> - 1:1.19.4-2
- Add missing epoch to the requires

* Mon Aug 24 2020 Luya Tshimbalanga <luya_tfz@thefinalzone.net> - 1:1.19.4-1
- Revert to 1.19.4 using epoch

* Wed Aug 19 2020 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 1.19.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Sat May 09 2020 Luya Tshimbalanga <luya_tfz@thefinalzone.net> - 1.19.6-1
- Update to 1.19.6

* Wed Feb 05 2020 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 1.19.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sat Aug 10 2019 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 1.19.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jun 06 2019 Luya Tshimbalanga <luya_tfz@thefinalzone.net> - 1.19.4-2
- Set ExclusiveArch to x86_64 due to failure of build system

* Thu Jun 06 2019 Luya Tshimbalanga <luya_tfz@thefinalzone.net> - 1.19.4-1
- Update to 1.19.4
- Remove conditional statement for ExclusiveArch

* Mon Feb 18 2019 Luya Tshimbalanga <luya_tfz@thefinalzone.net> - 1.19.3-2
- Fix from rpmfusion bugzilla #4041 suggested by Dominik 'Rathann' Mierzejewski
- Drop qt5-qtstyleplugins dependency as requirement
- Drop redundant pathfix.py from build requirement
- Use modern macro for desktop-utils path

* Mon Feb 18 2019 Luya Tshimbalanga <luya_tfz@thefinalzone.net> - 1.19.3-1
- Updated to 1.19.3
- Reenable patch for desktop file
- Set exclusivity for both 32 and 64 bits x86 architectures

* Sun Oct 21 2018 Luya Tshimbalanga <luya_tfz@thefinalzone.net> - 1.19.2-1
- Updated to 1.19.2
- Modernized spec
- Drop patch 

* Thu Apr 12 2018 Mark Harfouche <mark.harfouche@gmail.com> - 1.17.13-2
- ldconfig_scriptlets
- Removed desktopfiles post and postun

* Thu Feb 15 2018 Philipp Jaeger <p@pj4e.de> - 1.17.13
- Updated to 1.17.13

* Tue Nov 14 2017 Mark Harfouche <mark.harfouche@gmail.com> - 1.17.12
- Updated to 1.17.12

* Tue Nov 14 2017 Mark Harfouche <mark.harfouche@gmail.com> - 1.17.11-1
- rebuilt

* Sat Aug 5 2017 Mark Harfouche <mark.harfouche@gmail.com> - 1.17.10
- New upstream version

* Fri Aug 4 2017 Mark Harfouche <mark.harfouche@gmail.com> - 1.17.8-3
- Added more info about bundled libraries (Thanks Dominik Mierzejewski)

* Fri Aug 4 2017 Mark Harfouche <mark.harfouche@gmail.com> - 1.17.8-2
- Removed devel and 32 bit support

* Wed Feb 22 2017 Mark Harfouche <mark.harfouche@gmail.com> - 1.17.8
- New upstream version

* Mon Jan 23 2017 Mark Harfouche <mark.harfouche@gmail.com> - 1.17.6-3
- rebuilt

* Sun Jan 22 2017 Mark Harfouche <mark.harfouche@gmail.com> - 1.17.6-2
- Merged  Dominik Mierzejewski <rpm@greysector.net>'s rpm file into this one.
  https://rathann.fedorapeople.org/review/mendeleydesktop/

* Sun Jan 22 2017 Mark Harfouche <mark.harfouche@gmail.com> - 1.17.6
- Updated to Mendeley 1.17.6

* Tue Oct 18 2016 Mark Harfouche <mark.harfouche@gmail.com> - 1.17
- Updated to Mendeley 1.17

* Mon Apr 25 2016 Mark Harfouche <mark.harfouche@gmail.com> - 1.16.1-2
- More compliant with rpmlint

* Wed Apr 6 2016 Mark Harfouche <mark.harfouche@gmail.com> - 1.16.1
- Updated to Mendeley 1.16.1

* Mon Feb 22 2016 Mark Harfouche <mark.harfouche@gmail.com> - 1.15.3
- Updated to Mendeley 1.15.3

* Tue Dec 8 2015 Mark Harfouche <mark.harfouche@gmail.com> - 1.15.2
- Updated to Mendeley 1.15.2

* Wed Oct 14 2015 Mark Harfouche <mark.harfouche@gmail.com> - 1.15
- Updated to Mendeley 1.15

* Wed Jul 08 2015 Mark Harfouche <mark.harfouche@gmail.com> - 1.14-2
- modified the patch, they changed the exec string

* Wed Jul 8 2015 Mark Harfouche - 1.14-1
- Updated to Mendeley 1.14

* Fri Apr 10 2015 Mark Harfouche - 1.13.8-1
- Updated to Mendeley 1.13.8

* Tue Mar 31 2015 Mark Harfouche - 1.13.6-1
- Updated to Mendeley 1.13.6

* Wed Mar 04 2015 Alexander Korsunsky <fat.lobyte9@gmail.com> - 1.13.4-2
- Allow building in Mock

* Mon Feb 23 2015 Alexander Korsunsky <fat.lobyte9@gmail.com> - 1.13.4-1
- Updated to Mendeley 1.13.4

* Mon Jan 12 2015 Mark Harfouche - 1.12.4-1
- Updated to Mendeley 1.12.4

* Tue Sep 02 2014 Mark Harfouche - 1.12.1-1
- Updated to Mendeley 1.12.1

* Wed Oct 9 2013 Mark Harfouche - 1.10.1-1
- Updated to Mendeley 1.10.1

* Wed Aug 14 2013 Mark Harfouche - 1.9.2-1
- Updated to Mendeley 1.9.2

* Sun Jul 14 2013 Mark Harfouche - 1.9.1-18
- Commented out the sensitive line

* Sun Jul 14 2013 Mark Harfouche - 1.9.1-17
- Moved the modification of the binary to the prep section like the other patch

* Sun Jul 14 2013 Mark Harfouche - 1.9.1-16
- Touched up the files section so as not to include other programs directories

* Sun Jul 14 2013 Mark Harfouche - 1.9.1-15
- Changed the mendeley binary to inhibit the execution of the link-handler
  script.

* Sun Jul 14 2013 Mark Harfouche - 1.9.1-14
- Fixed the location of the documentation

* Sun Jul 14 2013 Mark Harfouche - 1.9.1-13
- Added the /sbin/ldconfig lines to the post and postrun sections

* Sat Jul 13 2013 Mark Harfouche - 1.9.1-12
- Spec file should be i686 compatible

* Sat Jul 13 2013 Mark Harfouche - 1.9.1-11
- Removed the 48x48 and 64x64 icons because they looked bad (they used white
  instead of alpha making them look horrible)

* Sat Jul 13 2013 Filipe Manco - 1.9.1-10
- Cleanup spec file.

* Sat Jul 13 2013 Filipe Manco - 1.9.1-9
- Greatly simplify spec file.

* Sat Jul 13 2013 Mark Harfouche - 1.9.1-8
- Fixed the .desktop file so that it would have the option --unix-distro-build
  at the end of the exec command

* Sat Jul 13 2013 Mark Harfouche - 1.9.1-7
- I dont think we need the dummy launcher, mendeley seems to run well without
  it, so I moved the executable from libexec to bin

* Sat Jul 13 2013 Mark Harfouche - 1.9.1-6
- Changed the name of the desktopfile to reflect the correct name of the wmclass

* Sat Jul 13 2013 Mark Harfouche - 1.9.1-5
- Removed the explicit dependencies since I think the packager finds them
  automatically

* Sat Jul 13 2013 Mark Harfouche - 1.9.1-4
- Changed the libexec name to mendeleydestop as suggested in Revision 2 but
  added the appropriate modifications to the spec file.

* Sat Jul 13 2013 Mark Harfouche - 1.9.1-3
- Undid the modifications of the previous version

* Fri Jul 12 2013 Filipe Manco - 1.9.1-2
- Binary use mendeleydesktop instead of mendelydesktop.x86_64

* Fri Jul 12 2013 Filipe Manco - 1.9.1-1
- Update to Mendeley version 1.9.1

* Sun Apr 7 2013 Chris Fallin - 1.8.4-1
- Updated to Mendeley version 1.8.4

* Thu Mar 21 2013 Chris Fallin - 1.8.3-1
- Updated to Mendeley version 1.8.3

* Wed Mar 13 2013 Mark Harfouche - 1.8.2-2
- Cleaned up the spec file

* Wed Mar 13 2013 Chris Fallin - 1.8.2-1
- Updated to Mendeley version 1.8.2

* Thu Jan 31 2013 Mark Harfouche - 1.8.0-1
- Updated to Mendeley version 1.8.0

* Tue Jan 22 2013 Mark Harfouche - 0.1.0-2
- Fixed the dependency for libpng.so.3

