### RPM external apache-tomcat 5.5.26
Source: http://download.nextag.com/apache/tomcat/tomcat-5/v5.5.26/bin/apache-tomcat-5.5.26.tar.gz
Requires: java-jdk
%build
source $JAVA_JDK_ROOT/etc/profile.d/init.sh
export JAVA_HOME=$JAVA_JDK_ROOT 
cd bin
tar xfz jsvc.tar.gz
cd jsvc-src
chmod +x configure
./configure
make
%install
cp -r ./* %i

#
