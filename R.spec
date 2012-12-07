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

#-----------------------------------------------------------------------
Name:		R
Version:	2.15.1
Release:	3
Summary:	A language for data analysis and graphics
URL:		http://www.r-project.org
Source0:	ftp://cran.r-project.org/pub/R/src/base/R-2/R-%{version}.tar.gz
Source1:	macros.R
Source2:	R-make-search-index.sh
Source3:	R-icons-png.tar.bz2
Source4:	R.bash_completion.bz2
Source100:	R.rpmlintrc
License:	GPLv2+
Group:		Sciences/Mathematics
BuildRequires:	bison
BuildRequires:	pkgconfig(blas)
BuildRequires:	bzip2-devel
BuildRequires:	pkgconfig(cairo)
BuildRequires:	cups-common
BuildRequires:	gcc-c++
BuildRequires:	gcc-gfortran
BuildRequires:	gcc-objc
BuildRequires:	gettext-devel
BuildRequires:	glibc-static-devel
BuildRequires:	gpm-devel
BuildRequires:	icu-devel >= 49
%if %{with java}
BuildRequires:	java-rpmbuild
%endif
BuildRequires:	jpeg-devel
BuildRequires:	pkgconfig(lapack)
BuildRequires:	less
BuildRequires:	pkgconfig(ice)
BuildRequires:	pkgconfig(sm)
BuildRequires:	pkgconfig(x11)
BuildRequires:	pkgconfig(xmu)
BuildRequires:	pkgconfig(xt)
BuildRequires:	pkgconfig(ncurses)
BuildRequires:	pkgconfig(pango)
BuildRequires:	paper-utils
%if %{with system_pcre}
BuildRequires:	pkgconfig(libpcre)
%endif
BuildRequires:	pkgconfig(libpng)
BuildRequires:	pth-devel
BuildRequires:	readline-devel
BuildRequires:	tcl-devel
BuildRequires:	texinfo
BuildRequires:	texlive
BuildRequires:	tiff-devel
BuildRequires:	tk-devel
BuildRequires:	zip
BuildRequires:	zlib-devel
# R-devel will pull in R-core
Requires:	R-devel = %{EVRD}
# libRmath-devel will pull in libRmath
Requires:	%{libRmath_devel} = %{EVRD}
Suggests:	x11-font-adobe-100dpi
Obsoletes:	R-recommended <= 1.5.1
Provides:	R-recommended
Patch1:		R-2.8.1-menu.patch
Patch2:		R-2.10.1-gfxdemos.patch

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
Requires:	gawk
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
Requires:	bzip2-devel
Requires:	gcc-c++
Requires:	gcc-gfortran
Requires:	libx11-devel
%if %{with system_pcre}
Requires:	pcre-devel
%endif
Requires:	pkgconfig
Requires:	tcl-devel
Requires:	texinfo
Requires:	texlive
Requires:	tk-devel
Requires:	zlib-devel
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
Requires:	pkgconfig
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
%patch1 -p1
%patch2 -p1

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

%make
make -C src/nmath/standalone

#make check-all
%make pdf
%make info

# Convert to UTF-8
for i in doc/manual/R-intro.info doc/manual/R-FAQ.info doc/FAQ doc/manual/R-admin.info doc/manual/R-exts.info-1; do
    iconv -f iso-8859-1 -t utf-8 -o $i{.utf8,}
    mv $i{.utf8,}
done

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


%changelog
* Tue Aug 21 2012 Paulo Andrade <pcpa@mandriva.com.br> 2.15.0-2
+ Revision: 815582
- Do not require packages in non free.

* Sun Apr 08 2012 Bernhard Rosenkraenzer <bero@bero.eu> 2.15.0-1
+ Revision: 789887
- Rebuild w/ current icu
- Update to 2.15.0

