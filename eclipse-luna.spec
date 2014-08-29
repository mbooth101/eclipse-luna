%global scl eclipse-luna
%scl_package %scl

%global __requires_exclude ^%{scl_runtime}$

Name:      %{scl_name}
Version:   1.0
Release:   12%{?dist}
Summary:   The Eclipse Luna Software Collection
License:   EPL
URL:       http://copr.fedoraproject.org/coprs/mbooth/%{scl}/
BuildArch: noarch

Source0:   http://www.eclipse.org/legal/epl-v10.html

# Standard SCL build requirements
BuildRequires: scl-utils
BuildRequires: scl-utils-build

# This is needed for java directory macros
BuildRequires: javapackages-tools

# List everything in the SCL here so that installation of only the metapackage brings in
# everything we need
Requires: %{scl_name}-release
Requires: %{scl_name}-runtime
Requires: %{scl_name}-eclipse-pde
Requires: %{scl_name}-eclipse-jdt
Requires: %{scl_name}-eclipse-jgit
Requires: %{scl_name}-eclipse-egit
Requires: %{scl_name}-eclipse-egit-mylyn
Requires: %{scl_name}-eclipse-subclipse
Requires: %{scl_name}-eclipse-subclipse-graph
Requires: %{scl_name}-eclipse-collabnet-merge
Requires: %{scl_name}-eclipse-cdt
Requires: %{scl_name}-eclipse-cdt-parsers
Requires: %{scl_name}-eclipse-cdt-llvm
Requires: %{scl_name}-eclipse-mylyn-builds-hudson
Requires: %{scl_name}-eclipse-mylyn-context-cdt
Requires: %{scl_name}-eclipse-mylyn-context-java
Requires: %{scl_name}-eclipse-mylyn-context-pde
Requires: %{scl_name}-eclipse-mylyn-context-team
Requires: %{scl_name}-eclipse-mylyn-docs-epub
Requires: %{scl_name}-eclipse-mylyn-docs-htmltext
Requires: %{scl_name}-eclipse-mylyn-docs-wikitext
Requires: %{scl_name}-eclipse-mylyn-ide
Requires: %{scl_name}-eclipse-mylyn-tasks-bugzilla
Requires: %{scl_name}-eclipse-mylyn-tasks-trac
Requires: %{scl_name}-eclipse-mylyn-tasks-web
Requires: %{scl_name}-eclipse-mylyn-versions-cvs
Requires: %{scl_name}-eclipse-mylyn-versions-git
Requires: %{scl_name}-eclipse-mylyn-versions-subclipse
Requires: %{scl_name}-eclipse-changelog
Requires: %{scl_name}-eclipse-gcov
Requires: %{scl_name}-eclipse-gprof
Requires: %{scl_name}-eclipse-linuxtools
Requires: %{scl_name}-eclipse-manpage
Requires: %{scl_name}-eclipse-oprofile
Requires: %{scl_name}-eclipse-perf
Requires: %{scl_name}-eclipse-quickrex
Requires: %{scl_name}-eclipse-rpm-editor
Requires: %{scl_name}-eclipse-shelled
Requires: %{scl_name}-eclipse-systemtap
Requires: %{scl_name}-eclipse-testng
Requires: %{scl_name}-eclipse-valgrind
Requires: %{scl_name}-eclipse-webtools-common
Requires: %{scl_name}-eclipse-webtools-dali
Requires: %{scl_name}-eclipse-webtools-javaee
Requires: %{scl_name}-eclipse-webtools-jsf
Requires: %{scl_name}-eclipse-webtools-servertools
Requires: %{scl_name}-eclipse-webtools-sourceediting
Requires: %{scl_name}-eclipse-webtools-webservices

%description
Meta-package that will install everything needed to use the %{scl}
Software Collection.

%package   release
Summary:   Repository configuration for the %{scl} Software Collection
Requires:  fedora-release = 20

%description release
Yum repository configuration for keeping the %{scl} Software Collection
up to date.

%package   runtime
Summary:   Runtime scripts for the %{scl} Software Collection
Requires:  scl-utils

%description runtime
Essential runtime scripts for working with the %{scl} Software
Collection.

%package   build
Summary:   Build configuration the %{scl} Software Collection
Requires:  scl-utils-build
Requires:  %{scl_name}-runtime

