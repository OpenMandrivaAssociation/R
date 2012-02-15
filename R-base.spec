%define libname %mklibname Rmath
# (tpg) really not needed
# for private copy in /usr/lib/R/share/perl/Text/DelimMatch.pm 
%define _provides_exceptions KernSmooth.so\\|MASS.so\\|R_X11.so\\|class.so\\|cluster.so\\|foreign.so\\|grDevices.so\\|grid.so\\|internet.so\\|lapack.so\\|lattice.so\\|libRblas.so\\|libRlapack.so\\|methods.so\\|mgcv.so\\|nlme.so\\|nnet.so\\|rpart.so\\|spatial.so\\|splines.so\\|stats.so\\|survival.so\\|tcltk.so\\|tools.so\\|vfonts.so\\|perl\(R::.*\)
%define _requires_exceptions libRblas.so\\|libRlapack.so\\|perl\(R::.*\)

%define _disable_ld_no_undefined 1

%bcond_without		system_pcre

%ifarch %mips %arm
%define use_java	0
%else
%define use_java	1
%endif

Summary:	A language for data analysis and graphics
Name:		R-base
Version:	2.12.2
Release:	2
License:	GPLv2+
Group:		Sciences/Mathematics
URL:		http://www.r-project.org
Source0:	http://cran.r-project.org/src/base/R-2/R-%{version}.tar.gz
Source1:        R-icons-png.tar.bz2
Source2:	R.bash_completion.bz2
Patch0:         R-2.8.1-menu.patch
Patch2:		R-2.8.1-underlinking.patch
Patch3:		R-2.7.2-CVE-2008-3931.patch
Patch5:		R-2.10.1-gfxdemos.patch
Patch6:		R-2.12.2-pcre.patch
BuildRequires:	pth-devel
BuildRequires:	glibc-static-devel
BuildRequires:	gcc-c++
BuildRequires:	cups-common
BuildRequires:	bzip2-devel
BuildRequires:	gcc-gfortran
BuildRequires:	gpm-devel
BuildRequires:	ncurses-devel
BuildRequires:	readline-devel
BuildRequires:	tk-devel
Buildrequires:	tcl
BuildRequires:	tcl-devel
BuildRequires:	texinfo
BuildRequires:	texlive
BuildRequires:  libx11-devel
BuildRequires:	libxmu-devel
BuildRequires:	libxt-devel
BuildRequires:	png-devel
BuildRequires:	jpeg-devel
%if %{with system_pcre}
BuildRequires:	pcre-devel
%endif
BuildRequires:	bison
BuildRequires:	xdg-utils
%if %{use_java}
BuildRequires:	java-rpmbuild
%endif
BuildRequires:	paper-utils
BuildRequires:	cairo-devel
BuildRequires:	pango-devel
BuildRequires:	libtiff-devel
BuildRequires:	zip
BuildRequires:	lapack-devel
BuildRequires:	blas-devel
BuildRequires:	gcc-objc
BuildRequires:	gcc-objc++
BuildRequires:	imake
BuildRequires:	gettext-devel
BuildRequires:	glibc-static-devel
BuildRequires:	pth-devel
#BuildRequires:	gnustep-make
#BuildRequires:	libgnustep-base-devel
#BuildRequires:	gnustep-base
BuildRequires:	lzma-devel
BuildRequires:	icu-devel
BuildRequires:	paper-utils
Requires:	tcl
Requires:	tk
Requires:	perl
Requires:	sed
Requires:	x11-font-adobe-100dpi
Provides:	R
Obsoletes:	R-recommended <= 1.5.1
Provides:	R-recommended

