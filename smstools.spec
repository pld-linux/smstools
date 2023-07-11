Summary:	SMS Server Tools
Summary(pl.UTF-8):	Narzędzia serwera SMS
Name:		smstools
Version:	3.1.21
Release:	1
License:	GPL v2
Group:		Applications/Communications
Source0:	http://smstools3.kekekasvi.com/packages/%{name}3-%{version}.tar.gz
# Source0-md5:	6a9f038fb38a49cc3a4f8f14a88fb8af
Source1:	%{name}.sysconfig
Source2:	%{name}.init
Patch0:		enable-statistics.patch
Patch1:		%{name}-Makefile.patch
Patch2:		gcc10.patch
URL:		http://smstools3.kekekasvi.com/
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
%setup -q -n %{name}3
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
%{__make} \
	CC="%{__cc}" \
	CFLAGS="-DNUMBER_OF_MODEMS=64 %{rpmcflags}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/etc/{rc.d/init.d,sysconfig},%{_sbindir},%{_libdir}/%{name}} \
	$RPM_BUILD_ROOT/var/spool/sms/{incoming,outgoing,failed,sent,OTHER}

cp -p examples/smsd.conf.full $RPM_BUILD_ROOT%{_sysconfdir}/smsd.conf
cp -p src/smsd $RPM_BUILD_ROOT%{_sbindir}
cp -p scripts/{email2sms,mysmsd,sendsms,smsevent} $RPM_BUILD_ROOT%{_libdir}/%{name}

cp -p %{SOURCE1} $RPM_BUILD_ROOT/etc/sysconfig/smsd
cp -p %{SOURCE2} $RPM_BUILD_ROOT/etc/rc.d/init.d/smsd

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
%dir %attr(710,root,uucp) /var/spool/sms/
%dir %attr(750,root,root) /var/spool/sms/OTHER
%dir %attr(750,root,root) /var/spool/sms/failed
%dir %attr(750,root,root) /var/spool/sms/incoming
%dir %attr(1730,root,uucp) /var/spool/sms/outgoing
%dir %attr(750,root,root) /var/spool/sms/sent
