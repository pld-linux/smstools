Summary:	SMS Server Tools
Summary(pl.UTF-8):	Narzędzia serwera SMS
Name:		smstools
Version:	2.2.14
Release:	1
License:	GPL v2
Group:		Applications/Communications
Source0:	http://www.meinemullemaus.de/smstools/packages/%{name}-%{version}.tar.gz
# Source0-md5:	05225fade4eafb7c162adebd749c7282
Source1:	%{name}.sysconfig
Source2:	%{name}.init
Patch0:		%{name}-daemonize.patch
Patch1:		%{name}-Makefile.patch
URL:		http://www.meinemullemaus.de/software/smstools/index.html
BuildRequires:	mm-devel
BuildRequires:	rpmbuild(macros) >= 1.268
Requires(post,preun):	/sbin/chkconfig
Requires:	rc-scripts
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The SMS Server Tools were made to send and receive SMS from one or
many GSM modems. They include a send/receive daemon and some sample
scripts to build an SMS email gateway and for logging into an SQL
database.

%description -l pl.UTF-8
SMS Server Tools jest pakietem stworzonym do wysyłania i odbierania
SMSów z jednego lub kilku modemów GSM. Zawiera demona do wysyłania i
odbierania przesyłek oraz zestaw skryptów dzięki którym można stworzyć
np. bramkę email->SMS.

%prep
%setup -q -n %{name}
%patch0 -p1
%patch1 -p1

%build
%{__make} \
	CC="%{__cc}" \
	CFLAGS="%{rpmcflags}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/etc/{rc.d/init.d,sysconfig},%{_sbindir},%{_libdir}/%{name}} \
	$RPM_BUILD_ROOT/var/spool/sms/{incoming,outgoing,failed,sent,OTHER}

install examples/smsd.conf.full $RPM_BUILD_ROOT%{_sysconfdir}/smsd.conf
install src/smsd $RPM_BUILD_ROOT%{_sbindir}
install scripts/{email2sms,mysmsd,sendsms,smsevent} $RPM_BUILD_ROOT%{_libdir}/%{name}

install %{SOURCE1} $RPM_BUILD_ROOT/etc/sysconfig/smsd
install %{SOURCE2} $RPM_BUILD_ROOT/etc/rc.d/init.d/smsd

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add smsd
%service smsd restart "sms daemon"

%preun
if [ "$1" = "0" ]; then
	%service smsd stop
	/sbin/chkconfig --del smsd
fi

%files
%defattr(644,root,root,755)
%doc doc/* examples/smsd.conf.{easy,full}
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/smsd.*
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/smsd
%attr(754,root,root) /etc/rc.d/init.d/smsd
%attr(755,root,root) %{_sbindir}/*
%dir %{_libdir}/%{name}
%attr(755,root,root) %{_libdir}/%{name}/*
%dir /var/spool/sms/
%attr(750,root,root) /var/spool/sms/OTHER
%attr(750,root,root) /var/spool/sms/failed
%attr(750,root,root) /var/spool/sms/incoming
%attr(770,root,uucp) /var/spool/sms/outgoing
%attr(750,root,root) /var/spool/sms/sent
