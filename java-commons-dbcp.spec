# TODO
# - use ant conditions (replace JDBC_4_ANT_KEY_BEGIN) instead of the code in prep
#
# Conditional build:
%bcond_without	javadoc		# don't build javadoc

%define		srcname	commons-dbcp
Summary:	Commons DBCP - database connection pooling
Summary(pl.UTF-8):	Commons DBCP - zarządzanie połączeniem z bazą danych
Name:		java-commons-dbcp
Version:	1.4
Release:	1
License:	Apache v2.0
Group:		Libraries/Java
Source0:	http://www.apache.org/dist/commons/dbcp/source/commons-dbcp-%{version}-src.tar.gz
# Source0-md5:	e9f599c99baefeeb0e192030c5d19d5d
Source1:	jakarta-commons-dbcp-tomcat5-build.xml
Patch0:		jakarta-commons-dbcp-bug-191.patch
Patch1:		jakarta-commons-dbcp-javadoc.patch
URL:		http://commons.apache.org/dbcp/
BuildRequires:	ant
BuildRequires:	java(jaxp_parser_impl)
BuildRequires:	java-commons-collections
BuildRequires:	java-commons-collections-tomcat5
BuildRequires:	java-commons-pool >= 1.2
BuildRequires:	java-commons-pool-tomcat5
BuildRequires:	jdk
BuildRequires:	jpackage-utils
BuildRequires:	rpm-javaprov
BuildRequires:	rpmbuild(macros) >= 1.300
Requires:	java-commons-collections
Requires:	java-commons-pool >= 1.2
Requires:	jpackage-utils
Provides:	jakarta-commons-dbcp
Obsoletes:	jakarta-commons-dbcp
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
Summary:	Commons DBCP documentation
Summary(pl.UTF-8):	Dokumentacja do Commons DBCP
Group:		Documentation
Requires:	jpackage-utils
Provides:	jakarta-commons-dbcp-javadoc
Obsoletes:	jakarta-commons-dbcp-doc
Obsoletes:	jakarta-commons-dbcp-javadoc

%description javadoc
Commons DBCP documentation.

%description javadoc -l pl.UTF-8
Dokumentacja do Commons DBCP.

%package tomcat5
Summary:	Commons DBCP dependency for Tomcat5
Summary(pl.UTF-8):	Elementy Commons DBCP dla Tomcata 5
Group:		Development/Languages/Java
Requires:	java(jaxp_parser_impl)
Provides:	jakarta-commons-dbcp-tomcat5
Obsoletes:	jakarta-commons-dbcp-source
Obsoletes:	jakarta-commons-dbcp-tomcat5

%description tomcat5
Commons DBCP dependency for Tomcat5.

%description tomcat5 -l pl.UTF-8
Elementy Commons DBCP dla Tomcata 5.

%prep
%setup -q -n commons-dbcp-%{version}-src
cp %{SOURCE1} tomcat5-build.xml
%{__sed} -i -e 's,\r$,,' build.xml


%if %{with java_sun}
java_version=$(IFS=.; set -- $(java -fullversion 2>&1 | grep -o '".*"' | xargs); echo "$1.$2")
if ! awk -vv=$java_version 'BEGIN{exit(v >= 1.6)}'; then # java is at least 1.6
%patch0 -p0
fi
%endif
%patch1 -p1

%build
required_jars="commons-pool commons-collections libgcj"
export CLASSPATH=$(build-classpath $required_jars)
%ant clean
%ant build-jar %{?with_javadoc:javadoc}

required_jars="jdbc-stdext xercesImpl commons-collections-tomcat5 commons-pool-tomcat5 libgcj"
export CLASSPATH=$(build-classpath $required_jars)
%ant -f tomcat5-build.xml

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_javadir}
# jars
install dist/%{srcname}.jar $RPM_BUILD_ROOT%{_javadir}/%{srcname}-%{version}.jar
ln -sf %{srcname}-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{srcname}.jar

install dbcp-tomcat5/%{srcname}-tomcat5.jar $RPM_BUILD_ROOT%{_javadir}/%{srcname}-tomcat5-%{version}.jar
ln -sf %{srcname}-tomcat5-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{srcname}-tomcat5.jar

# javadoc
%if %{with javadoc}
install -d $RPM_BUILD_ROOT%{_javadocdir}/%{srcname}-%{version}
cp -a dist/docs/api/* $RPM_BUILD_ROOT%{_javadocdir}/%{srcname}-%{version}
ln -s %{srcname}-%{version} $RPM_BUILD_ROOT%{_javadocdir}/%{srcname} # ghost symlink
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post javadoc
ln -nfs %{name}-%{version} %{_javadocdir}/%{name}

%files
%defattr(644,root,root,755)
%doc RELEASE-NOTES.txt
%{_javadir}/commons-dbcp.jar
%{_javadir}/commons-dbcp-%{version}.jar

%files tomcat5
%defattr(644,root,root,755)
%{_javadir}/commons-dbcp-tomcat5.jar
%{_javadir}/commons-dbcp-tomcat5-%{version}.jar

%if %{with javadoc}
%files javadoc
%defattr(644,root,root,755)
%{_javadocdir}/%{srcname}-%{version}
%ghost %{_javadocdir}/%{srcname}
%endif
