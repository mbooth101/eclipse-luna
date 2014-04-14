Name:           eclipse-luna
Version:        1.0
Release:        1%{?dist}
Summary:        %scl Software Collection Metapackage

License:        EPL
URL:            
Source0:        

BuildRequires:  
Requires:       

%description


%prep
%setup -q


%build
%configure
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
%make_install


%files
%doc



%changelog
* Mon Apr 14 2014 Mat Booth <fedora@matbooth.co.uk>
- 
