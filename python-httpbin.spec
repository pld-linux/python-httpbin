#
# Conditional build:
%bcond_without	python2 # CPython 2.x module
%bcond_without	python3 # CPython 3.x module

%define 	module	template
Summary:	HTTP Request and Response Service
Summary(pl.UTF-8):	Usługa żądań i odpowiedzi HTTP
Name:		python-httpbin
Version:	0.5.0
Release:	2
License:	ISC
Group:		Libraries/Python
#Source0Download: https://pypi.python.org/simple/httpbin
Source0:	https://files.pythonhosted.org/packages/source/h/httpbin/httpbin-%{version}.tar.gz
# Source0-md5:	923793df99156caa484975ade96ee115
URL:		https://github.com/Runscope/httpbin
%if %(locale -a | grep -q '^C\.UTF-8$'; echo $?)
BuildRequires:	glibc-localedb-all
%endif
%if %{with python2}
BuildRequires:	python-modules >= 1:2.7
BuildRequires:	python-setuptools
%endif
%if %{with python3}
BuildRequires:	python3-modules >= 1:3.4
BuildRequires:	python3-setuptools
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

%build
%if %{with python2}
%py_build
%endif

%if %{with python3}
LC_ALL=C.UTF-8 %py3_build
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%py_install

%py_postclean
%endif

%if %{with python3}
LC_ALL=C.UTF-8 %py3_install
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc AUTHORS LICENSE README.rst
%{py_sitescriptdir}/httpbin
%{py_sitescriptdir}/httpbin-%{version}-py*.egg-info
%endif

%if %{with python3}
%files -n python3-httpbin
%defattr(644,root,root,755)
%doc AUTHORS LICENSE README.rst
%{py3_sitescriptdir}/httpbin
%{py3_sitescriptdir}/httpbin-%{version}-py*.egg-info
%endif
