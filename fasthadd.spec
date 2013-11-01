%global commit d0b06280410956a3f98d42cfb40fc9ae4a717ac5
%global shortcommit %(c=%{commit}; echo ${c:0:7})

Name:           fasthadd
Version:        1.0
Release:        1%{?dist}
Summary:        A program to add ProtocolBuffer-formatted ROOT files in a quick way

Group:          Applications/System
License:        GPLv2+
URL:            https://github.com/cms-sw/cmssw
Source0:        https://github.com/rovere/cmssw/archive/%{commit}/%{name}-%{version}-%{shortcommit}.tar.gz
BuildRoot:      %{_topdir}/BUILDROOT/%{name}-%{version}-%{release}

BuildRequires:  root, protobuf-devel >= 2.4.1, protobuf-compiler >= 2.4.1
Requires:       root, protobuf >= 2.4.1

%description
A program to add ProtocolBuffer-formatted ROOT files in a quick way

%prep
%setup -q -n cmssw-%{commit}


%build
mkdir %{name}
cd %{name}
cp %{_builddir}/cmssw-%{commit}/DQMServices/Components/test/fastHadd.cc .
sed -i -e s#DQMServices/Core/src/ROOTFilePB.pb.h#ROOTFilePB.pb.h# fastHadd.cc
cp %{_builddir}/cmssw-%{commit}/DQMServices/Core/src/ROOTFilePB.proto .
protoc -I ./ --cpp_out=./ ROOTFilePB.proto
g++ -O2 -o fasthadd ROOTFilePB.pb.cc fastHadd.cc `pkg-config --libs protobuf` `root-config --cflags --libs | sed -e s/-lGraf3d// | sed -e s/-lPhysics//`


#make %{?_smp_mflags}


%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{_bindir}/
cp -p %{name}/fasthadd %{buildroot}%{_bindir}/


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc
%{_bindir}/*


%changelog
