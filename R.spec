%define		upgrade_from_2_12		1

# (tpg) really not needed
# for private copy in /usr/lib/R/share/perl/Text/DelimMatch.pm 
%define __noautoprov 'KernSmooth.so\\|MASS.so\\|R_X11.so\\|class.so\\|cluster.so\\|foreign.so\\|grDevices.so\\|grid.so\\|internet.so\\|lapack.so\\|lattice.so\\|libRblas.so\\|libRlapack.so\\|methods.so\\|mgcv.so\\|nlme.so\\|nnet.so\\|rpart.so\\|spatial.so\\|splines.so\\|stats.so\\|survival.so\\|tcltk.so\\|tools.so\\|vfonts.so\\|perl\(R::.*\)'
%define __noautoreq 'libRblas.so\\|libRlapack.so\\|perl\(R::.*\)'
%define _disable_ld_no_undefined 1

%bcond_without	system_pcre

%ifarch %{mips} %{arm}
    %bcond_with	java
%else
    %bcond_without java
%endif

%ifarch x86_64
    %define	java_arch		amd64
%else
    %define	java_arch		%{_arch}
%endif

%define		libRmath		%{mklibname Rmath}
%define		libRmath_devel		%{mklibname -d Rmath}
%define		libRmath_static_devel	%{mklibname -d -s Rmath}

Summary:	A language for data analysis and graphics
Name:		R
Version:	3.1.1
Release:	3
License:	GPLv2+
Group:		Sciences/Mathematics
Url:		http://www.r-project.org
Source0:	ftp://cran.r-project.org/pub/R/src/base/R-3/R-%{version}.tar.gz
Source1:	macros.R
Source2:	R-make-search-index.sh
Source3:	R-icons-png.tar.bz2
Source4:	R.bash_completion.bz2
Source100:	R.rpmlintrc
Patch1:		R-3.0.1-menu.patch
Patch2:		R-3.0.0-gfxdemos.patch
BuildRequires:	bison
BuildRequires:	cups-common
BuildRequires:	gcc-c++
BuildRequires:	gcc-gfortran
BuildRequires:	gcc-objc
%if %{with java}
BuildRequires:	java-rpmbuild
BuildRequires:	java-devel
%endif
BuildRequires:	less
BuildRequires:	paper-utils
BuildRequires:	texinfo
BuildRequires:	texlive
BuildRequires:	zip
BuildRequires:	bzip2-devel
BuildRequires:	gettext-devel
BuildRequires:	glibc-static-devel
BuildRequires:	gpm-devel
BuildRequires:	jpeg-devel
BuildRequires:	pth-devel
BuildRequires:	readline-devel
BuildRequires:	tiff-devel
BuildRequires:	pkgconfig(blas)
BuildRequires:	pkgconfig(cairo)
BuildRequires:	pkgconfig(ice)
BuildRequires:	pkgconfig(icu-i18n)
BuildRequires:	pkgconfig(lapack)
%if %{with system_pcre}
BuildRequires:	pkgconfig(libpcre)
%endif
BuildRequires:	pkgconfig(libpng)
BuildRequires:	pkgconfig(ncurses)
BuildRequires:	pkgconfig(pango)
BuildRequires:	pkgconfig(sm)
BuildRequires:	pkgconfig(tcl)
BuildRequires:	pkgconfig(tk)
BuildRequires:	pkgconfig(x11)
BuildRequires:	pkgconfig(xmu)
BuildRequires:	pkgconfig(xt)
BuildRequires:	pkgconfig(zlib)
# R-devel will pull in R-core
Requires:	R-devel = %{EVRD}
# libRmath-devel will pull in libRmath
Requires:	%{libRmath_devel} = %{EVRD}
Suggests:	x11-font-adobe-100dpi
Obsoletes:	R-recommended <= 1.5.1
Provides:	R-recommended

%description
This is a metapackage that provides both core R userspace and 
all R development components.

