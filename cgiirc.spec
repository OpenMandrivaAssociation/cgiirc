%define name    cgiirc
%define version 0.5.9
%define release %mkrel 2

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
Requires:	apache
# webapp macros and scriptlets
Requires(post):		rpm-helper >= 0.16-2mdv2007.0
Requires(postun):	rpm-helper >= 0.16-2mdv2007.0
BuildRequires:	rpm-helper >= 0.16-2mdv2007.0
BuildRequires:	rpm-mandriva-setup >= 1.23-1mdv2007.0
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
    Allow from all
</Directory>
EOF

%clean
rm -rf %{buildroot}

%post
%_post_webapp

%postun
%_postun_webapp

%files
%defattr(-,root,root)
%doc README docs/*
%{_datadir}/%{name}
%{_var}/www/%{name}
%{_var}/www/cgi-bin/*
%config(noreplace) %{_sysconfdir}/cgiirc.config
%config(noreplace) %{_webappconfdir}/%{name}.conf
