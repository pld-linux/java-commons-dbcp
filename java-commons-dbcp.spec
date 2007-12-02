# NOTE
# - need jdk 1.5 due java.sql.Wrapper abstract issue
%include	/usr/lib/rpm/macros.java
Summary:	Jakarta Commons DBCP - database connection pooling
Summary(pl.UTF-8):	Jakarta Commons DBCP - zarządzanie połączeniem z bazą danych
Name:		jakarta-commons-dbcp
Version:	1.2.1
Release:	1.3
License:	Apache
Group:		Development/Languages/Java
Source0:	http://www.apache.org/dist/jakarta/commons/dbcp/source/commons-dbcp-%{version}-src.tar.gz
# Source0-md5:	b7336a1d34ea0e8e9c39b67af510c46d
Source1:	%{name}-tomcat5-build.xml
URL:		http://jakarta.apache.org/commons/dbcp/
BuildRequires:	ant
BuildRequires:	jakarta-commons-collections
BuildRequires:	jakarta-commons-collections-tomcat5
BuildRequires:	jakarta-commons-pool >= 1.2
BuildRequires:	jakarta-commons-pool-tomcat5
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

%package tomcat5
Summary:	DBCP dependency for Tomcat5
Group:		Development/Languages/Java
Obsoletes:	jakarta-commons-dbcp-source

%description tomcat5
DBCP dependency for Tomcat5

%prep
%setup -q -n commons-dbcp-%{version}
cp %{SOURCE1} tomcat5-build.xml

%build
required_jars="commons-pool commons-collections"
export CLASSPATH=$(build-classpath $required_jars)
%ant dist

required_jars="jdbc-stdext xercesImpl commons-collections-tomcat5 commons-pool-tomcat5"
export CLASSPATH=$(build-classpath $required_jars)
%ant -f tomcat5-build.xml

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_javadir}
for a in dist/*.jar; do
	jar=${a##*/}
	cp -a dist/$jar $RPM_BUILD_ROOT%{_javadir}/${jar%%.jar}-%{version}.jar
	ln -s ${jar%%.jar}-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/$jar
done

install pool-tomcat5/commons-dbcp-tomcat5.jar $RPM_BUILD_ROOT%{_javadir}/%{name}-tomcat5-%{version}.jar
ln -sf %{name}-tomcat5-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}-tomcat5.jar

# javadoc
install -d $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
cp -a dist/docs/api/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
ln -s %{name}-%{version} $RPM_BUILD_ROOT%{_javadocdir}/%{name} # ghost symlink

%clean
rm -rf $RPM_BUILD_ROOT

%post javadoc
ln -nfs %{name}-%{version} %{_javadocdir}/%{name}

%files
%defattr(644,root,root,755)
%doc *.txt
%{_javadir}/commons-dbcp.jar
%{_javadir}/commons-dbcp-%{version}.jar

%files tomcat5
%defattr(644,root,root,755)
%{_javadir}/%{name}-tomcat5.jar
%{_javadir}/%{name}-tomcat5-%{version}.jar

%files javadoc
%defattr(644,root,root,755)
%{_javadocdir}/%{name}-%{version}
%ghost %{_javadocdir}/%{name}
