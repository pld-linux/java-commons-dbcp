Summary:	Jakarta Commons DBCP - database connection pooling
Summary(pl.UTF-8):   Jakarta Commons DBCP - zarządzanie połączeniem z bazą danych
Name:		jakarta-commons-dbcp
Version:	1.2.1
Release:	1
License:	Apache
Group:		Development/Languages/Java
Source0:	http://www.apache.org/dist/jakarta/commons/dbcp/source/commons-dbcp-%{version}-src.tar.gz
# Source0-md5:	b7336a1d34ea0e8e9c39b67af510c46d
URL:		http://jakarta.apache.org/commons/dbcp/
BuildRequires:	ant
BuildRequires:	jakarta-commons-pool >= 1.2
BuildRequires:	jdk >= 1.2
Requires:	jakarta-commons-collections
Requires:	jakarta-commons-pool >= 1.2
Requires:	jre >= 1.2
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_javalibdir	%{_datadir}/java

%description
The DBCP package provides database connection pooling services. The
following features are supported:
 - DataSource and Driver interfaces to the pool,
 - Support for arbitrary sources of the underlying Connections,
 - Integration with arbitrary org.apache.commons.pool.ObjectPool
   implementations,
 - Support for Connection validation, expiration, etc.,
 - Support for PreparedStatement pooling,
 - XML configuration.

%description -l pl.UTF-8
Pakiet DBCP dostarcza usługi gospodarujące połączeniami z bazą danych.
Obsługiwane są następujące własności:
 - interfejsy DataSource i Driver,
 - obsługa dowolnych źródeł dla podlegających im połączeń,
 - integracja z dowolnymi implementacjami
   org.apache.commons.pool.ObjectPool,
 - obsługa kontroli poprawności, przedawnienia połączeń itp.,
 - obsługa zarządzania PreparedStatement,
 - konfiguracja w XML-u.

%package doc
Summary:	Jakarta Commons DBCP
Summary(pl.UTF-8):   Dokumentacja do Jakarta Commons DBCP
Group:		Development/Languages/Java

%description doc
Jakarta Commons DBCP.

%description doc -l pl.UTF-8
Dokumentacja do Jakarta Commons DBCP.

%prep
%setup -q -n commons-dbcp-%{version}

%build
cat << EOF > build.properties
commons-pool.jar=%{_javalibdir}/commons-pool.jar
EOF
ant dist

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_javalibdir}

install dist/*.jar $RPM_BUILD_ROOT%{_javalibdir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc *.txt
%{_javalibdir}/*.jar

%files doc
%defattr(644,root,root,755)
%doc dist/docs