* Thu Feb 23 2012 Paulo Andrade <pcpa@mandriva.com.br> 2.14.1-3
+ Revision: 779406
- Add a compile time flag to upgrade cleanly from R 2.12.

* Tue Feb 21 2012 Paulo Andrade <pcpa@mandriva.com.br> 2.14.1-2
+ Revision: 778336
- Add documentation symlink from rpm docdir to R docdir.
- Correct rebuild issues with rpmbuild with R-core installed.

* Wed Feb 15 2012 Paulo Andrade <pcpa@mandriva.com.br> 2.14.1-1
+ Revision: 774567
- Update to latest upstream release.
- Rework package to benefit from R2spec.
- Rework R to use fedora R2spec and update to latest version.

* Tue Feb 14 2012 Paulo Andrade <pcpa@mandriva.com.br> 2.12.2-2
+ Revision: 774044
- Correct build with newer libpcre.

  + Oden Eriksson <oeriksson@mandriva.com>
    - rebuilt for new pcre
    - various fixes
    - rebuilt against libtiff.so.5
    - attempt to relink against libpng15.so.15

* Mon Jun 06 2011 Funda Wang <fwang@mandriva.org> 2.12.2-1
+ Revision: 682951
- new version 2.12.2

* Sun Jun 05 2011 Funda Wang <fwang@mandriva.org> 2.12.0-6
+ Revision: 682811
- rebuild for new icu

* Mon Mar 14 2011 Funda Wang <fwang@mandriva.org> 2.12.0-5
+ Revision: 644526
- rebuild for new icu

* Wed Feb 02 2011 Funda Wang <fwang@mandriva.org> 2.12.0-4
+ Revision: 634989
- rebuild
- tighten BR

* Sat Nov 27 2010 Funda Wang <fwang@mandriva.org> 2.12.0-3mdv2011.0
+ Revision: 601641
- rebuild for liblzma

* Mon Nov 08 2010 Funda Wang <fwang@mandriva.org> 2.12.0-2mdv2011.0
+ Revision: 594963
- bump rel
- try to export libR at least

* Sat Nov 06 2010 Tomasz Pawel Gajc <tpg@mandriva.org> 2.12.0-1mdv2011.0
+ Revision: 594193
- disable check on all archs
- run checks only on ix86 arch
- update to new version 2.12.0
- add buildrequires on paper-utils

* Thu Apr 22 2010 Frederik Himpe <fhimpe@mandriva.org> 2.11.0-1mdv2010.1
+ Revision: 537985
- update to new version 2.11.0

* Sun Mar 21 2010 Funda Wang <fwang@mandriva.org> 2.10.1-4mdv2010.1
+ Revision: 526042
- rebuild for new icu

* Sun Jan 10 2010 Oden Eriksson <oeriksson@mandriva.com> 2.10.1-3mdv2010.1
+ Revision: 488740
- rebuilt against libjpeg v8

  + Giuseppe Ghibò <ghibo@mandriva.com>
    - Fix path for PDF manuals (needed by Tk gui).
    - Add graphics (Patch5) demo to list of available demos in Tk Gui menu.
    - make post script of cat of CONTENTS into index.txt more robust.

* Tue Dec 15 2009 Frederik Himpe <fhimpe@mandriva.org> 2.10.1-1mdv2010.1
+ Revision: 479120
- Update to new version 2.10.1
- Remove string format patch: not needed anymore

* Sun Nov 08 2009 Tomasz Pawel Gajc <tpg@mandriva.org> 2.10.0-1mdv2010.1
+ Revision: 463065
- add buildrequires on icu-devel and lzma-devel
- update to new version 2.10.0

  + Olivier Blin <blino@mandriva.org>
    - disable java on mips & arm (from Arnaud Patard)

* Mon Aug 24 2009 Frederik Himpe <fhimpe@mandriva.org> 2.9.2-1mdv2010.0
+ Revision: 420514
- Update to new version 2.9.2
- Update string format patch

