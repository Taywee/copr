Name:       jujutsu
Version:    0.8.0
Release:    1%{?dist}
Summary:    A Git-compatible DVCS that is both simple and powerful

License:    MIT
URL:        https://github.com/martinvonz/jj
Source0:    %{url}/archive/refs/tags/v%{version}.tar.gz

%if 0%{?el8} || 0%{?el9}
%else
BuildRequires: cargo >= 1.69
BuildRequires: rust >= 1.69
%endif
BuildRequires: gcc
BuildRequires: git-core
BuildRequires: python3-devel
BuildRequires: openssl-devel
BuildRequires: pkgconf-pkg-config

BuildRequires: pkgconfig(openssl)
BuildRequires: pkgconfig(x11)
BuildRequires: pkgconfig(xcb)
BuildRequires: pkgconfig(zlib)

%description
Jujutsu is a Git-compatible DVCS. It combines features from Git (data model,
speed), Mercurial (anonymous branching, simple CLI free from "the index",
revsets, powerful history-rewriting), and Pijul/Darcs (first-class conflicts),
with features not found in most of them (working-copy-as-a-commit, undo
functionality, automatic rebase, safe replication via rsync, Dropbox, or
distributed file system).

%prep
%autosetup

# Change default optimizations
sed -i '/profile.release/d' Cargo.toml
sed -i '/strip = "debuginfo"/d' Cargo.toml
sed -i '/codegen-units = 1/d' Cargo.toml

echo -e '\n[profile.release]' >> Cargo.toml
echo 'opt-level = "3"' >> Cargo.toml
echo 'strip = true' >> Cargo.toml
echo 'lto = "thin"' >> Cargo.toml
echo 'codegen-units = 1' >> Cargo.toml

%if 0%{?el8} || 0%{?el9}
  curl https://sh.rustup.rs -sSf | sh -s -- --profile minimal -y
%endif


%install
# export CARGO_PROFILE_RELEASE_BUILD_OVERRIDE_OPT_LEVEL=3
%if 0%{?el8} || 0%{?el9}
source "$HOME/.cargo/env"
%endif
cargo install --root=%{buildroot}%{_prefix} --path=.


rm -f %{buildroot}%{_prefix}/.crates.toml \
    %{buildroot}%{_prefix}/.crates2.json
strip --strip-all %{buildroot}%{_bindir}/*


%files
%license LICENSE
%doc README.md
%{_bindir}/jj


%changelog
* Tue Aug 08 2023 Taylor C. Richberger <taywee@gmx.com> - 0.8.0
- chore(update): 0.8.0
