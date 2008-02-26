%define version 0.0.14.1
%define release %mkrel 1

%define libggz_version %{version}
%define ggz_client_libs_version %{version}

%define games_list chess chinese-checkers combat dots ggzcards hastings reversi spades tictactoe

Name:		ggz-gtk-games
Summary:	GGZ Games for GTK+ user interface
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		Games/Other
URL:		http://ggzgamingzone.org/
BuildRoot:	%_tmppath/%{name}-%{version}-%{release}-buildroot

Source0:	http://ftp.ggzgamingzone.org/pub/ggz/%{version}/%{name}-%{version}.tar.bz2

BuildRequires:	libggz-devel = %{libggz_version}
BuildRequires:	ggz-client-libs-devel = %{ggz_client_libs_version}
BuildRequires:	bison
BuildRequires:	gtk+2-devel
Requires:	libggz = %{libggz_version}
Requires:	ggz-gtk-client = %{version}
Requires(Pre):	ggz-client-libs = %{ggz_client_libs_version}
Requires(Post):	ggz-client-libs = %{ggz_client_libs_version}
Provides:	ggz-game-modules = %{version}

%description
The complete set of GGZ Gaming Zone games for GTK+ user interface.
Includes all of the following:
    Chess		Chinese Checkers	Combat
    Connect the Dots	GGZCards		Hastings
    La Pocha		Reversi			Spades
    Tic-Tac-Toe

%prep
%setup -q

%build
%configure2_5x --enable-gtk=gtk2 --with-libggz-libraries=%{_libdir} --with-ggzmod-libraries=%{_libdir} --with-ggzcore-libraries=%{_libdir}
%make


%install
rm -rf %{buildroot}
%makeinstall_std

rm %{buildroot}%{_sysconfdir}/ggz.modules
rmdir %{buildroot}%{_sysconfdir}

# Get a copy of all of our .dsc files
mkdir -p %{buildroot}%{_datadir}/ggz/ggz-config
for i in %games_list; do
  install -m 0644 $i/module.dsc %{buildroot}%{_datadir}/ggz/ggz-config/gtk-$i.dsc
done

%find_lang %{name} --all-name

%clean
rm -rf %{buildroot}


%post
# Run ggz-config vs. all installed games
if [ -f %{_sysconfdir}/ggz.modules ]; then
  for i in %games_list; do
    ggz-config --install --modfile=%{_datadir}/ggz/ggz-config/gtk-$i.dsc --force
  done
fi


%preun
# Run ggz-config to uninstall all the games
if [ "$1" = "0" ]; then
  if [ -f %{_sysconfdir}/ggz.modules ]; then
    for i in %games_list; do
      ggz-config --remove --modfile=%{_datadir}/ggz/ggz-config/gtk-$i.dsc
    done
  fi
fi

%files -f %{name}.lang
%defattr(-,root,root)
%doc AUTHORS COPYING ChangeLog INSTALL NEWS README README.GGZ QuickStart.GGZ TODO
%{_libdir}/ggz/*
%{_datadir}/ggz/ccheckers
%{_datadir}/ggz/combat
%{_datadir}/ggz/ggz-config/*
%{_datadir}/ggz/pixmaps/*
%{_datadir}/ggz/chess/pixmaps/*
%{_datadir}/ggz/hastings/pixmaps/*
%{_datadir}/ggz/reversi/pixmaps/*
%{_datadir}/ggz/tictactoe/pixmaps/*


