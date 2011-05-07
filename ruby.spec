%define rubyxver        1.9
%define rubyver         1.9.2
%define rubylibver      1.9.1
%define _patchlevel     180
%define dotpatchlevel   %{?_patchlevel:.%{_patchlevel}}
%define patchlevel      %{?_patchlevel:-p%{_patchlevel}}
%define arcver          %{rubyver}%{?patchlevel}
%define sitedir         %{_libdir}/ruby/site_ruby

%define rubygems_version    1.4.2
%define minitest_version    1.6.0
%define rake_version        0.8.7
%define rdoc_version        2.5.8
# This is required to ensure that noarch files puts under /usr/lib/... for
# multilib because ruby library is installed under /usr/{lib,lib64}/ruby anyway.
#%define sitedir2        %{_prefix}/lib/ruby/site_ruby
%define _normalized_cpu %(echo `echo %{_target_cpu} | sed 's/^ppc/powerpc/' | sed -e 's|i.86|i386|'`)

Name:                   ruby
Version:                %{rubyver}%{?dotpatchlevel}
Release:                2%{?dist}
License:                Ruby License/GPL - see COPYING
URL:                    http://www.ruby-lang.org/
BuildRoot:              %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:          ncurses-devel gdbm-devel openssl-devel glibc-devel readline-devel bison libX11-devel tk-devel tcl-devel db4-devel

Source:                 ftp://ftp.ruby-lang.org/pub/%{name}/%{rubyxver}/%{name}-%{arcver}.tar.gz
Summary:                An interpreter of object-oriented scripting language
Group:                  Development/Languages
Requires:               %{name}-libs = %{version}-%{release}

%description
Ruby is the interpreted scripting language for quick and easy
object-oriented programming.  It has many features to process text
files and to do system management tasks (as in Perl).  It is simple,
straight-forward, and extensible.


%package libs
Summary:                Libraries necessary to run Ruby
Group:                  Development/Libraries
# ext/bigdecimal/bigdecimal.{c,h} are under (GPL+ or Artistic) which
# are used for bigdecimal.so
License:                (Ruby or GPLv2) and (GPL+ or Artistic)
Provides:               ruby(abi) = %{rubyxver}
Provides:               libruby = %{version}-%{release}
Obsoletes:              libruby <= %{version}-%{release}

%description libs
This package includes the libruby, necessary to run Ruby.


%package devel
Summary:                A Ruby development environment
Group:                  Development/Languages
Requires:               %{name}-libs = %{version}-%{release}

%description devel
Header files and libraries for building a extension library for the
Ruby or an application embedded Ruby.


%package rdoc
Summary:                A tool to generate documentation from Ruby source files
Group:                  Development/Languages
# generators/template/html/html.rb is under CC-BY
License:                (GPLv2 or Ruby) and CC-BY
Requires:               %{name}-irb = %{version}-%{release}
Provides:               rdoc = %{version}-%{release}
Obsoletes:              rdoc <= %{version}-%{release}

%description rdoc
The rdoc is a tool to generate the documentation from Ruby source files.
It supports some output formats, like HTML, Ruby interactive reference (ri),
XML and Windows Help file (chm).


%package irb
Summary:                The Interactive Ruby
Group:                  Development/Languages
Requires:               %{name} = %{version}-%{release}
Provides:               irb = %{version}-%{release}
Obsoletes:              irb <= %{version}-%{release}

%description irb
The irb is acronym for Interactive Ruby.  It evaluates ruby expression
from the terminal.


%package tcltk
Summary:                Tcl/Tk interface for scripting language Ruby
Group:                  Development/Languages
# Many files under ext/tk/sample/ are under TCL
License:                (Ruby or GPLv2) and TCL
Requires:               %{name}-libs = %{version}-%{release}

%description tcltk
Tcl/Tk interface for the object-oriented scripting language Ruby.


%package docs
Summary:                Manuals and FAQs for scripting language Ruby
Group:                  Documentation

%description docs
Manuals and FAQs for the object-oriented scripting language Ruby.


%package ri
Summary:                Ruby interactive reference
Group:                  Documentation
Requires:               %{name}-rdoc = %{version}-%{release}
Provides:               ri = %{version}-%{release}
Obsoletes:              ri <= %{version}-%{release}

%description ri
ri is a command line tool that displays descriptions of built-in
Ruby methods, classes and modules. For methods, it shows you the calling
sequence and a description. For classes and modules, it shows a synopsis
along with a list of the methods the class or module implements.

%package -n rubygem-rake
Summary:                Ruby based make-like utility
Group:                  Development/Languages
Requires:               ruby(abi) = %{rubyxver}
Requires:               ruby(rubygems)
Provides:               rubygem(rake) = %{rake_version}
Obsoletes:              rubygem(rake) <= %{rake_version}

