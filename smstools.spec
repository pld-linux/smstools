Summary:	SMS Server Tools
Summary(pl):	Narz�dzia serwera SMS
Name:		smstools
Version:	1.14.8
Release:	1
License:	GPL v2
Group:		Applications/Communications
Source0:	http://www.meinemullemaus.de/smstools/packages/%{name}-%{version}.tar.gz
# Source0-md5:	104b640b3d640431e6b3ac91c1b8ca70
Source1:	%{name}.sysconfig
Source2:	%{name}.init
Patch0:		%{name}-daemonize.patch
Patch1:		%{name}-Makefile.patch
URL:		http://www.meinemullemaus.de/smstools/index.html
BuildRequires:	mm-devel
PreReq:		rc-scripts
Requires(post,preun):	/sbin/chkconfig
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The SMS Server Tools were made to send and receive SMS from one or
many GSM modems. They include a send/receive daemon and some sample
scripts to build an SMS email gateway and for logging into an SQL
database.

%description -l pl
SMS Server Tools jest pakietem stworzonym do wysy�ania i odbierania
SMS�w z jednego lub kilku modem�w GSM. Zawiera demona do wysy�ania i
odbierania przesy�ek oraz zestaw skrypt�w dzi�ki kt�rym mo�na stworzy�
np. bramk� email->SMS.

%prep
%setup -q -n smstools
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

install examples/smsd.conf.full $RPM_BUILD_ROOT/etc/smsd.conf
install bin/{smsd,getsms,putsms} $RPM_BUILD_ROOT%{_sbindir}
install bin/{email2sms,mysmsd,sendsms,smsevent} $RPM_BUILD_ROOT%{_libdir}/%{name}

install %{SOURCE1} $RPM_BUILD_ROOT/etc/sysconfig/smsd
install %{SOURCE2} $RPM_BUILD_ROOT/etc/rc.d/init.d/smsd

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add smsd
if [ -f /var/lock/subsys/smsd ]; then
	/etc/rc.d/init.d/smsd restart 1>&2
else
	echo "Run \"/etc/rc.d/init.d/smsd start\" to start sms daemon."
fi

%preun
if [ "$1" = "0" ]; then
	if [ -f /var/lock/subsys/smsd ]; then
		/etc/rc.d/init.d/smsd stop 1>&2
	fi
	/sbin/chkconfig --del smsd
fi

%files
%defattr(644,root,root,755)
%doc doc/manual.html doc/html examples/smsd.{black,conf.{easy,full}}
%config(noreplace) %verify(not size mtime md5) /etc/smsd.*
%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) /etc/sysconfig/smsd
%attr(754,root,root) /etc/rc.d/init.d/smsd
%attr(755,root,root) %{_sbindir}/*
%dir %{_libdir}/%{name}
%attr(755,root,root) %{_libdir}/%{name}/*
/var/spool/sms