# We require java 8 to build some parts of eclipse, but the java 8 packages in Fedora 20 do not provide
# "java" or "java-devel" so java 7 always gets pulled into the build root
# This is a problem because java 7 has a higher priority than java 8 so java 7 is used at build time
# instead of 8
# We work around this by pulling in java 8 here and providing "java" or "java-devel" so that
# we always have the correct version of java when building packages for the scl
Requires:  java-1.8.0-openjdk
Requires:  java-1.8.0-openjdk-devel
Provides:  java = 1:1.8.0
Provides:  java-devel = 1:1.8.0

%description build
Essential build configuration macros for building the %{scl}
Software Collection.

%prep
%setup -c -T
cp -p %{SOURCE0} .

%build
# Yum repository configuration
cat <<EOF >%{scl}.repo
[mbooth-%{scl}]
name=The %{scl} Software Collection for Fedora \$releasever
baseurl=http://copr-be.cloud.fedoraproject.org/results/mbooth/%{scl}/fedora-\$releasever-\$basearch/
skip_if_unavailable=True
gpgcheck=0
enabled=1
EOF

# Enable collection script
cat <<EOF >enable
# General variables
export PATH=%{_bindir}\${PATH:+:\${PATH}}
export MANPATH=%{_mandir}:\${MANPATH}
export INFOPATH=%{_infodir}\${INFOPATH:+:\${INFOPATH}}

# Needed by Java Packages Tools to locate java.conf
export JAVACONFDIRS="%{_sysconfdir}/java:\${JAVACONFDIRS:-/etc/java}"

# Required by XMvn to locate its configuration files
export XDG_CONFIG_DIRS="%{_sysconfdir}/xdg:\${XDG_CONFIG_DIRS:-/etc/xdg}"

# Required to locate shared libs inside the collection
export LD_LIBRARY_PATH="%{_prefix}/lib:%{_prefix}/lib64${LD_LIBRARY_PATH:+:\$LD_LIBRARY_PATH}"
EOF

# Java configuration
cat <<EOF >java.conf
JAVA_LIBDIR=%{_javadir}
JNI_LIBDIR=%{_jnidir}
JVM_ROOT=%{_jvmdir}
EOF

# Ivy configuration
cat <<EOF >ivysettings.xml
<ivysettings>
  <settings defaultResolver="default"/>
  <resolvers>
    <filesystem name="%{scl}-public">
      <ivy pattern="\${ivy.conf.dir}/lib/[module]/apache-ivy-[revision].xml" />
      <artifact pattern="%{_datadir}/java/\[artifact].[ext]" />
    </filesystem>
    <filesystem name="public">
      <ivy pattern="\${ivy.conf.dir}/lib/[module]/apache-ivy-[revision].xml" />
      <artifact pattern="%{_root_datadir}/java/\[artifact].[ext]" />
    </filesystem>
    <chain name="main" dual="true">
      <resolver ref="%{scl}-public"/>
      <resolver ref="public"/>
    </chain>
  </resolvers>
  <include url="\${ivy.default.settings.dir}/ivysettings-local.xml"/>
  <include url="\${ivy.default.settings.dir}/ivysettings-default-chain.xml"/>
</ivysettings>
EOF

# XMvn configuration
cat <<EOF >configuration.xml
<?xml version="1.0" encoding="UTF-8"?>
<configuration>
  <resolverSettings>
    <prefixes>
      <prefix>/opt/rh/%{scl}/root</prefix>
    </prefixes>
  </resolverSettings>
  <installerSettings>
    <metadataDir>opt/rh/%{scl}/root/usr/share/maven-fragments</metadataDir>
  </installerSettings>
  <repositories>
    <repository>
      <id>%{scl}-resolve</id>
      <type>compound</type>
      <properties>
        <prefix>opt/rh/%{scl}/root</prefix>
        <namespace>%{scl}</namespace>
      </properties>
      <configuration>
        <repositories>
          <repository>base-resolve</repository>
        </repositories>
      </configuration>
    </repository>
    <repository>
      <id>resolve-system</id>
      <type>compound</type>
      <properties>
        <prefix>/</prefix>
      </properties>
      <configuration>
        <repositories>
          <repository>%{scl}-resolve</repository>
          <repository>base-resolve</repository>
        </repositories>
      </configuration>
    </repository>
    <repository>
      <id>install</id>
      <type>compound</type>
      <properties>
        <prefix>opt/rh/%{scl}/root</prefix>
        <namespace>%{scl}</namespace>
      </properties>
      <configuration>
        <repositories>
          <repository>base-install</repository>
        </repositories>
      </configuration>
    </repository>
    <repository>
      <id>install-raw-pom</id>
      <type>compound</type>
      <properties>
        <prefix>opt/rh/%{scl}/root</prefix>
        <namespace>%{scl}</namespace>
      </properties>
      <configuration>
        <repositories>
          <repository>base-raw-pom</repository>
        </repositories>
      </configuration>
    </repository>
    <repository>
      <id>install-effective-pom</id>
      <type>compound</type>
      <properties>
        <prefix>opt/rh/%{scl}/root</prefix>
        <namespace>%{scl}</namespace>
      </properties>
      <configuration>
        <repositories>
          <repository>base-effective-pom</repository>
        </repositories>
      </configuration>
    </repository>
  </repositories>
