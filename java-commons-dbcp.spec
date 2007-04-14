%include	/usr/lib/rpm/macros.java
Summary:	Jakarta Commons DBCP - database connection pooling
Summary(pl.UTF-8):	Jakarta Commons DBCP - zarządzanie połączeniem z bazą danych
Name:		jakarta-commons-dbcp
Version:	1.2.1
Release:	1.2
License:	Apache
Group:		Development/Languages/Java
Source0:	http://www.apache.org/dist/jakarta/commons/dbcp/source/commons-dbcp-%{version}-src.tar.gz
# Source0-md5:	b7336a1d34ea0e8e9c39b67af510c46d
URL:		http://jakarta.apache.org/commons/dbcp/
BuildRequires:	ant
BuildRequires:	jakarta-commons-collections
BuildRequires:	jakarta-commons-pool >= 1.2
BuildRequires:	jdk >= 1.2
BuildRequires:	jpackage-utils
BuildRequires:	rpm-javaprov
BuildRequires:	rpmbuild(macros) >= 1.300
Requires:	jakarta-commons-collections
Requires:	jakarta-commons-pool >= 1.2
Requires:	jre >= 1.2
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

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

%package javadoc
Summary:	Jakarta Commons DBCP
Summary(pl.UTF-8):	Dokumentacja do Jakarta Commons DBCP
Group:		Documentation
Requires:	jpackage-utils
Obsoletes:	jakarta-commons-dbcp-doc

%description javadoc
Jakarta Commons DBCP.

%description javadoc -l pl.UTF-8
Dokumentacja do Jakarta Commons DBCP.

%package source
Summary:	Jakarta Commons DBCP source code
Summary(pl.UTF-8):	Kod źródłowy Jakarta Commons DBCP
Group:		Development/Languages/Java
AutoReq:	no
AutoProv:	no

%description source
Jakarta Commons DBCP source code.

%description source -l pl.UTF-8
Kod źródłowy Jakarta Commons DBCP.

%prep
%setup -q -n commons-dbcp-%{version}

%build
required_jars="commons-pool commons-collections"
export CLASSPATH=$(build-classpath $required_jars)
%ant dist

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_javadir}
for a in dist/*.jar; do
	jar=${a##*/}
	cp -a dist/$jar $RPM_BUILD_ROOT%{_javadir}/${jar%%.jar}-%{version}.jar
	ln -s ${jar%%.jar}-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/$jar
done

# javadoc
install -d $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
cp -pr dist/docs/api/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}

# source code
install -d $RPM_BUILD_ROOT%{_prefix}/src/%{name}-%{version}
cp -a src $RPM_BUILD_ROOT%{_prefix}/src/%{name}-%{version}

%clean
rm -rf $RPM_BUILD_ROOT

%post javadoc
rm -f %{_javadocdir}/%{name}
ln -s %{name}-%{version} %{_javadocdir}/%{name}

%postun javadoc
if [ "$1" = "0" ]; then
	rm -f %{_javadocdir}/%{name}
fi

%files
%defattr(644,root,root,755)
%doc *.txt
%{_javadir}/*.jar

%files javadoc
%defattr(644,root,root,755)
%{_javadocdir}/%{name}-%{version}

%files source
%defattr(644,root,root,755)
%{_prefix}/src/%{name}-%{version}
