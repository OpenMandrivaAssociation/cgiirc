%define name    cgiirc
%define version 0.5.9
%define release %mkrel 8

Name:           %{name}
Version:        %{version}
Release:        %{release}
Summary:        IRC gateway 
License:        Artistic and GPL
Group:		Networking/WWW
URL:            http://cgiirc.sourceforge.net
Source:		http://prdownloads.sourceforge.net/cgiirc/%{name}-%{version}.tar.bz2
Patch0:		%{name}-0.5.8.fhs.patch
Patch1:		%{name}-0.5.7.config.patch
Requires:	webserver
%if %mdkversion < 201010
Requires(post):   rpm-helper
Requires(postun):   rpm-helper
%endif
BuildArch:      noarch
BuildRoot:      %{_tmppath}/%{name}-%{version}

%description
CGI:IRC is a Perl/CGI program that lets you access IRC from a web browser, it
is designed to be flexible and has many uses such as an IRC gateway for an IRC
network, a chat-room for a website or to access IRC when stuck behind a
restrictive firewall.

%prep
%setup -q
%patch0 -p1
%patch1 -p0
chmod 755 docs/*.pl
find . -name .htaccess -exec rm -f {} \;

%install
rm -rf %{buildroot}

install -d -m 755 %{buildroot}%{_var}/www/cgi-bin
install -d -m 755 %{buildroot}%{_var}/www/%{name}
install -d -m 755 %{buildroot}%{_datadir}/%{name}
install -d -m 755 %{buildroot}%{_sysconfdir}

install -m 755 *.cgi %{buildroot}%{_var}/www/cgi-bin
install -m 644 cgiirc.config.full %{buildroot}%{_sysconfdir}/cgiirc.config
cp -r modules %{buildroot}%{_datadir}/%{name}
cp -r interfaces %{buildroot}%{_datadir}/%{name}
cp -r formats %{buildroot}%{_datadir}/%{name}
cp -r images/* %{buildroot}%{_var}/www/%{name}

# apache configuration
install -d -m 755 %{buildroot}%{_webappconfdir}
cat > %{buildroot}%{_webappconfdir}/%{name}.conf <<EOF
# CGI::IRC configuration

Alias /%{name} %{_var}/www/%{name}
  
<Directory %{_var}/www/%{name}>
    Order allow,deny
    Allow from all
</Directory>
EOF

%clean
rm -rf %{buildroot}

%post
%if %mdkversion < 201010
%_post_webapp
%endif

%postun
%if %mdkversion < 201010
%_postun_webapp
%endif

%files
%defattr(-,root,root)
%doc README docs/*
%{_datadir}/%{name}
%{_var}/www/%{name}
%{_var}/www/cgi-bin/*
%config(noreplace) %{_sysconfdir}/cgiirc.config
%config(noreplace) %{_webappconfdir}/%{name}.conf


%changelog
* Sun Dec 05 2010 Oden Eriksson <oeriksson@mandriva.com> 0.5.9-8mdv2011.0
+ Revision: 610133
- rebuild

* Mon Mar 01 2010 Guillaume Rousse <guillomovitch@mandriva.org> 0.5.9-7mdv2010.1
+ Revision: 513155
- rely on filetrigger for reloading apache configuration begining with 2010.1, rpm-helper macros otherwise

* Wed Sep 02 2009 Thierry Vignaud <tv@mandriva.org> 0.5.9-6mdv2010.0
+ Revision: 424795
- rebuild

* Wed Jul 23 2008 Thierry Vignaud <tv@mandriva.org> 0.5.9-5mdv2009.0
+ Revision: 243478
- rebuild

* Wed Jan 02 2008 Olivier Blin <oblin@mandriva.com> 0.5.9-3mdv2008.1
+ Revision: 140692
- restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Sun Aug 19 2007 Guillaume Rousse <guillomovitch@mandriva.org> 0.5.9-3mdv2008.0
+ Revision: 67054
- rebuild

  + Erwan Velu <erwan@mandriva.org>
    - Import cgiirc



* Fri Jun 30 2006 Guillaume Rousse <guillomovitch@mandriva.org> 0.5.9-2mdv2007.0
- relax buildrequires versionning

* Mon Jun 26 2006 Guillaume Rousse <guillomovitch@mandriva.org> 0.5.9-1mdv2007.0
- new version
- %%mkrel
- new webapp macros
- decompress patches

* Fri May 05 2006 Guillaume Rousse <guillomovitch@mandriva.org> 0.5.8-1mdk
- New release 0.5.8
- rediff fhs patch
- backport compatible apache configuration file

* Mon Sep 12 2005 Guillaume Rousse <guillomovitch@mandriva.org> 0.5.7-1mdk
- first mdk release