R is a language and environment for statistical computing and graphics. 
R is similar to the award-winning S system, which was developed at 
Bell Laboratories by John Chambers et al. It provides a wide 
variety of statistical and graphical techniques (linear and
nonlinear modelling, statistical tests, time series analysis,
classification, clustering, ...).

R is designed as a true computer language with control-flow
constructions for iteration and alternation, and it allows users to
add additional functionality by defining new functions. For
computationally intensive tasks, C, C++ and Fortran code can be linked
and called at run time.

%files

#-----------------------------------------------------------------------
%package	core
Summary:	The minimal R components necessary for a functional runtime
Group:		Sciences/Mathematics
Requires:	cups
Requires:	less
Requires:	perl
Requires:	sed
Requires:	texlive
Requires:	vim
Requires:	xdg-utils
# These are the submodules that R-core provides. Sometimes R modules say they
# depend on one of these submodules rather than just R. These are provided for 
# packager convenience.
%rename R-base
Provides:	R-boot = 1.3.3
Provides:	R-class = 7.3.3
Provides:	R-cluster = 1.14.1
Provides:	R-codetools = 0.2.8
Provides:	R-datasets = %{version}
Provides:	R-foreign = 0.8.46
Provides:	R-graphics = %{version}
Provides:	R-grDevices = %{version}
Provides:	R-grid = %{version}
Provides:	R-KernSmooth = 2.23.6
Provides:	R-lattice = 0.20.0
Provides:	R-MASS = 7.3.16
Provides:	R-Matrix = 1.0.1
Obsoletes:	R-Matrix < 0.999375-7
Provides:	R-methods = %{version}
Provides:	R-mgcv = 1.7.9
Provides:	R-nlme = 3.1.102
Provides:	R-nnet = 7.3.1
Provides:	R-parallel = %{version}
Provides:	R-rpart = 3.1.50
Provides:	R-spatial = 7.3.3
Provides:	R-splines = %{version}
Provides:	R-stats = %{version}
Provides:	R-stats4 = %{version}
Provides:	R-survival = 2.36.10
Provides:	R-tcltk = %{version}
Provides:	R-tools = %{version}
Provides:	R-utils = %{version}

%description	core
A language and environment for statistical computing and graphics.
R is similar to the award-winning S system, which was developed at
Bell Laboratories by John Chambers et al. It provides a wide
variety of statistical and graphical techniques (linear and
nonlinear modelling, statistical tests, time series analysis,
classification, clustering, ...).

R is designed as a true computer language with control-flow
constructions for iteration and alternation, and it allows users to
add additional functionality by defining new functions. For
computationally intensive tasks, C, C++ and Fortran code can be linked
and called at run time.

%post core
    %{_sbindir}/texlive.post
    %if %{with java}
    R CMD javareconf \
	JAVA_HOME=%{_jvmdir}/jre \
	JAVA_CPPFLAGS='-I%{_jvmdir}/java/include\ -I%{_jvmdir}/java/include/linux' \
	JAVA_LIBS='-L%{_jvmdir}/jre/lib/%{java_arch}/server \
	-L%{_jvmdir}/jre/lib/%{java_arch}\ -L%{_jvmdir}/java/lib/%{java_arch} \
	-L/lib\ -L/usr/lib\ -ljvm' \
	JAVA_LD_LIBRARY_PATH=%{_jvmdir}/jre/lib/%{java_arch}/server:%{_jvmdir}/jre/lib/%{java_arch}:%{_jvmdir}/java/lib/%{java_arch}:/usr/java/packages/lib/%{java_arch}:/lib:/usr/lib \
	> /dev/null 2>&1 || exit 0
    %endif

%postun core
    if [ $1 -eq 0 ] ; then
	%{_sbindir}/texlive.post
    fi

%if %{upgrade_from_2_12}
%posttrans core
    if [ ! -e %{_libdir}/R/doc ]; then
	ln -sf %{_docdir}/R %{_libdir}/R/doc
    fi
%endif

