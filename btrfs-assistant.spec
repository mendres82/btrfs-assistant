#
# spec file for package btrfs-assistant
#
# Copyright (c) 2022 SUSE LLC
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via https://bugs.opensuse.org/
#


Name:           btrfs-assistant
Version:        0
Release:        0
Summary:        Btrfs Assistant
License:        GPL-3.0-or-later
URL:            https://gitlab.com/btrfs-assistant/btrfs-assistant
Source:         %{name}-%{version}.tar.gz
BuildRequires:  cmake
%if 0%{?suse_version} < 1600
BuildRequires:  gcc13
BuildRequires:  gcc13-c++
%else
BuildRequires:  gcc
BuildRequires:  gcc-c++
%endif
BuildRequires:  libbtrfs-devel
BuildRequires:  libbtrfsutil-devel
BuildRequires:  pkgconfig(systemd)
BuildRequires:  cmake(Qt6Core)
BuildRequires:  cmake(Qt6DBus)
BuildRequires:  cmake(Qt6Widgets)
BuildRequires:  cmake(Qt6LinguistTools)
Requires:       polkit

%description
Btrfs Assistant is a GUI management tool to make managing a Btrfs filesystem easier.  The primary features it offers are:

An easy to read overview of Btrfs metadata
A simple view of subvolumes with or without Snapper/Timeshift snapshots
Run and monitor scrub and balance operations
A pushbutton method for removing subvolumes
A management front-end for Snapper with enhanced restore functionality

View, create and delete snapshots
Restore snapshots in a variety of situations

When the filesystem is mounted in a different distro
When booted off a snapshot
From a live ISO


View, create, edit, remove Snapper configurations
Browse snapshots and restore individual files
Browse diffs of a single file across snapshot versions
Manage Snapper systemd units


A front-end for Btrfs Maintenance

Manage systemd units
Easily manage configuration for defrag, balance and srub settings

%lang_package

%prep
%autosetup -p1

%build
%if 0%{?suse_version} < 1600
export CC=gcc-13
export CXX=g++-13
%endif
%cmake \
  -DCMAKE_BUILD_TYPE=Release \
  -DBTRFS_ASSISTANT_SYSTEMD_UNIT_DIR=%{_unitdir}
%cmake_build

%install
%cmake_install

%check
%ctest

%find_lang btrfsassistant --with-qt

# Do not restart or stop the helper from package scripts; it may be
# mid-operation and exits on its own when idle (see docs/packaging.md).

%pre
%service_add_pre %{name}-helper.service

%post
%service_add_post %{name}-helper.service

%preun
%systemd_preun %{name}-helper.service

%postun
%service_del_postun %{name}-helper.service

%files
%license LICENSE
%doc README.md changelog
%{_bindir}/btrfs-assistant
%config(noreplace) %{_sysconfdir}/btrfs-assistant.conf
%{_datadir}/applications/btrfs-assistant.desktop
%{_datadir}/metainfo/btrfs-assistant.metainfo.xml
%{_datadir}/dbus-1/system.d/org.btrfsassistant.Helper1.conf
%{_datadir}/dbus-1/system-services/org.btrfsassistant.Helper1.service
%dir %{_prefix}/lib/btrfs-assistant/
%{_prefix}/lib/btrfs-assistant/btrfs-assistant-helper
%{_unitdir}/btrfs-assistant-helper.service
%dir %{_datadir}/polkit-1/
%dir %{_datadir}/polkit-1/actions/
%{_datadir}/polkit-1/actions/org.btrfsassistant.policy
%dir %{_datadir}/icons/hicolor
%dir %{_datadir}/icons/hicolor/scalable
%dir %{_datadir}/icons/hicolor/scalable/apps
%{_datadir}/icons/*/*/*/*.svg

%files lang -f btrfsassistant.lang
%dir %{_datadir}/btrfs-assistant/
%dir %{_datadir}/btrfs-assistant/translations/

%changelog