%description -n rubygem-rake
Rake is a Make-like program implemented in Ruby. Tasks and dependencies are
specified in standard Ruby syntax.


%package -n rubygems
Summary:                 The Ruby standard for packaging ruby libraries
Group:                   Development/Libraries
Requires:                ruby(abi) = %{rubyxver}
Requires:                ruby-rdoc
Requires:                gcc ruby-devel
Provides:                ruby(rubygems) = %{rubygems_version}
Obsoletes:               ruby(rubygems) <= %{rubygems_version}

%description -n rubygems
RubyGems is the Ruby standard for publishing and managing third party
libraries


%package -n rubygem-minitest
Summary:                Small and fast replacement for ruby's huge and slow test/unit
Group:                  Development/Languages
Requires:               ruby(abi) = %{rubyxver}
Requires:               ruby(rubygems)
Provides:               rubygem(minitest) = %{minitest_version}
Obsoletes:              rubygem(minitest) <= %{minitest_version}

%description -n rubygem-minitest
minitest/unit is a small and fast replacement for ruby's huge and slow
test/unit. This is meant to be clean and easy to use both as a regular
test writer and for language implementors that need a minimal set of
methods to bootstrap a working unit test suite.

miniunit/spec is a functionally complete spec engine.

miniunit/mock, by Steven Baker, is a beautifully tiny mock object framework.


%prep
%setup -c

%build
pushd %{name}-%{arcver}
export CFLAGS="$RPM_OPT_FLAGS -Wall -fno-strict-aliasing"
%configure \
  --enable-shared \
  --disable-rpath \
  --libdir=%{_libdir} \
  --prefix=%{_prefix} \
  --prefix=/usr \
  --localstatedir=/var \
  --sysconfdir=/etc


make RUBY_INSTALL_NAME=ruby %{?_smp_mflags} COPY="cp -p" %{?_smp_mflags}

popd

%check
pushd %{name}-%{arcver}
make test
popd


%install
rm -rf $RPM_BUILD_ROOT

make -C $RPM_BUILD_DIR/%{name}-%{version}/%{name}-%{arcver} DESTDIR=$RPM_BUILD_ROOT install

# generate ri doc
rubybuilddir=$RPM_BUILD_DIR/%{name}-%{version}/%{name}-%{arcver}
rm -rf %{name}-%{arcver}/.ext/rdoc
LD_LIBRARY_PATH=$RPM_BUILD_ROOT%{_libdir} RUBYLIB=$RPM_BUILD_ROOT%{_libdir}/ruby/%{rubylibver}:$RPM_BUILD_ROOT%{_libdir}/ruby/%{rubylibver}/%{_normalized_cpu}-%{_target_os} make -C $rubybuilddir DESTDIR=$RPM_BUILD_ROOT install-doc


find $RPM_BUILD_ROOT/ -name "*.so" -exec chmod 755 {} \;

%clean
rm -rf $RPM_BUILD_ROOT

%post libs -p /sbin/ldconfig

%postun libs -p /sbin/ldconfig