</configuration>
EOF

%install
%{scl_install}

install -d -m 755 %{buildroot}%{_root_sysconfdir}/yum.repos.d
install -p -m 644 %{scl}.repo %{buildroot}%{_root_sysconfdir}/yum.repos.d/

install -d -m 755 %{buildroot}%{_scl_scripts}
install -p -m 755 enable %{buildroot}%{_scl_scripts}/

install -d -m 755 %{buildroot}%{_sysconfdir}/java
install -p -m 644 java.conf %{buildroot}%{_sysconfdir}/java/

install -d -m 755 %{buildroot}%{_sysconfdir}/ivy
install -p -m 644 ivysettings.xml %{buildroot}%{_sysconfdir}/ivy/

install -d -m 755 %{buildroot}%{_sysconfdir}/xdg/xmvn
install -p -m 644 configuration.xml %{buildroot}%{_sysconfdir}/xdg/xmvn/

# Misc other directories we should also own
install -d -m 755 %{buildroot}%{_jnidir}
install -d -m 755 %{buildroot}%{_javadir}
install -d -m 755 %{buildroot}%{_javadocdir}
install -d -m 755 %{buildroot}%{_datadir}/appdata
install -d -m 755 %{buildroot}%{_datadir}/maven-effective-poms
install -d -m 755 %{buildroot}%{_datadir}/maven-fragments
install -d -m 755 %{buildroot}%{_datadir}/maven-poms

%files
# The base package is empty because it is a meta-package whose sole purpose
# is to install the whole software collection

%files release
%config(noreplace) %{_root_sysconfdir}/yum.repos.d/%{scl}.repo

%files runtime -f filesystem
%doc epl-v10.html
%{_sysconfdir}/java
%{_sysconfdir}/ivy
%{_jnidir}
%{_javadir}
%{_javadocdir}
%{_datadir}/appdata
%{_datadir}/maven-effective-poms
%{_datadir}/maven-fragments
%{_datadir}/maven-poms
%{scl_files}

%files build
%{_root_sysconfdir}/rpm/macros.%{scl}-config

%changelog
* Fri Aug 29 2014 Mat Booth <mat.booth@redhat.com> - 1.0-12
- Add requires for webtools to main metapackage

* Fri Aug 15 2014 Mat Booth <mat.booth@redhat.com> - 1.0-11
- Add LD_LIBRARY_PATH to collection enable script

* Wed Jul 30 2014 Mat Booth <mat.booth@redhat.com> - 1.0-10
- Add requires for TestNG/ShellEd to main metapackage

* Fri Jul 25 2014 Mat Booth <mat.booth@redhat.com> - 1.0-9
- Fix unowned man page directories
- Add requires for Mylyn/Linuxtools to main metapackage

* Tue Jul 22 2014 Mat Booth <mat.booth@redhat.com> - 1.0-8
- Add requires for Subclipse and CDT to main metapackage

* Thu Jul 17 2014 Mat Booth <mat.booth@redhat.com> - 1.0-7
- Add requires for PDE/JDT/JGit/EGit to main metapackage

* Mon Jul 14 2014 Mat Booth <mat.booth@redhat.com> - 1.0-6
- Fix directory ownership problems
- Make sure java 8 is used at build time for scl packages
- Fix man and info path vars

* Tue Jul 08 2014 Mat Booth <mat.booth@redhat.com> - 1.0-5
- Add BR on javapackages-tools so that java.conf gets populated correctly.

* Fri May 02 2014 Mat Booth <mat.booth@redhat.com> - 1.0-4
- Add ivy configuration to runtime package.

* Wed Apr 30 2014 Mat Booth <mat.booth@redhat.com> - 1.0-3
- Fix auto-requires on %%{scl_runtime}

* Tue Apr 29 2014 Mat Booth <mat.booth@redhat.com> - 1.0-2
- Add java and maven configuration to the runtime package.

* Mon Apr 14 2014 Mat Booth <mat.booth@redhat.com> - 1.0-1
- Initial release of the eclipse-luna software collection metapackage.
