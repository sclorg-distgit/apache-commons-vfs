%{?scl:%scl_package apache-commons-vfs}
%{!?scl:%global pkg_name %{name}}

# hadoop was retired
%bcond_without hadoop
%bcond_without ftp
%bcond_without ssh

Name:          %{?scl_prefix}apache-commons-vfs
Version:       2.1
Release:       10.1%{?dist}
Summary:       Commons Virtual File System
License:       ASL 2.0
Url:           http://commons.apache.org/vfs/
Source0:       http://www.apache.org/dist/commons/vfs/source/commons-vfs-%{version}-src.tar.gz

BuildRequires:  %{?scl_prefix}maven-local
BuildRequires:  %{?scl_prefix}mvn(commons-httpclient:commons-httpclient)
BuildRequires:  %{?scl_prefix}mvn(commons-logging:commons-logging)
BuildRequires:  %{?scl_prefix}mvn(commons-net:commons-net)
BuildRequires:  %{?scl_prefix}mvn(org.apache.ant:ant)
BuildRequires:  %{?scl_prefix}mvn(org.apache.commons:commons-collections4)
BuildRequires:  %{?scl_prefix}mvn(org.apache.commons:commons-compress)
BuildRequires:  %{?scl_prefix}mvn(org.apache.commons:commons-parent:pom:)
BuildRequires:  %{?scl_prefix}mvn(org.apache.maven.plugins:maven-antrun-plugin)
%if %{with hadoop}
BuildRequires:  mvn(org.apache.hadoop:hadoop-common)
BuildRequires:  mvn(org.apache.hadoop:hadoop-hdfs)
%endif
%if %{with ssh}
BuildRequires:  %{?scl_prefix}mvn(com.jcraft:jsch)
%endif
%if %{with ftp}
BuildRequires:  mvn(org.apache.ftpserver:ftpserver-core)
%endif

BuildArch:     noarch
Provides:      %{name}2 = %{version}-%{release}

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

%description examples
VFS is a Virtual File System library - Examples.

%package project
Summary:       Commons VFS Parent POM

%description project
Commons VFS Parent POM.

%package javadoc
Summary:       Javadoc for %{pkg_name}

%description javadoc
This package contains javadoc for %{pkg_name}.

%prep
%setup -q -n commons-vfs-%{version}

%pom_remove_plugin :apache-rat-plugin

# Convert from dos to unix line ending
for file in LICENSE.txt NOTICE.txt README.txt RELEASE-NOTES.txt; do
 sed -i.orig 's|\r||g' $file
 touch -r $file.orig $file
 rm $file.orig
done

# Disable unwanted module
%pom_disable_module dist

# Fix ant gId
%pom_change_dep -r :ant org.apache.ant:
# Upadate bouncycastle aId
%pom_change_dep -r :bcprov-jdk16 :bcprov-jdk15on

# Remove unwanted dependency jackrabbit-{standalone,webdav}
%pom_remove_dep -r org.apache.jackrabbit:

rm -rf core/src/{main,test}/java/org/apache/commons/vfs2/provider/webdav

# Use old version of sshd-core
%pom_remove_dep -r :sshd-core

# hadoop has been retired
%if %{without hadoop}
%pom_remove_dep -r org.apache.hadoop
rm -r core/src/{main,test}/java/org/apache/commons/vfs2/provider/hdfs
%endif

# not really needed
%pom_remove_plugin :maven-checkstyle-plugin
%pom_remove_plugin :findbugs-maven-plugin

%if %{without ssh}
%pom_remove_dep -r :jsch
rm -r core/src/{main,test}/java/org/apache/commons/vfs2/provider/sftp
rm examples/src/main/java/org/apache/commons/vfs2/libcheck/SftpCheck.java
%endif

%if %{without ftp}
%pom_remove_dep -r :ftpserver-core
rm -r core/src/{main,test}/java/org/apache/commons/vfs2/provider/ftps
%endif


# Fix installation directory and symlink
%mvn_file :commons-vfs2 %{pkg_name}
%mvn_file :commons-vfs2 %{pkg_name}2
%mvn_file :commons-vfs2 commons-vfs
%mvn_file :commons-vfs2 commons-vfs2
%mvn_file :commons-vfs2-examples %{pkg_name}-examples
%mvn_file :commons-vfs2-examples %{pkg_name}2-examples
%mvn_file :commons-vfs2-examples commons-vfs-examples
%mvn_file :commons-vfs2-examples commons-vfs2-examples

%mvn_alias :commons-vfs2 "org.apache.commons:commons-vfs" "commons-vfs:commons-vfs"
%mvn_alias :commons-vfs2-examples "org.apache.commons:commons-vfs-examples" "commons-vfs:commons-vfs-examples"

%build
%mvn_build -sf

%install
%mvn_install

mkdir -p %{buildroot}%{_sysconfdir}/ant.d
echo "ant commons-logging commons-vfs" > commons-vfs
install -p -m 644 commons-vfs %{buildroot}%{_sysconfdir}/ant.d/commons-vfs

%files -f .mfiles-commons-vfs2
%doc README.txt RELEASE-NOTES.txt
%license LICENSE.txt NOTICE.txt

%files examples -f .mfiles-commons-vfs2-examples

%files project -f .mfiles-commons-vfs2-project
%license LICENSE.txt NOTICE.txt

%files javadoc -f .mfiles-javadoc
%license LICENSE.txt NOTICE.txt

%files ant
%config %{_sysconfdir}/ant.d/commons-vfs

%changelog
* Wed Jun 21 2017 Java Maintainers <java-maint@redhat.com> - 2.1-10.1
- Automated package import and SCL-ization

* Mon Feb 06 2017 Michael Simacek <msimacek@redhat.com> - 2.1-10
- Add conditionals for ftp and ssh

* Mon Feb 06 2017 Michael Simacek <msimacek@redhat.com> - 2.1-9
- Remove rat-plugin

* Sun Jan 29 2017 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.1-8
- Fix hadoop build conditionals

* Fri Oct 28 2016 gil cattaneo <puntogil@libero.it> 2.1-7
- enable HDFS support (rhbz#1387108)

* Mon Oct  3 2016 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.1-6
- Remove build-requires on perl

* Thu Jul 21 2016 gil cattaneo <puntogil@libero.it> 2.1-5
- add missing BR

* Sat Jun 25 2016 gil cattaneo <puntogil@libero.it> 2.1-4
- disable tests failure

* Thu Jun 02 2016 gil cattaneo <puntogil@libero.it> 2.1-3
- disable hadoop stuff with bcond

* Thu Jun 02 2016 Michael Simacek <msimacek@redhat.com> - 2.1-2
- Remove support for retired hadoop

* Sun May 22 2016 gil cattaneo <puntogil@libero.it> 2.1-1
- update to 2.1

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.0-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Jan 29 2015 gil cattaneo <puntogil@libero.it> 2.0-15
- introduce license macro

* Wed Jul 30 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.0-14
- Fix build-requires on apache-commons-parent

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Mar 04 2014 Stanislav Ochotnicky <sochotnicky@redhat.com> - 2.0-12
- Use Requires: java-headless rebuild (#1067528)

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Jun 28 2013 gil cattaneo <puntogil@libero.it> 2.0-10
- used pom_xpath_set macro

* Fri Jun 28 2013 gil cattaneo <puntogil@libero.it> 2.0-9
- swith to pom macros
- packaged in /usr/share/java instead of /usr/share/java/apache-commons-vfs

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
