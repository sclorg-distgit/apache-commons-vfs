%global pkg_name apache-commons-vfs
%{?scl:%scl_package %{pkg_name}}
%{?maven_find_provides_and_requires}

%global base_name vfs
%global short_name commons-%{base_name}
Name:          %{?scl_prefix}%{pkg_name}
Version:       2.0
Release:       11.12%{?dist}
Summary:       Commons Virtual File System
License:       ASL 2.0
Url:           http://commons.apache.org/%{base_name}/
Source0:       http://www.apache.org/dist/commons/%{base_name}/source/%{short_name}-%{version}-src.tar.gz
# add maven-compiler-plugin configuration
# fix ant gId
# remove/disable jackrabbit-webdav support
# remove org.apache.commons commons-build-plugin
# remove org.codehaus.mojo findbugs-maven-plugin
# remove maven-scm
# remove old vfs stuff
Patch0:        %{pkg_name}-%{version}-build.patch

BuildRequires:  %{?scl_prefix_java_common}maven-local
BuildRequires:  %{?scl_prefix_java_common}mvn(com.jcraft:jsch)
BuildRequires:  %{?scl_prefix_java_common}mvn(commons-collections:commons-collections)
BuildRequires:  %{?scl_prefix_java_common}mvn(commons-httpclient:commons-httpclient)
BuildRequires:  %{?scl_prefix_java_common}mvn(commons-logging:commons-logging)
BuildRequires:  %{?scl_prefix_java_common}mvn(commons-net:commons-net)
BuildRequires:  %{?scl_prefix_java_common}mvn(org.apache.ant:ant)
BuildRequires:  %{?scl_prefix_java_common}mvn(org.apache.commons:commons-compress)
BuildRequires:  %{?scl_prefix_java_common}mvn(org.jdom:jdom)
BuildRequires:  %{?scl_prefix}mvn(org.apache.commons:commons-parent:pom:) >= 26-7
BuildRequires:  %{?scl_prefix}mvn(org.apache.maven.plugins:maven-antrun-plugin)

# test deps
BuildRequires:  %{?scl_prefix_java_common}mvn(junit:junit)

BuildArch:     noarch

%description
Commons VFS provides a single API for accessing various
different file systems. It presents a uniform view of the
files from various different sources, such as the files on
local disk, on an HTTP server, or inside a Zip archive.
Some of the features of Commons VFS are:
* A single consistent API for accessing files of different
 types.
* Support for numerous file system types.
* Caching of file information. Caches information in-JVM,
 and optionally can cache remote file information on the
 local file system.
* Event delivery.
* Support for logical file systems made up of files from
 various different file systems.
* Utilities for integrating Commons VFS into applications,
 such as a VFS-aware ClassLoader and URLStreamHandlerFactory.
* A set of VFS-enabled Ant tasks.

%package ant
Summary:       Development files for Commons VFS
Requires:      %{name} = %{version}-%{release}

%description ant
This package enables support for the Commons VFS ant tasks.

%package examples
Summary:       Commons VFS Examples
Requires:      %{name} = %{version}-%{release}

%description examples
VFS is a Virtual File System library - Examples.

%package javadoc
Summary:       Javadoc for %{pkg_name}

%description javadoc
This package contains javadoc for %{pkg_name}.

%prep
%setup -q -n %{short_name}-%{version}
%{?scl:scl enable %{scl_java_common} %{scl_maven} %{scl} - <<"EOF"}
set -e -x
perl -pi -e 's/\r$//g;' *.txt

%patch0 -p1
rm -rf core/src/main/java/org/apache/commons/vfs2/provider/webdav
rm -rf core/src/test/java/org/apache/commons/vfs2/provider/webdav
sed -i 's|"webdav",||' core/src/test/java/org/apache/commons/vfs2/util/DelegatingFileSystemOptionsBuilderTest.java

sed -i "s|<module>dist</module>|<!--module>dist</module-->|" pom.xml

# not really needed
%pom_remove_plugin :maven-checkstyle-plugin

