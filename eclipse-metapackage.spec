%global scl eclipse-mars
%global scl_vendor mbooth
%scl_package %scl

Name:      %{scl_name}
Version:   1.0
Release:   3%{?dist}
Summary:   The Eclipse Mars Software Collection
License:   EPL
URL:       http://copr.fedoraproject.org/coprs/%{scl_vendor}/%{scl}/

Source0:   http://www.eclipse.org/legal/epl-v10.html

# Standard SCL build requirements
BuildRequires: scl-utils
BuildRequires: scl-utils-build

# This is needed for java directory macros
BuildRequires: javapackages-tools

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
Summary:   Build configuration the %{scl} Software Collection
Requires:  scl-utils-build
Requires:  %{scl_name}-runtime

%description build
Essential build configuration macros for building the %{scl}
Software Collection.

%prep
%setup -c -T
cp -p %{SOURCE0} .

%build
# Enable collection script
cat <<EOF >enable
# General variables
export PATH=%{_bindir}:%{_sbindir}\${PATH:+:\${PATH}}
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
    <metadataRepositories>
      <repository>%{_scl_root}/usr/share/maven-metadata</repository>
    </metadataRepositories>
    <prefixes>
      <prefix>%{_scl_root}</prefix>
    </prefixes>
  </resolverSettings>
  <installerSettings>
    <metadataDir>opt/%{scl_vendor}/%{scl}/root/usr/share/maven-metadata</metadataDir>
  </installerSettings>
  <repositories>
    <repository>
      <id>%{scl}-resolve</id>
      <type>compound</type>
      <properties>
        <prefix>opt/%{scl_vendor}/%{scl}/root</prefix>
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
        <prefix>opt/%{scl_vendor}/%{scl}/root</prefix>
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
        <prefix>opt/%{scl_vendor}/%{scl}/root</prefix>
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
        <prefix>opt/%{scl_vendor}/%{scl}/root</prefix>
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
install -d -m 755 %{buildroot}%{_datadir}/maven-metadata
install -d -m 755 %{buildroot}%{_datadir}/maven-poms

%files
# The base package is empty because it is a meta-package whose sole purpose
# is to install the whole software collection

%files runtime -f filesystem
%doc epl-v10.html
%{scl_files}
%{_sysconfdir}
%dir %{_javadir}
%dir %{_javadocdir}
%dir %{_datadir}/appdata
%dir %{_datadir}/maven-effective-poms
%dir %{_datadir}/maven-fragments
%dir %{_datadir}/maven-metadata
%dir %{_datadir}/maven-poms

%files build
%{_root_sysconfdir}/rpm/macros.%{scl}-config

%changelog
* Mon Dec 08 2014 Mat Booth <mat.booth@redhat.com> - 1.0-3
- Make archful so that we own lib64 dirs
- Add sbin to SCL's PATH

* Fri Nov 14 2014 Mat Booth <mat.booth@redhat.com> - 1.0-2
- SCL's _sysconfdir is now under /etc instead of /opt
- Fix maven artifact resolution

* Thu Nov 13 2014 Mat Booth <mat.booth@redhat.com> - 1.0-1
- Initial release of the eclipse-mars software collection metapackage.

