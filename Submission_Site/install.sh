#!/bin/bash

if [[ $EUID -ne 0 ]]; then
   echo "This script must be run as root" 1>&2
   exit 1
fi

apt-get update
apt-get install apache2 mysql-server mysql-workbench php5 libapache2-mod-php5 php5-mysqlnd -y

echo >> /etc/apache2/apache2.conf
echo "#php stuff" >> /etc/apache2/apache2.conf
echo AddHandler php5-script .php >> /etc/apache2/apache2.conf
echo AddType application/x-httpd-php .php .html >> /etc/apache2/apache2.conf
echo DirectoryIndex index.php index.phtml index.html index.htm >> /etc/apache2/apache2.conf
echo LoadModule php5_module modules/libphp5.so >> /etc/apache2/apache2.conf

service apache2 restart
service httpd restart