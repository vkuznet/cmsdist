### RPM cms das 04.00.12
## INITENV +PATH PYTHONPATH %i/${PYTHON_LIB_SITE_PACKAGES}

%define pkg0 das2go
%define ver0 %realversion
%define pkg1 DASTools
%define ver1 00.00.04
Source0: https://github.com/dmwm/%pkg0/archive/%ver0.tar.gz
Source1: https://github.com/dmwm/%pkg1/archive/%ver1.tar.gz

Requires: go jemalloc yui mongo rotatelogs

# RPM macros documentation
# http://www.rpm.org/max-rpm/s1-rpm-inside-macros.html
%prep
%setup -D -T -b 1 -n %pkg1-%ver1
%setup -D -T -b 0 -n %pkg0-%ver0

%build
cd ..
mkdir -p gopath
export GOPATH=$PWD/gopath
# build das2go
cd %pkg0-%ver0
echo "start das2go build: $PWD"
mkdir -p $GOPATH/src/github.com/dmwm/das2go
cp -r * $GOPATH/src/github.com/dmwm/das2go
go get github.com/shirou/gopsutil
go get github.com/dmwm/cmsauth
go get github.com/vkuznet/x509proxy
go get gopkg.in/yaml.v2
go get gopkg.in/mgo.v2
go get github.com/sirupsen/logrus
cd $GOPATH/src/github.com/dmwm/das2go
git clone https://github.com/dmwm/das2go.git
cp -r das2go/.git .
rm -rf das2go
make
cd -

# build das tools
cd ../%pkg1-%ver1
echo "start DASTools build: $PWD"
mkdir -p $GOPATH/src/github.com/dmwm/DASTools
cp -r * $GOPATH/src/github.com/dmwm/DASTools
cd $GOPATH/src/github.com/dmwm/DASTools
git clone https://github.com/dmwm/DASTools.git
cp -r DASTools/.git .
rm -rf DASTools
make
cd -

%install
# install das2go
cd ..
echo "start das2go install: $PWD"
export GOPATH=$PWD/gopath
mkdir -p %i/bin
cp $GOPATH/src/github.com/dmwm/das2go/das2go %i/bin
cp $GOPATH/src/github.com/dmwm/das2go/bin/das2go_server %i/bin
mkdir -p %i/das2go/yui
cp -r $GOPATH/src/github.com/dmwm/das2go/{js,css,images,templates} %i/das2go/
export YUI_ROOT
cp -r $YUI_ROOT/build %i/das2go/yui/

# install das tools
echo "start DASTools install: $PWD"
export GOPATH=$PWD/gopath
cp $GOPATH/src/github.com/dmwm/DASTools/bin/* %i/bin

# Generate dependencies-setup.{sh,csh} so init.{sh,csh} picks full environment.
%addDependency

%post
%{relocateConfig}etc/profile.d/dependencies-setup.*sh

%files
%{installroot}/%{pkgrel}/
%exclude %{installroot}/%{pkgrel}/doc
