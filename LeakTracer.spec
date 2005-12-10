Summary:	A tool for trace and analyze memory leaks in C++ programs
Name:		LeakTracer
Version:	2.3
Release:	1
License:	Public Domain
Group:		Applications
Source0:	http://www.andreasen.org/LeakTracer/LeakTracer.tar.gz
# Source0-md5:	e1cf9d03c12a45d39f253e558d231438
Patch0:		%{name}-Makefile.patch
URL:		http://www.andreasen.org/LeakTracer/
BuildRequires:	libstdc++-devel
BuildRequires:	sed >= 4.0
Requires:	gdb
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
LeakTracer is a small tool for checking a C++ program for memory
leaks. To use LeakTracer, run your program using the provided
LeakCheck script. It uses the LD_PRELOAD feature to "overlay" some
functions on top of your functions (no recompile needed). leak-anlyze
uses gdb to print out the exact line where the memory was allocated
and not freed - this of course means you have to free all dynamically
allocated data. LeakTracer also overrides the global operator new and
operator delete - this will give problems if you override them as
well. LeakTracer traces only new/new[] and delete calls - it does not
look at malloc/free/realloc.

%prep
%setup -q -n %{name}
%patch0 -p1

%build
sed -i "s:SHLIB=.*:SHLIB=%{_libdir}/LeakTracer.so:" LeakCheck

%{__make} \
	CXX="%{__cxx}" \
	CXXFLAGS="%{rpmcflags}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_libdir}}

install leak-analyze	$RPM_BUILD_ROOT%{_bindir}
install LeakCheck	$RPM_BUILD_ROOT%{_bindir}
install LeakTracer.so	$RPM_BUILD_ROOT%{_libdir}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_libdir}/*.so
