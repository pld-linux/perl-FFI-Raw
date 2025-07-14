#
# Conditional build:
%bcond_without	tests	# do not perform "make test"

%define		pdir	FFI
%define		pnam	Raw
Summary:	FFI::Raw - Perl bindings to the portable FFI library (libffi)
Name:		perl-FFI-Raw
Version:	0.32
Release:	1
# same as perl
License:	GPL v1+ or Artistic
Group:		Development/Languages/Perl
Source0:	http://www.cpan.org/modules/by-module/FFI/%{pdir}-%{pnam}-%{version}.tar.gz
# Source0-md5:	a2fa68728f71f17fc869f7d56592de87
Patch0:		%{name}-makefile.patch
Patch1:		%{name}-manifest.patch
URL:		http://search.cpan.org/dist/FFI-Raw/
BuildRequires:	libffi
BuildRequires:	perl-devel >= 1:5.8.0
BuildRequires:	rpm-perlprov >= 4.1-13
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
FFI::Raw provides a low-level foreign function interface (FFI) for
Perl based on libffi. In essence, it can access and call functions
exported by shared libraries without the need to write C/XS code.

Dynamic symbols can be automatically resolved at runtime so that the
only information needed to use FFI::Raw is the name (or path) of the
target library, the name of the function to call and its signature
(though it is also possible to pass a function pointer obtained, for
example, using DynaLoader).

%prep
%setup -q -n %{pdir}-%{pnam}-%{version}
%patch -P0 -p1
%patch -P1 -p1

%{__rm} -r deps/libffi

%build
%{__perl} Makefile.PL \
	INSTALLDIRS=vendor
%{__make} \
	CC="%{__cc}" \
	OPTIMIZE="%{rpmcflags}"

%{?with_tests:%{__make} test}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc Change* README
%{perl_vendorarch}/FFI/Raw.pm
%{perl_vendorarch}/FFI/Raw
%dir %{perl_vendorarch}/auto/FFI/Raw
%attr(755,root,root) %{perl_vendorarch}/auto/FFI/Raw/Raw.so
%{_mandir}/man3/*
