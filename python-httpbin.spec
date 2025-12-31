#
# Conditional build:
%bcond_with	tests	# unit tests (2 failures)
%bcond_without	python2 # CPython 2.x module
%bcond_with	python3 # CPython 3.x module (built from python3-httpbin.spec)
%bcond_with	sentry	# Sentry support via raven

Summary:	HTTP Request and Response Service
Summary(pl.UTF-8):	Usługa żądań i odpowiedzi HTTP
Name:		python-httpbin
# keep 0.7.x here for python2 support
Version:	0.7.0
Release:	1
License:	ISC
Group:		Libraries/Python
#Source0Download: https://pypi.python.org/simple/httpbin
Source0:	https://files.pythonhosted.org/packages/source/h/httpbin/httpbin-%{version}.tar.gz
# Source0-md5:	1629975ff6eeb1e5a72ce3deda88ef4e
Patch0:		httpbin-brotli.patch
Patch1:		httpbin-disable-sentry.patch
URL:		https://github.com/Runscope/httpbin
%if %(locale -a | grep -q '^C\.UTF-8$'; echo $?)
BuildRequires:	glibc-localedb-all
%endif
%if %{with python2}
BuildRequires:	python-modules >= 1:2.7
BuildRequires:	python-setuptools
%if %{with tests}
BuildRequires:	python-brotlicffi
BuildRequires:	python-decorator
BuildRequires:	python-flask
BuildRequires:	python-itsdangerous
BuildRequires:	python-markupsafe
%{?with_sentry:BuildRequires:	python-raven}
BuildRequires:	python-six
BuildRequires:	python-werkzeug >= 0.14.1
%endif
%endif
%if %{with python3}
BuildRequires:	python3-modules >= 1:3.4
BuildRequires:	python3-setuptools
%if %{with tests}
BuildRequires:	python3-brotlicffi
BuildRequires:	python3-decorator
BuildRequires:	python3-flask
BuildRequires:	python3-itsdangerous
BuildRequires:	python3-markupsafe
%{?with_sentry:BuildRequires:	python3-raven}
BuildRequires:	python3-six
BuildRequires:	python3-werkzeug >= 0.14.1
%endif
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
Requires:	python-modules >= 1:2.7
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
HTTP Request and Response Service.

%description -l pl.UTF-8
Usługa żądań i odpowiedzi HTTP.

%package -n python3-httpbin
Summary:	HTTP Request and Response Service
Summary(pl.UTF-8):	Usługa żądań i odpowiedzi HTTP
Group:		Libraries/Python
Requires:	python3-modules >= 1:3.4

%description -n python3-httpbin
HTTP Request and Response Service.

%description -n python3-httpbin -l pl.UTF-8
Usługa żądań i odpowiedzi HTTP.

%prep
%setup -q -n httpbin-%{version}
%patch -P0 -p1
%if %{without sentry}
%patch -P1 -p1
%endif

%build
%if %{with python2}
%py_build

%if %{with tests}
%{__python} test_httpbin.py
%endif
%endif

%if %{with python3}
LC_ALL=C.UTF-8 \
%py3_build

%if %{with tests}
%{__python3} test_httpbin.py
%endif
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%py_install

%py_postclean
%endif

%if %{with python3}
LC_ALL=C.UTF-8 \
%py3_install
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc AUTHORS LICENSE README.md
%{py_sitescriptdir}/httpbin
%{py_sitescriptdir}/httpbin-%{version}-py*.egg-info
%endif

%if %{with python3}
%files -n python3-httpbin
%defattr(644,root,root,755)
%doc AUTHORS LICENSE README.md
%{py3_sitescriptdir}/httpbin
%{py3_sitescriptdir}/httpbin-%{version}-py*.egg-info
%endif