* Sat Aug 15 2009 Oden Eriksson <oeriksson@mandriva.com> 2.9.0-2mdv2010.0
+ Revision: 416647
- rebuilt against libjpeg v7

* Sun Jun 14 2009 Tomasz Pawel Gajc <tpg@mandriva.org> 2.9.0-1mdv2010.0
+ Revision: 385948
- update to new version 2.9.0

* Wed Mar 18 2009 Tomasz Pawel Gajc <tpg@mandriva.org> 2.8.1-6mdv2009.1
+ Revision: 357464
- disable for now checks for ix86, because they fails only in iurt
- rebuild
- rebuild
- define _disable_ld_no_undefined 1, because i have no idea how to fix Makefile compressed into tarball, R kernel modules
- patch 1 is not needed anymore
- update to new version 2.8.1
- export compiles flags by using %%setup_compile_flags macro

  + Guillaume Rousse <guillomovitch@mandriva.org>
    - add pth-devel and glibc-static-devel to build dependencies
    - rebuild for latest tk libs

  + Thierry Vignaud <tv@mandriva.org>
    - rebuild for new libreadline

* Fri Oct 31 2008 Tomasz Pawel Gajc <tpg@mandriva.org> 2.8.0-1mdv2009.1
+ Revision: 299061
- disable patch 3 for now
- disable patch 1 for now
- update to new version 2.8.0

* Wed Sep 17 2008 Tomasz Pawel Gajc <tpg@mandriva.org> 2.7.2-2mdv2009.0
+ Revision: 285483
- Patch3: security fix for CVE-2008-3931

* Tue Aug 26 2008 Tomasz Pawel Gajc <tpg@mandriva.org> 2.7.2-1mdv2009.0
+ Revision: 276262
- update to new version 2.7.2

