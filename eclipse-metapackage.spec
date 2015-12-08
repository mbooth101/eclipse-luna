%global scl eclipse-neon
%global scl_vendor mbooth
%scl_package %scl

Name:      %{scl_name}
Version:   1.0
Release:   1%{?dist}
Summary:   The Eclipse Neon Software Collection
License:   EPL
URL:       http://copr.fedoraproject.org/coprs/%{scl_vendor}/%{scl}/

Source0:   http://www.eclipse.org/legal/epl-v10.html

# Standard SCL build requirements
BuildRequires: scl-utils >= 2.0.1-7
BuildRequires: scl-utils-build >= 2.0.1-7

# List everything in the SCL here so that installation of only the metapackage brings in
# everything we need
Requires: %{scl_name}-runtime

%description
Meta-package that will install everything needed to use the %{scl}
Software Collection.

%package   runtime
Summary:   Runtime scripts for the %{scl} Software Collection
Requires:  scl-utils

%description runtime
Essential runtime scripts for working with the %{scl} Software
Collection.

%package   build
Summary:   Build configuration for the %{scl} Software Collection
Requires:  scl-utils-build
Requires:  %{scl_name}-runtime

%description build
Essential build configuration macros for building the %{scl}
Software Collection.

%prep
%setup -c -T
cp -p %{SOURCE0} .

%build
# Java configuration
cat <<EOF >java.conf
JAVA_LIBDIR=%{_datadir}/java
JNI_LIBDIR=%{_prefix}/lib/java
JVM_ROOT=%{_prefix}/lib/jvm
EOF

# XMvn configuration
cat <<EOF >configuration.xml
<configuration xmlns="http://fedorahosted.org/xmvn/CONFIG/2.0.0">
  <resolverSettings>
    <prefixes>
      <prefix>%{_scl_root}</prefix>
      <prefix>/</prefix>
    </prefixes>
    <metadataRepositories>
      <repository>%{_scl_root}/usr/share/maven-metadata</repository>
    </metadataRepositories>
  </resolverSettings>
  <installerSettings>
    <metadataDir>opt/%{scl_vendor}/%{scl}/root/usr/share/maven-metadata</metadataDir>
  </installerSettings>
  <repositories>
    <repository>
      <id>resolve-%{scl}</id>
      <type>compound</type>
      <properties>
        <prefix>%{_scl_root}</prefix>
        <namespace>%{scl}</namespace>
      </properties>
      <configuration>
        <repositories>
          <repository>base-resolve</repository>
        </repositories>
      </configuration>
    </repository>
    <repository>
      <id>resolve</id>
      <type>compound</type>
      <properties>
        <prefix>/</prefix>
      </properties>
      <configuration>
        <repositories>
	  <!-- Put resolvers in order you want to use them, from
	       highest to lowest preference. (resolve-local is
	       resolver that resolves from local Maven repository in
	       .xm2 in current directory.) -->
          <repository>resolve-local</repository>
          <repository>resolve-%{scl}</repository>
          <repository>base-resolve</repository>
        </repositories>
      </configuration>
    </repository>
    <repository>
      <id>install</id>
      <type>compound</type>
      <properties>
        <prefix>opt/%{scl_vendor}/%{scl}/root</prefix>
        <namespace>%{scl}</namespace>
      </properties>
      <configuration>
        <repositories>
          <repository>base-install</repository>
        </repositories>
      </configuration>
    </repository>
  </repositories>
</configuration>
EOF

%install
%{scl_install}

# Add missing vendor info to build macros
cat <<EOF >>%{buildroot}%{_root_sysconfdir}/rpm/macros.%{scl}-config
%%scl_vendor %scl_vendor
EOF

# Install enable script
%{scl_enable_script}

# Install environment module
cat <<EOF >%{buildroot}%{_scl_scripts}/%{scl}
#%Module1.0
# General path variables
prepend-path PATH %{_bindir}:%{_sbindir}
prepend-path MANPATH %{_mandir}

# Required by Java Packages Tools to locate java.conf
prepend-path JAVACONFDIRS %{_sysconfdir}/java:/etc/java

# Required by XMvn to locate its configuration files
prepend-path XDG_CONFIG_DIRS %{_sysconfdir}/xdg:/etc/xdg

# Required to locate shared libs inside the collection
prepend-path LD_LIBRARY_PATH %{_prefix}/lib:%{_prefix}/lib64
EOF

install -d -m 755 %{buildroot}%{_sysconfdir}/java
install -p -m 644 java.conf %{buildroot}%{_sysconfdir}/java/

install -d -m 755 %{buildroot}%{_sysconfdir}/xdg/xmvn
install -p -m 644 configuration.xml %{buildroot}%{_sysconfdir}/xdg/xmvn/

# Misc other directories we should also own
install -d -m 755 %{buildroot}%{_prefix}/lib/java
install -d -m 755 %{buildroot}%{_datadir}/java
install -d -m 755 %{buildroot}%{_datadir}/javadoc
install -d -m 755 %{buildroot}%{_datadir}/appdata
install -d -m 755 %{buildroot}%{_datadir}/maven-metadata
install -d -m 755 %{buildroot}%{_datadir}/maven-poms

%files
# The base package is empty because it is a meta-package whose sole purpose
# is to install the whole software collection

%files runtime -f filesystem
%doc epl-v10.html
%{scl_files}
%{_sysconfdir}/java

# Misc other directories we should also own
%dir %{_prefix}/lib/java
%dir %{_datadir}/java
%dir %{_datadir}/javadoc
%dir %{_datadir}/appdata
%dir %{_datadir}/maven-metadata
%dir %{_datadir}/maven-poms

%files build
%{_root_sysconfdir}/rpm/macros.%{scl}-config

%changelog
* Mon Dec 07 2015 Mat Booth <mat.booth@redhat.com> - 1.0-1
- Initial release of the eclipse-neon software collection metapackage.