%files		core
%{_bindir}/*
%{_datadir}/R
%{_libdir}/R
%exclude %{_libdir}/R/include
%{_prefix}/lib/rpm/R-make-search-index.sh
%{_infodir}/R-*.info*
%{_sysconfdir}/bash_completion.d/*
%{_sysconfdir}/rpm/macros.d/macros.R
%{_mandir}/man1/*
%{_sysconfdir}/ld.so.conf.d/*
%{_texmfdir}/tex/latex/R
%{_iconsdir}/Rlogo.png
%{_liconsdir}/*
%{_miconsdir}/*
%{_datadir}/applications/*
%doc %{_docdir}/R

#-----------------------------------------------------------------------
%package	devel
Summary:	Files for development of R packages
Group:		Development/Other
Requires:	R-core = %{EVRD}
# You need all the BuildRequires for the development version
Requires:	gcc-c++
Requires:	gcc-gfortran
Requires:	texinfo
Requires:	texlive
Requires:	bzip2-devel
Requires:	pkgconfig(x11)
%if %{with system_pcre}
Requires:	pkgconfig(libpcre)
%endif
Requires:	pkgconfig(tcl)
Requires:	pkgconfig(tk)
Requires:	pkgconfig(zlib)
Provides:	R-Matrix-devel = 1.0.1
Obsoletes:	R-Matrix-devel < 0.999375-7

%description	devel
Install R-devel if you are going to develop or compile R packages.

%files		devel
%{_libdir}/pkgconfig/libR.pc
%{_includedir}/R
%{_libdir}/R/include

#-----------------------------------------------------------------------
%package	-n %{libRmath}
Summary:	Standalone math library from the R project
Group:		System/Libraries
Provides:	Rmath = %{EVRD}

%description	-n %{libRmath}
A standalone library of mathematical and statistical functions derived
from the R project.  This package provides the shared libRmath library.

%files		-n %{libRmath}
%{_libdir}/libRmath.so

#-----------------------------------------------------------------------
%package	-n %{libRmath_devel}
Summary:	Headers from the R Standalone math library
Group:		Development/Other
Requires:	%{libRmath} = %{EVRD}
Provides:	Rmath-devel = %{EVRD}

%description	-n %{libRmath_devel}
A standalone library of mathematical and statistical functions derived
from the R project.  This package provides the libRmath header files.

%files		-n %{libRmath_devel}
%{_includedir}/Rmath.h
%{_libdir}/pkgconfig/libRmath.pc

#-----------------------------------------------------------------------
%package	-n %{libRmath_static_devel}
Summary:	Static R Standalone math library
Group:		Development/Other
Requires:	%{libRmath_devel} = %{EVRD}
Provides:	Rmath-static-devel = %{EVRD}

%description	-n %{libRmath_static_devel}
A standalone library of mathematical and statistical functions derived
from the R project.  This package provides the static libRmath library.

%files		-n %{libRmath_static_devel}
%{_libdir}/libRmath.a

########################################################################
%prep
%setup -q
%apply_patches

#-----------------------------------------------------------------------
%build
# Add PATHS to Renviron for R_LIBS_SITE
echo 'R_LIBS_SITE=${R_LIBS_SITE-'"'/usr/local/lib/R/site-library:/usr/local/lib/R/library:%{_libdir}/R/library:%{_datadir}/R/library'"'}' >> etc/Renviron.in
export R_PDFVIEWER="%{_bindir}/xdg-open"
export R_PRINTCMD="lpr"
export R_BROWSER="%{_bindir}/xdg-open"

# instead of "BuildConflicts: R-core" and/or R-foo packages
if [ -x %{bindir}/Rscript ]; then
    mkdir bin
    ln -sf bin/R bin/Rscript
fi

export FCFLAGS="%{optflags}"
%if %{with java}
    export JAVA_HOME="%{java_home}"
%endif

(
    %configure						\
	--with-tcltk					\
	--with-tcl-config=%{_libdir}/tclConfig.sh	\
	--with-tk-config=%{_libdir}/tkConfig.sh		\
	--with-cairo					\
	--with-libpng					\
	--with-jpeglib					\
	--with-system-zlib				\
	--with-system-bzlib				\
%if %{with system_pcre}
	--with-system-pcre				\
%else
	--without-system-pcre				\
%endif
	--with-system-xz				\
	--with-ICU					\
	--with-readline					\
	--disable-BLAS-shlib				\
	--with-lapack=%{_libdir}			\
	--with-blas=%{_libdir}				\
	--enable-R-shlib				\
	--enable-prebuilt-html				\
	rdocdir=%{_docdir}/R				\
	rsharedir=%{_datadir}/R
) | grep -A30 'R is now' - > CAPABILITIES

# (tpg) somehow --prefix is not honored
sed -i -e 's#/usr/local#%{_prefix}#g' Makeconf

%make -j1
make -C src/nmath/standalone

#make check-all
%make pdf
# %make info

# Uncomment once we fix info pages for R
# Convert to UTF-8
#for i in doc/manual/R-intro.info doc/manual/R-FAQ.info doc/FAQ doc/manual/R-admin.info doc/manual/R-exts.info-1; do
#    iconv -f iso-8859-1 -t utf-8 -o $i{.utf8,}
#    mv $i{.utf8,}
#done

#-----------------------------------------------------------------------
%install
make DESTDIR=%{buildroot} install install-info
make DESTDIR=%{buildroot} install-pdf

rm -f %{buildroot}%{_infodir}/dir
rm -f %{buildroot}%{_infodir}/dir.old
install -p CAPABILITIES %{buildroot}%{_docdir}/R

# Install libRmath files
make -C src/nmath/standalone install DESTDIR=%{buildroot}

mkdir -p %{buildroot}/etc/ld.so.conf.d
echo "%{_libdir}/R/lib" > %{buildroot}/etc/ld.so.conf.d/%{name}-%{_arch}.conf

mkdir -p %{buildroot}%{_datadir}/R/library

# Install rpm helper macros
mkdir -p %{buildroot}%{_sysconfdir}/rpm/macros.d
install -m0644 %{SOURCE1} %{buildroot}%{_sysconfdir}/rpm/macros.d

# Install rpm helper script
mkdir -p %{buildroot}%{_prefix}/lib/rpm/
install -m0755 %{SOURCE2} %{buildroot}/usr/lib/rpm/

# Fix html/packages.html
# We can safely use RHOME here, because all of these are system packages.
sed -i 's|\..\/\..|%{_libdir}/R|g' %{buildroot}%{_docdir}/R/html/packages.html

for i in %{buildroot}%{_libdir}/R/library/*/html/*.html; do
  sed -i 's|\..\/\..\/..\/doc|%{_docdir}/R|g' $i
done

# Fix exec bits
chmod +x %{buildroot}%{_datadir}/R/sh/echo.sh
chmod -x %{buildroot}%{_libdir}/R/library/mgcv/CITATION %{buildroot}%{_docdir}/R/CAPABILITIES

# Symbolic link for convenience
# Actually do make the reverse link done in fedora, to avoid the need to
# fight rpm to convert a directory into a symlink if upgrading from
# previous mandriva packages
ln -sf ../%{_lib}/R/include %{buildroot}%{_includedir}/R

%if !%{upgrade_from_2_12}
ln -sf %{_docdir}/R %{buildroot}%{_libdir}/R/doc
%endif

# Symbolic link for LaTeX
mkdir -p %{buildroot}%{_texmfdir}/tex/latex
pushd %{buildroot}%{_texmfdir}/tex/latex
    ln -s ../../../R/texmf/tex/latex R
popd

cp doc/COPYING %{buildroot}%{_docdir}/R

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
tar xjf %{SOURCE3} -C %{buildroot}%{_iconsdir}

# (tpg) add bash completion file
mkdir -p %{buildroot}%{_sysconfdir}/bash_completion.d
bzcat %{SOURCE4} > %{buildroot}%{_sysconfdir}/bash_completion.d/R-base