%mvn_alias :commons-vfs2 "org.apache.commons:%{short_name}" "%{short_name}:%{short_name}"
%mvn_alias :commons-vfs2-examples "org.apache.commons:%{short_name}-examples" "%{short_name}:%{short_name}-examples"

# main package wins parent POM
%mvn_package ":commons-vfs2-project" commons-vfs2
%{?scl:EOF}

%build
%{?scl:scl enable %{scl_java_common} %{scl_maven} %{scl} - <<"EOF"}
set -e -x
%mvn_build -s
%{?scl:EOF}

%install
%{?scl:scl enable %{scl_java_common} %{scl_maven} %{scl} - <<"EOF"}
set -e -x
%mvn_install

mkdir -p %{buildroot}%{_sysconfdir_java_common}/ant.d
echo "ant commons-logging %{short_name}" > %{short_name}
install -p -m 644 %{short_name} %{buildroot}%{_sysconfdir_java_common}/ant.d/%{short_name}
%{?scl:EOF}


%files -f .mfiles-commons-vfs2
%dir %{_mavenpomdir}/%{pkg_name}
%dir %{_javadir}/%{pkg_name}
%doc LICENSE.txt NOTICE.txt README.txt RELEASE-NOTES.txt

%files examples -f .mfiles-commons-vfs2-examples

%files javadoc -f .mfiles-javadoc
%doc LICENSE.txt NOTICE.txt

%files ant
%config %{_sysconfdir_java_common}/ant.d/%{short_name}

%changelog
* Thu Jan 15 2015 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.0-11.12
- Install ant.d files into rh-java-common's ant.d

* Thu Jan 15 2015 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.0-11.11
- Add directory ownership on %%{_mavenpomdir} subdir

* Tue Jan 13 2015 Michael Simacek <msimacek@redhat.com> - 2.0-11.10
- Mass rebuild 2015-01-13

* Mon Jan 12 2015 Michael Simacek <msimacek@redhat.com> - 2.0-11.9
- Fix parent pom BR
- BR packages from common collection

* Mon Jan 12 2015 Michael Simacek <msimacek@redhat.com> - 2.0-11.8
- Rebuild to regenerate requires from java-common

* Tue Jan 06 2015 Michael Simacek <msimacek@redhat.com> - 2.0-11.7
- Mass rebuild 2015-01-06

* Mon May 26 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.0-11.6
- Mass rebuild 2014-05-26

* Wed Feb 19 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.0-11.5
- Mass rebuild 2014-02-19

* Tue Feb 18 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.0-11.4
- Mass rebuild 2014-02-18

* Mon Feb 17 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.0-11.3
- SCL-ize build-requires

* Thu Feb 13 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.0-11.2
- Rebuild to regenerate auto-requires

* Tue Feb 11 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.0-11.1
- First maven30 software collection build

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 2.0-11
- Mass rebuild 2013-12-27

* Fri Sep 20 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.0-10
- Add BuildRequires on apache-commons-parent >= 26-7

* Fri Jun 28 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.0-9
- Rebuild to regenerate API documentation
- Resolves: CVE-2013-1571

* Fri Jun 28 2013 Michal Srb <msrb@redhat.com> - 2.0-8
- Fix directory ownership

* Thu Jun 27 2013 Michal Srb <msrb@redhat.com> - 2.0-7
- Build with XMvn
- Do not ignore test failures
- Fix BR

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Feb 06 2013 Java SIG <java-devel@lists.fedoraproject.org> - 2.0-5
- Update for https://fedoraproject.org/wiki/Fedora_19_Maven_Rebuild
- Replace maven BuildRequires with maven-local

* Wed Aug  1 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.0-4
- Rebuild against javamail

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jun 18 2012 gil cattaneo <puntogil@libero.it> 2.0-2
- add subpackage ant
- install NOTICE.txt in javadocs subpackage

* Mon May 14 2012 gil cattaneo <puntogil@libero.it> 2.0-1
- initial rpm
