%global commit a6cfbd2fad5011b6fdb08902efa3595cdc331e7e
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%define files_for_build fastHadd.cc run_fastHadd_tests.sh test_fastHaddMerge.py fastParallelHadd.py

Name:           fasthadd
Version:        2.1
Release:        1%{?dist}
Summary:        A program to add ProtocolBuffer-formatted ROOT files in a quick way

Group:          Applications/System
License:        GPLv2+
URL:            https://github.com/cms-sw/cmssw
Source0:        https://github.com/rovere/cmssw/archive/%{commit}/%{name}-%{version}-%{shortcommit}.tar.gz
BuildRoot:      %{_topdir}/BUILDROOT/%{name}-%{version}-%{release}

BuildRequires:  root, root-physics, root-graf3d, root-tree-player, protobuf-devel >= 2.4.1, protobuf-compiler >= 2.4.1
Requires:       root, root-tree-player, protobuf >= 2.4.1

%description
A program to add ProtocolBuffer-formatted ROOT files in a quick way

%prep
%setup -q -n cmssw-%{commit}


%build
mkdir %{name}
cd %{name}
for f in %{files_for_build}; do cp %{_builddir}/cmssw-%{commit}/DQMServices/Components/test/${f} .; done
sed -i -e s#DQMServices/Core/src/ROOTFilePB.pb.h#ROOTFilePB.pb.h# fastHadd.cc
cp %{_builddir}/cmssw-%{commit}/DQMServices/Core/src/ROOTFilePB.proto .
protoc -I ./ --cpp_out=./ ROOTFilePB.proto
g++ -O2 -o fastHadd ROOTFilePB.pb.cc fastHadd.cc `pkg-config --libs protobuf` `root-config --cflags --libs`


#make %{?_smp_mflags}


%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{_bindir}/
cp -p %{name}/fastHadd %{buildroot}%{_bindir}/
cp -p %{name}/fastParallelHadd.py %{buildroot}%{_bindir}/

%check
mkdir -p test
pushd test
cp ../%{name}/fastHadd .
for f in %{files_for_build}; do cp %{_builddir}/cmssw-%{commit}/DQMServices/Components/test/${f} .; done
export PATH=./:${PATH}
echo $PATH
. ./run_fastHadd_tests.sh
if [ $? -ne 0 ]; then
  exit $?
fi
popd
rm -fr test

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc
%{_bindir}/fastHadd
%{_bindir}/fastParallelHadd.py*

%changelog
