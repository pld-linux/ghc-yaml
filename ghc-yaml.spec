#
# Conditional build:
%bcond_without	prof		# profiling library
#
%define		pkgname	yaml
Summary:	Support for parsing and rendering YAML documents
Summary(pl.UTF-8):	Analiza i renderowanie dokumentów YAML
Name:		ghc-%{pkgname}
Version:	0.11.4.0
Release:	2
License:	BSD
Group:		Development/Languages
#Source0Download: http://hackage.haskell.org/package/yaml
Source0:	http://hackage.haskell.org/package/%{pkgname}-%{version}/%{pkgname}-%{version}.tar.gz
# Source0-md5:	18322a12aa993871315c33dbe7529026
URL:		http://hackage.haskell.org/package/yaml
BuildRequires:	ghc >= 6.12.3
BuildRequires:	ghc-aeson >= 0.11
BuildRequires:	ghc-attoparsec >= 0.11.3.0
BuildRequires:	ghc-base >= 4.9.1
BuildRequires:	ghc-bytestring >= 0.9.1.4
BuildRequires:	ghc-conduit >= 1.2.8
BuildRequires:	ghc-containers
BuildRequires:	ghc-directory
BuildRequires:	ghc-filepath
BuildRequires:	ghc-libyaml >= 0.1
BuildRequires:	ghc-mtl
BuildRequires:	ghc-resourcet >= 0.3
BuildRequires:	ghc-scientific >= 0.3
BuildRequires:	ghc-template-haskell
BuildRequires:	ghc-text
BuildRequires:	ghc-transformers >= 0.1
BuildRequires:	ghc-unordered-containers
BuildRequires:	ghc-vector
%if %{with prof}
BuildRequires:	ghc-prof >= 6.12.3
BuildRequires:	ghc-aeson-prof >= 0.11
BuildRequires:	ghc-attoparsec-prof >= 0.11.3.0
BuildRequires:	ghc-base-prof >= 4.9.1
BuildRequires:	ghc-bytestring-prof >= 0.9.1.4
BuildRequires:	ghc-conduit-prof >= 1.2.8
BuildRequires:	ghc-containers-prof
BuildRequires:	ghc-directory-prof
BuildRequires:	ghc-filepath-prof
BuildRequires:	ghc-libyaml-prof >= 0.1
BuildRequires:	ghc-mtl-prof
BuildRequires:	ghc-resourcet-prof >= 0.3
BuildRequires:	ghc-scientific-prof >= 0.3
BuildRequires:	ghc-template-haskell-prof
BuildRequires:	ghc-text-prof
BuildRequires:	ghc-transformers-prof >= 0.1
BuildRequires:	ghc-unordered-containers-prof
BuildRequires:	ghc-vector-prof
%endif
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 1.608
Requires(post,postun):	/usr/bin/ghc-pkg
%requires_eq	ghc
Requires:	ghc-aeson >= 0.11
Requires:	ghc-attoparsec >= 0.11.3.0
Requires:	ghc-base >= 4.9.1
Requires:	ghc-bytestring >= 0.9.1.4
Requires:	ghc-conduit >= 1.2.8
Requires:	ghc-containers
Requires:	ghc-directory
Requires:	ghc-filepath
Requires:	ghc-libyaml >= 0.1
Requires:	ghc-mtl
Requires:	ghc-resourcet >= 0.3
Requires:	ghc-scientific >= 0.3
Requires:	ghc-template-haskell
Requires:	ghc-text
Requires:	ghc-transformers >= 0.1
Requires:	ghc-unordered-containers
Requires:	ghc-vector
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# debuginfo is not useful for ghc
%define		_enable_debug_packages	0

# don't compress haddock files
%define		_noautocompressdoc	*.haddock

%description
This package provides support for parsing and emitting YAML documents.

%description -l pl.UTF-8
Ten pakiet zapewnia obsługę analizy i tworzenia dokumentów YAML.

%package prof
Summary:	Profiling %{pkgname} library for GHC
Summary(pl.UTF-8):	Biblioteka profilująca %{pkgname} dla GHC
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	ghc-prof >= 6.12.3
Requires:	ghc-aeson-prof >= 0.11
Requires:	ghc-attoparsec-prof >= 0.11.3.0
Requires:	ghc-base-prof >= 4.9.1
Requires:	ghc-bytestring-prof >= 0.9.1.4
Requires:	ghc-conduit-prof >= 1.2.8
Requires:	ghc-containers-prof
Requires:	ghc-directory-prof
Requires:	ghc-filepath-prof
Requires:	ghc-libyaml-prof >= 0.1
Requires:	ghc-mtl-prof
Requires:	ghc-resourcet-prof >= 0.3
Requires:	ghc-scientific-prof >= 0.3
Requires:	ghc-template-haskell-prof
Requires:	ghc-text-prof
Requires:	ghc-transformers-prof >= 0.1
Requires:	ghc-unordered-containers-prof
Requires:	ghc-vector-prof

%description prof
Profiling %{pkgname} library for GHC. Should be installed when
GHC's profiling subsystem is needed.

%description prof -l pl.UTF-8
Biblioteka profilująca %{pkgname} dla GHC. Powinna być zainstalowana
kiedy potrzebujemy systemu profilującego z GHC.

%package doc
Summary:	HTML documentation for ghc %{pkgname} package
Summary(pl.UTF-8):	Dokumentacja w formacie HTML dla pakietu ghc %{pkgname}
Group:		Documentation

%description doc
HTML documentation for ghc %{pkgname} package.

%description doc -l pl.UTF-8
Dokumentacja w formacie HTML dla pakietu ghc %{pkgname}.

%prep
%setup -q -n %{pkgname}-%{version}

%build
runhaskell Setup.lhs configure -v2 \
	%{?with_prof:--enable-library-profiling} \
	--flags="-no-exe" \
	--prefix=%{_prefix} \
	--libdir=%{_libdir} \
	--libexecdir=%{_libexecdir} \
	--docdir=%{_docdir}/%{name}-%{version}

runhaskell Setup.lhs build
runhaskell Setup.lhs haddock
# --executables fails here

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_libdir}/%{ghcdir}/package.conf.d

runhaskell Setup.lhs copy --destdir=$RPM_BUILD_ROOT

# work around automatic haddock docs installation
%{__rm} -rf %{name}-%{version}-doc
cp -a $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version} %{name}-%{version}-doc
%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}

runhaskell Setup.lhs register \
	--gen-pkg-config=$RPM_BUILD_ROOT%{_libdir}/%{ghcdir}/package.conf.d/%{pkgname}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
%ghc_pkg_recache

%postun
%ghc_pkg_recache

%files
%defattr(644,root,root,755)
%doc LICENSE
%attr(755,root,root) %{_bindir}/yaml2json
%attr(755,root,root) %{_bindir}/json2yaml
%{_libdir}/%{ghcdir}/package.conf.d/%{pkgname}.conf
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/libHSyaml-%{version}-*.so
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/libHSyaml-%{version}-*.a
%exclude %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/libHSyaml-%{version}-*_p.a
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/*.dyn_hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/*.dyn_hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Yaml
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Yaml/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Yaml/*.dyn_hi

%if %{with prof}
%files prof
%defattr(644,root,root,755)
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/libHSyaml-%{version}-*_p.a
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Yaml/*.p_hi
%endif

%files doc
%defattr(644,root,root,755)
%doc %{name}-%{version}-doc/*
