%global scl eclipse-luna
%scl_package %scl

Name:      %{scl_name}
Version:   1.0
Release:   1%{?dist}
Summary:   The %{scl} Software Collection
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
Summary:   Repository configuration the %{scl} Software Collection
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

%description build
Essential build configuration macros for building the %{scl}
Software Collection.

%prep
%setup -c -T

cp -p %{SOURCE0} .

%build

%install
install -d -m 755 %{buildroot}%{_root_sysconfdir}/yum.repos.d
cat >> %{buildroot}%{_root_sysconfdir}/yum.repos.d/%{scl}.repo << EOF
[mbooth-%{scl}]
name=The %{scl} Software Collection for Fedora \$releasever
baseurl=http://copr-be.cloud.fedoraproject.org/results/mbooth/%{scl}/fedora-\$releasever-\$basearch/
skip_if_unavailable=True
gpgcheck=0
enabled=1
EOF

install -d -m 755 %{buildroot}%{_scl_scripts}/root
cat >> %{buildroot}%{_scl_scripts}/enable << EOF
export PATH=%{_bindir}\${PATH:+:\${PATH}}
EOF
%scl_install

%files
%doc epl-v10.html

%files release
%config(noreplace) %{_root_sysconfdir}/yum.repos.d/%{scl}.repo

%files runtime
%scl_files

%files build
%{_root_sysconfdir}/rpm/macros.%{scl}-config

%changelog
* Mon Apr 14 2014 Mat Booth <mat.booth@redhat.com> - 1.0-1
- Initial release of the eclipse-luna software collection metapackage.