%description
`GNU S' - A language and environment for statistical computing and
graphics. R is similar to the S system, which was developed at Bell
Laboratories by John Chambers et al. It provides a wide variety of
statistical and graphical techniques (linear and nonlinear modelling,
statistical tests, time series analysis, classification, clustering, ...).

R is designed as a true computer language with control-flow
constructions for iteration and alternation, and it allows users to
add additional functionality by defining new functions. For
computationally intensive tasks, C, C++ and Fortran code can be linked
and called at run time.

%package -n %{libname}
Summary:	Standalone math library from the R project
Group:		Development/Other

%description -n %{libname}
A standalone library of mathematical and statistical functions derived
from the R project.  This packages provides the shared libRmath library.

%package -n %{libname}-devel
Summary:	Standalone math library from the R project
Group:		Development/Other
Provides:	libRmath-devel = %{version}-%{release}
Requires:	%{libname} = %{version}-%{release}

%description -n %{libname}-devel
A standalone library of mathematical and statistical functions derived
from the R project.  This packages provides the static libRmath library
and header files.

%prep
%setup -qn R-%{version}
%patch0 -p1
#%patch2 -p1
#%patch3 -p1 -b .cve
%patch5 -p1
%if %{with system_pcre}
%patch6 -p1
%endif

#perl -pi -e "s/firefox/mozilla-firefox/" m4/R.m4 configure
#rm -f acinclude.m4
aclocal -I ./m4
autoconf --force
#autoreconf -fiv

%build
export R_BROWSER="$(type -p xdg-open)"
export R_PDFVIEWER="$(type -p xdg-open)"
export R_PRINTCMD="lpr"
#export R_BROWSER="%{_bindir}/mozilla-firefox"

# (tpg) do not set R_LIBS #37781
#echo 'R_LIBS=${R_LIBS-'"'%{_libdir}/R/lib'"'}' >> etc/Renviron.in
# (tpg) try to not build with -ffast-math
export CFLAGS=$(echo "%{optflags}" | sed -e s/-ffast-math/-fno-fast-math/g )
export CFLAGS="%{optflags}"
export FFLAGS=$CFLAGS
export CXXFLAGS=$CFLAGS
export FCFLAGS=$CFLAGS
export OBJCFLAGS=$CFLAGS
export F77="gfortran"
%if %{use_java}
export JAVA_HOME="%{java_home}"
%endif
export FPICFLAGS=-fPIC
unset DISPLAY

%configure2_5x \
	--with-tcltk \
	--with-tcl-config=%{_libdir}/tclConfig.sh \
	--with-tk-config=%{_libdir}/tkConfig.sh \
	--with-cairo \
	--with-libpng \
	--with-jpeglib \
	--with-system-zlib \
	--with-system-bzlib \
%if %{with system_pcre}
	--with-system-pcre \
%else
	--without-system-pcre \
%endif
	--with-system-xz \
	--with-ICU \
	--with-readline \
	%if %mdkversion >= 200900
	--disable-BLAS-shlib \
	%else
	--enable-BLAS-shlib \
	%endif
	%if %mdkversion >= 200900
	--with-lapack=%{_libdir} \
	--with-blas=%{_libdir} \
	%endif
	--enable-threads=pth \
	--enable-R-profiling \
	--enable-R-shlib

# (tpg) somehow --prefix is not honored
sed -i -e 's#/usr/local#%{_prefix}#g' Makeconf

%make

pushd src/nmath/standalone
make
popd

%make pdf
%make info

# DON'T comment "make check" below! If R doesn't pass the 'check' test
# then it is probably badly compiled, or there are problems with
# the compiler.

# (tpg) disable for now checks for ix86, because they fails only in iurt!
#%ifarch %{ix86}
#%check
#make check
#%endif

%install
rm -rf %{buildroot}

# (tpg) makeinstall_std is broken here
%makeinstall install-info rhome=%{buildroot}%{_libdir}/R

pushd src/nmath/standalone
%makeinstall \
    includedir=%{buildroot}%{_includedir} \
    libdir=%{buildroot}%{_libdir}
popd

mv doc/manual/*.pdf %{_builddir}/R-%{version} || :
# Add soft links (useful for TK gui)
for i in R-admin R-data refman R-exts R-FAQ R-intro R-lang; do
	ln -s %{_datadir}/doc/R-base/${i}.pdf %{buildroot}%{_libdir}/R/doc/manual/${i}.pdf
done

# Remove latex versions of help pages
#
rm -rf %{buildroot}%{_libdir}/R/library/*/latex/

# Get rid of buildroot in script
for i in %{buildroot}%{_libdir}/R/bin/R %{buildroot}%{_bindir}/R %{buildroot}%{_libdir}/pkgconfig/libR*.pc;
do
  sed -i "s|%{buildroot}||g" $i;
done

# Remove package indices. They are rebuilt by the postinstall script.
#
rm -f %{buildroot}%{_libdir}/R/doc/html/function.html
rm -f %{buildroot}%{_libdir}/R/doc/html/packages.html
rm -f %{buildroot}%{_libdir}/R/doc/html/search/index.txt

# Fix permissions
chmod 644 %{buildroot}%{_libdir}/R/library/MASS/scripts/*
chmod 755 %{buildroot}%{_libdir}/R/share/sh/echo.sh

mkdir -p %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/mandriva-%{name}.desktop <<EOF
[Desktop Entry]
Name=R
Comment=A language for statistical computing
Exec=%{_bindir}/R --gui=tk
Terminal=true
Type=Application
Icon=Rlogo
Categories=Science;Math;
EOF

# icons
mkdir -p %{buildroot}%{_iconsdir}
tar xjf %{SOURCE1} -C %{buildroot}%{_iconsdir}

# remove unpackaged files
rm -f %{buildroot}%{_infodir}/dir{,.old*}

# remove private perl libraries
rm -rf %{buildroot}%{_libdir}/R/share/perl/File
rm -rf %{buildroot}%{_libdir}/R/share/perl/Text

# (tpg) add bash completion file
mkdir -p %{buildroot}%{_sysconfdir}/bash_completion.d
bzcat %{SOURCE2} > %{buildroot}%{_sysconfdir}/bash_completion.d/R-base

# cleanups
rm -f %{buildroot}%{_libdir}/*.*a

%post
%_install_info R-admin.info
%_install_info R-data.info
%_install_info R-exts.info
%_install_info R-FAQ.info
%_install_info R-intro.info
%_install_info R-lang.info
%{_bindir}/R CMD perl %{_libdir}/R/share/perl/build-help.pl --htmllist > /dev/null 2>&1
cat %{_libdir}/R/library/*/CONTENTS > %{_libdir}/R/doc/html/search/index.txt 2>/dev/null || :

%preun 
if [ $1 = 0 ]; then
rm -f %{_libdir}/R/doc/html/function.html \
	 %{_libdir}/R/doc/html/packages.html \
	 %{_libdir}/R/doc/html/search/index.txt
%_remove_install_info R-admin.info
%_remove_install_info R-data.info
%_remove_install_info R-exts.info
%_remove_install_info R-FAQ.info
%_remove_install_info R-intro.info
%_remove_install_info R-lang.info
fi

%files
%doc README VERSION NEWS
%doc R-admin.pdf R-data.pdf R-exts.pdf R-FAQ.pdf R-intro.pdf R-lang.pdf refman.pdf
%{_sysconfdir}/bash_completion.d/*
%{_bindir}/R
%{_bindir}/Rscript
%{_mandir}/*/*
%{_libdir}/R
%{_infodir}/*.info*
%{_iconsdir}/*.*
%{_liconsdir}/*.*
%{_miconsdir}/*.*
%{_datadir}/applications/*.desktop
%{_libdir}/pkgconfig/libR.pc

%files -n %{libname}
%{_libdir}/libRmath.so

%files -n %{libname}-devel
%{_includedir}/Rmath.h
%{_libdir}/pkgconfig/libRmath.pc
