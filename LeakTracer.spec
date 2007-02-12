Summary:	A tool for trace and analyze memory leaks in C++ programs
Summary(pl.UTF-8):   Narzędzie do śledzenia i analizowania wycieków pamięci w programach w C++
Name:		LeakTracer
Version:	2.4
Release:	1
License:	Public Domain
Group:		Applications
Source0:	http://www.andreasen.org/LeakTracer/LeakTracer.tar.gz
# Source0-md5:	e1cf9d03c12a45d39f253e558d231438
Patch0:		%{name}-Makefile.patch
Patch1:		%{name}-64bit.patch
Patch2:		%{name}-caller_addr.patch
URL:		http://www.andreasen.org/LeakTracer/
BuildRequires:	gcc-c++
BuildRequires:	sed >= 4.0
Requires:	gdb
ExcludeArch:	alpha arm mips
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
LeakTracer is a small tool for checking a C++ program for memory
leaks. To use LeakTracer, run your program using the provided
LeakCheck script. It uses the LD_PRELOAD feature to "overlay" some
functions on top of your functions (no recompile needed). leak-analyze
uses gdb to print out the exact line where the memory was allocated
and not freed - this of course means you have to free all dynamically
allocated data. LeakTracer also overrides the global operator new and
operator delete - this will give problems if you override them as
well. LeakTracer traces only new/new[] and delete calls - it does not
look at malloc/free/realloc.

%description -l pl.UTF-8
LeakTracer to małe narzędzie do sprawdzania programów w C++ pod kątem
wycieków pamięci. Aby go użyć na jakimś programie, trzeba uruchomić
ten program przy użyciu załączonego skryptu LeakCheck. Używa on
LD_PRELOAD do przykrycia niektórych funkcji (rekompilacja nie jest
potrzebna). leak-analyze używa gdb do pokazania w których dokładnie
liniach pamięć została przydzielona i nie zwolniona - co oznacza, że
trzeba zwolnić wszystkie dynamicznie przydzielone dane. LeakTracer
przykrywa także globalne operatory new i delete - może to spowodować
problemy, jeśli my także chcemy je przykryć. LeakTracer śledzi tylko
wywołania new/new[] i delete - nie patrzy na malloc/free/realloc.

%prep
%setup -q -n %{name}
%patch0 -p1
%patch1 -p0
%patch2 -p0

%build
sed -i "s:SHLIB=.*:SHLIB=%{_libdir}/LeakTracer.so:" LeakCheck

%{__make} \
	CXX="%{__cxx}" \
	CXXFLAGS="%{rpmcxxflags} -nodefaultlibs -O1 -fno-omit-frame-pointer"

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