%files
%defattr(-, root, root, -)
%doc %{name}-%{arcver}/COPYING*
%doc %{name}-%{arcver}/ChangeLog
%doc %{name}-%{arcver}/GPL
%doc %{name}-%{arcver}/LEGAL
%doc %{name}-%{arcver}/NEWS
%doc %{name}-%{arcver}/README
%lang(ja) %doc %{name}-%{arcver}/README.ja
%doc %{name}-%{arcver}/ToDo
%doc %{name}-%{arcver}/doc/ChangeLog-1.8.0
%doc %{name}-%{arcver}/doc/ChangeLog-YARV
%doc %{name}-%{arcver}/doc/NEWS-1.8.7
%{_bindir}/ruby
%{_bindir}/erb
%{_bindir}/testrb
%{_mandir}/man1/ruby.1*
%{_mandir}/man1/erb.1*
%files libs
%defattr(-, root, root, -)
%doc %{name}-%{arcver}/README
%lang(ja) %doc %{name}-%{arcver}/README.ja
%doc %{name}-%{arcver}/COPYING*
%doc %{name}-%{arcver}/ChangeLog
%doc %{name}-%{arcver}/GPL
%doc %{name}-%{arcver}/LEGAL
%dir %{_libdir}/ruby
%dir %{_libdir}/ruby/%{rubylibver}
%dir %{_libdir}/ruby/%{rubylibver}/%{_normalized_cpu}-%{_target_os}
%dir %{_libdir}/ruby/site_ruby
%dir %{_libdir}/ruby/site_ruby/%{rubylibver}/%{_normalized_cpu}-%{_target_os}
## the following files should goes into ruby-rdoc package.
%exclude %{_libdir}/ruby/%{rubylibver}/rdoc.rb
%exclude %{_libdir}/ruby/%{rubylibver}/rdoc
## the following files should go into the ruby-rake
%exclude %{_libdir}/ruby/%{rubylibver}/rake.rb
%exclude %{_libdir}/ruby/%{rubylibver}/rake
## the following files should go into the ruby-rubygems package.
%exclude %{_libdir}/ruby/%{rubylibver}/rbconfig
%exclude %{_libdir}/ruby/%{rubylibver}/rubygems.rb
%exclude %{_libdir}/ruby/%{rubylibver}/ubygems.rb
%exclude %{_libdir}/ruby/%{rubylibver}/rubygems
## the following files shoudl go into the ruby-minitest package.
%exclude %{_libdir}/ruby/%{rubylibver}/minitest
## the following files should goes into ruby-tcltk package.
%exclude %{_libdir}/ruby/%{rubylibver}/*tk.rb
%exclude %{_libdir}/ruby/%{rubylibver}/tcltk.rb
%exclude %{_libdir}/ruby/%{rubylibver}/tk
%exclude %{_libdir}/ruby/%{rubylibver}/tk*.rb
%exclude %{_libdir}/ruby/%{rubylibver}/tkextlib
%exclude %{_libdir}/ruby/%{rubylibver}/%{_normalized_cpu}-%{_target_os}/tcltklib.so
%exclude %{_libdir}/ruby/%{rubylibver}/%{_normalized_cpu}-%{_target_os}/tkutil.so
## the following files should goes into ruby-irb package.
%exclude %{_libdir}/ruby/%{rubylibver}/irb.rb
%exclude %{_libdir}/ruby/%{rubylibver}/irb
## files in ruby-libs from here
%{_libdir}/libruby.so.*
%{_libdir}/ruby/%{rubylibver}/*.rb
%{_libdir}/ruby/%{rubylibver}/bigdecimal
%{_libdir}/ruby/%{rubylibver}/cgi
%{_libdir}/ruby/%{rubylibver}/date
%{_libdir}/ruby/%{rubylibver}/digest
%{_libdir}/ruby/%{rubylibver}/dl
%{_libdir}/ruby/%{rubylibver}/drb
%{_libdir}/ruby/%{rubylibver}/json
%{_libdir}/ruby/%{rubylibver}/net
%{_libdir}/ruby/%{rubylibver}/openssl
%{_libdir}/ruby/%{rubylibver}/optparse
%{_libdir}/ruby/%{rubylibver}/racc
%{_libdir}/ruby/%{rubylibver}/rexml
%{_libdir}/ruby/%{rubylibver}/rinda
%{_libdir}/ruby/%{rubylibver}/ripper
%{_libdir}/ruby/%{rubylibver}/rss
%{_libdir}/ruby/%{rubylibver}/shell
%{_libdir}/ruby/%{rubylibver}/syck
%{_libdir}/ruby/%{rubylibver}/test
%{_libdir}/ruby/%{rubylibver}/uri
%{_libdir}/ruby/%{rubylibver}/webrick
%{_libdir}/ruby/%{rubylibver}/xmlrpc
%{_libdir}/ruby/%{rubylibver}/yaml
%{_libdir}/ruby/%{rubylibver}/%{_normalized_cpu}-%{_target_os}/*.so
%{_libdir}/ruby/%{rubylibver}/%{_normalized_cpu}-%{_target_os}/digest
%{_libdir}/ruby/%{rubylibver}/%{_normalized_cpu}-%{_target_os}/dl
%{_libdir}/ruby/%{rubylibver}/%{_normalized_cpu}-%{_target_os}/enc
%{_libdir}/ruby/%{rubylibver}/%{_normalized_cpu}-%{_target_os}/io
%{_libdir}/ruby/%{rubylibver}/%{_normalized_cpu}-%{_target_os}/json
%{_libdir}/ruby/%{rubylibver}/%{_normalized_cpu}-%{_target_os}/mathn
%{_libdir}/ruby/%{rubylibver}/%{_normalized_cpu}-%{_target_os}/racc
%{_libdir}/ruby/%{rubylibver}/%{_normalized_cpu}-%{_target_os}/rbconfig.rb

%files devel
%defattr(-, root, root, -)
%doc %{name}-%{arcver}/COPYING*
%doc %{name}-%{arcver}/ChangeLog
%doc %{name}-%{arcver}/GPL
%doc %{name}-%{arcver}/LEGAL
%doc %{name}-%{arcver}/README.EXT
%lang(ja) %doc %{name}-%{arcver}/README.EXT.ja
%{_libdir}/libruby.so
%{_libdir}/libruby-static.a
%{_includedir}/ruby-%{rubylibver}/ruby.h
%{_includedir}/ruby-%{rubylibver}/ruby/*.h
%{_includedir}/ruby-%{rubylibver}/ruby/backward/*.h
%{_includedir}/ruby-%{rubylibver}/%{_normalized_cpu}-%{_target_os}/ruby/config.h

%files irb
%defattr(-, root, root, -)
%doc %{name}-%{arcver}/COPYING*
%doc %{name}-%{arcver}/ChangeLog
%doc %{name}-%{arcver}/GPL
%doc %{name}-%{arcver}/LEGAL
%{_bindir}/irb
%{_libdir}/ruby/%{rubylibver}/irb.rb
%{_libdir}/ruby/%{rubylibver}/irb
%{_mandir}/man1/irb.1*


%files rdoc
%defattr(-, root, root, -)
%doc %{name}-%{arcver}/COPYING*
%doc %{name}-%{arcver}/ChangeLog
%doc %{name}-%{arcver}/GPL
%doc %{name}-%{arcver}/LEGAL
%{_bindir}/rdoc
%{_libdir}/ruby/%{rubylibver}/rdoc
%{_libdir}/ruby/%{rubylibver}/rdoc.rb
%{_libdir}/ruby/gems/%{rubylibver}/specifications/rdoc*


%files tcltk
%defattr(-, root, root, -)
%doc %{name}-%{arcver}/COPYING*
%doc %{name}-%{arcver}/ChangeLog
%doc %{name}-%{arcver}/GPL
%doc %{name}-%{arcver}/LEGAL
#%doc tmp-ruby-docs/ruby-tcltk/ext/*
%{_libdir}/ruby/%{rubylibver}/*-tk.rb
%{_libdir}/ruby/%{rubylibver}/tcltk.rb
%{_libdir}/ruby/%{rubylibver}/tk
%{_libdir}/ruby/%{rubylibver}/tk*.rb
%{_libdir}/ruby/%{rubylibver}/tkextlib
%{_libdir}/ruby/%{rubylibver}/%{_normalized_cpu}-%{_target_os}/tcltklib.so
%{_libdir}/ruby/%{rubylibver}/%{_normalized_cpu}-%{_target_os}/tkutil.so

%files ri
%defattr(-, root, root, -)
%doc %{name}-%{arcver}/COPYING*
%doc %{name}-%{arcver}/ChangeLog
%doc %{name}-%{arcver}/GPL
%doc %{name}-%{arcver}/LEGAL
%{_mandir}/man1/ri.1.*
%{_bindir}/ri
%{_datadir}/ri

%files -n rubygem-rake
%defattr(-, root, root, -)
%doc %{name}-%{arcver}/COPYING*
%doc %{name}-%{arcver}/ChangeLog
%doc %{name}-%{arcver}/GPL
%doc %{name}-%{arcver}/LEGAL
%{_bindir}/rake
%{_mandir}/man1/rake.1.*
%{_libdir}/ruby/%{rubylibver}/rake
%{_libdir}/ruby/%{rubylibver}/rake.rb
%{_libdir}/ruby/gems/%{rubylibver}/specifications/rake*

%files -n rubygems
%defattr(-, root, root, -)
%doc %{name}-%{arcver}/COPYING*
%doc %{name}-%{arcver}/ChangeLog
%doc %{name}-%{arcver}/GPL
%doc %{name}-%{arcver}/LEGAL
%{_bindir}/gem
%{_libdir}/ruby/%{rubylibver}/rubygems.rb
%{_libdir}/ruby/%{rubylibver}/ubygems.rb
%{_libdir}/ruby/%{rubylibver}/rbconfig
%{_libdir}/ruby/%{rubylibver}/rubygems


%files -n rubygem-minitest
%defattr(-, root, root, -)
%doc %{name}-%{arcver}/COPYING*
%doc %{name}-%{arcver}/ChangeLog
%doc %{name}-%{arcver}/GPL
%doc %{name}-%{arcver}/LEGAL
%{_libdir}/ruby/%{rubylibver}/minitest
%{_libdir}/ruby/gems/%{rubylibver}/specifications/minitest*


%files docs
%defattr(-, root, root, -)
%doc %{name}-%{arcver}/COPYING*
%doc %{name}-%{arcver}/ChangeLog
%doc %{name}-%{arcver}/GPL
%doc %{name}-%{arcver}/LEGAL
%{_datadir}/doc/ruby

%changelog
* Sat Mar 5 2011 Erik Sabowski <airyk@sabowski.com> 1.9.2-p180-1
- Initial spec for Ruby 1.9 for centos5 w/ split packages
