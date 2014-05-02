%global scl eclipse-luna
%scl_package %scl

%global __requires_exclude ^%{scl_runtime}$

Name:      %{scl_name}
Version:   1.0
Release:   4%{?dist}
Summary:   The Eclipse Luna Software Collection
License:   EPL
URL:       http://copr.fedoraproject.org/coprs/mbooth/%{scl}/
BuildArch: noarch

Source0:   http://www.eclipse.org/legal/epl-v10.html

# List everything in the SCL here
Requires: %{scl_name}-release
Requires: %{scl_name}-runtime

BuildRequires: scl-utils-build

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
Requires:  %{scl_runtime}

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

# Needed by Java Packages Tools to locate java.conf
export JAVACONFDIRS="%{_sysconfdir}/java:\${JAVACONFDIRS:-/etc/java}"

# Required by XMvn to locate its configuration files
export XDG_CONFIG_DIRS="%{_sysconfdir}/xdg:\${XDG_CONFIG_DIRS:-/etc/xdg}"
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

%files
# The base package is empty because it is a meta-package whose sole purpose
# is to install the whole software collection

%files release
%config(noreplace) %{_root_sysconfdir}/yum.repos.d/%{scl}.repo

%files runtime
%doc epl-v10.html
%{_sysconfdir}/java
%{_sysconfdir}/ivy
%{_sysconfdir}/xdg/xmvn/configuration.xml
%{scl_files}

%files build
%doc epl-v10.html
%{_root_sysconfdir}/rpm/macros.%{scl}-config

%changelog
* Fri May 02 2014 Mat Booth <fedora@matbooth.co.uk> - 1.0-4
- Add ivy configuration to runtime package.

* Wed Apr 30 2014 Mat Booth <fedora@matbooth.co.uk> - 1.0-3
- Fix auto-requires on %%{scl_runtime}

* Tue Apr 29 2014 Mat Booth <mat.booth@redhat.com> - 1.0-2
- Add java and maven configuration to the runtime package.

* Mon Apr 14 2014 Mat Booth <mat.booth@redhat.com> - 1.0-1
- Initial release of the eclipse-luna software collection metapackage.