* Thu Aug 07 2008 Tomasz Pawel Gajc <tpg@mandriva.org> 2.7.1-2mdv2009.0
+ Revision: 266675
- disable -ffast-math flag as it breaks tests
- add conditionals for mdv 200900
- Patch1: fix detection of bzip2 version
- Patch2: fix underlinking (work in progress)
- use %%{_prefix} instead of hardcoded /usr/local
- compile against system wide blas and lapack (disabled --enable-BLAS-shlib)
- use pth threads
- use _disable_ld_no_undefined to fix build
- add missing buildrequires on imake, gcc-objc, gcc-objc++ and gettext-devel
- require x11-font-adobe-100dpi
- add buildrequires on zip
- do not set R_LIBS variable (#37781)
- add requires on x11-font-adobe-75dpi, as it was pointed on cooker ML
- try to build with enabled -ffast-math
- update to new version 2.7.1

  + Thierry Vignaud <tv@mandriva.org>
    - rebuild early 2009.0 package (before pixel changes)

  + Pixel <pixel@mandriva.com>
    - rpm filetriggers deprecates update_menus/update_scrollkeeper/update_mime_database/update_icon_cache/update_desktop_database/post_install_gconf_schemas
    - fix typo calling %%clean_icon_cache in %%postun
    - do not call ldconfig in %%post/%%postun, it is now handled by filetriggers

* Thu Apr 24 2008 Tomasz Pawel Gajc <tpg@mandriva.org> 2.7.0-4mdv2009.0
+ Revision: 197249
- add buildrequires on pango, cairo and tiff

* Thu Apr 24 2008 Tomasz Pawel Gajc <tpg@mandriva.org> 2.7.0-3mdv2009.0
+ Revision: 197243
- new version

* Mon Feb 11 2008 Tomasz Pawel Gajc <tpg@mandriva.org> 2.6.2-3mdv2008.1
+ Revision: 165448
- revert my last commit (lapack & blas)
- use system blas and lapack libraries
- add bash completion file

* Mon Feb 11 2008 Tomasz Pawel Gajc <tpg@mandriva.org> 2.6.2-2mdv2008.1
+ Revision: 165176
- use xdg-open instead of hardcoding pdfviewer and web browser

* Sun Feb 10 2008 Tomasz Pawel Gajc <tpg@mandriva.org> 2.6.2-1mdv2008.1
+ Revision: 164979
- enable java support
- add missing build requires on bison and paper-utils
- export FCFLAGS and OBJCFLAGS
- use xpdf as a default pdf viewer
- do not compile with -ffast-math, as it breaks checks
- new version 2.6.2

* Wed Dec 19 2007 Tomasz Pawel Gajc <tpg@mandriva.org> 2.6.1-4mdv2008.1
+ Revision: 133819
- fix exceptions for package requires

* Sun Dec 16 2007 Tomasz Pawel Gajc <tpg@mandriva.org> 2.6.1-3mdv2008.1
+ Revision: 120664
- add requires exceptions on perl(R::*)
- new license policy
- do not package COPYING file
- add missing scriplets

* Wed Dec 12 2007 Guillaume Rousse <guillomovitch@mandriva.org> 2.6.1-2mdv2008.1
+ Revision: 118467
- don't provide private perl libraries
  don't even ship private copies of standard ones

* Tue Nov 27 2007 Tomasz Pawel Gajc <tpg@mandriva.org> 2.6.1-1mdv2008.1
+ Revision: 113286
- new version

* Tue Oct 09 2007 Tomasz Pawel Gajc <tpg@mandriva.org> 2.6.0-1mdv2008.1
+ Revision: 96121
- new version
- requires tk

* Fri Sep 07 2007 Anssi Hannula <anssi@mandriva.org> 2.5.1-3mdv2008.0
+ Revision: 82069
- buildrequires tcl-devel
- rebuild for new soname of tcl

* Thu Sep 06 2007 Adam Williamson <awilliamson@mandriva.org> 2.5.1-2mdv2008.0
+ Revision: 81307
- menu entry fix for #33216

* Tue Jul 03 2007 Tomasz Pawel Gajc <tpg@mandriva.org> 2.5.1-1mdv2008.0
+ Revision: 47695
- drop patch 1
- new version

* Sat Jun 16 2007 Tomasz Pawel Gajc <tpg@mandriva.org> 2.5.0-7mdv2008.0
+ Revision: 40396
- blacklist self-requires on libraries

* Sat Jun 16 2007 Tomasz Pawel Gajc <tpg@mandriva.org> 2.5.0-6mdv2008.0
+ Revision: 40300
- really remove unneeded requires
- blacklist libraries as a provides

* Fri Jun 15 2007 Tomasz Pawel Gajc <tpg@mandriva.org> 2.5.0-5mdv2008.0
+ Revision: 39940
- blacklist lapack.so from provides
- fix bug #31177
- evince is now default pdf viewer
- fix file list
- get rid of ld.so.conf.d stuff

* Sat May 05 2007 Tomasz Pawel Gajc <tpg@mandriva.org> 2.5.0-4mdv2008.0
+ Revision: 23202
- R doesn't set its own library path, now it does
- correct requires on R and libRmath
- drop unused directory

* Thu May 03 2007 Tomasz Pawel Gajc <tpg@mandriva.org> 2.5.0-3mdv2008.0
+ Revision: 21963
- enable libRmath compiling
- add reworked P1 from Fedora
- added some stuff - hope rkward will work

* Mon Apr 30 2007 Tomasz Pawel Gajc <tpg@mandriva.org> 2.5.0-2mdv2008.0
+ Revision: 19462
- remove buildrequires on liblapack-devel
- drop P0 (seems to be not needed)
- revoke dead configure options and add new ones
- fix buildrequires
- drop old menu style

* Thu Apr 26 2007 Tomasz Pawel Gajc <tpg@mandriva.org> 2.5.0-1mdv2008.0
+ Revision: 18415
- new version
- own missing files

