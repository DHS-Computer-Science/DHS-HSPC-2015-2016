#!/bin/bash

if [[ $EUID -ne 0 ]]; then
   echo "This script must be run as root" 1>&2
   exit 1
fi

echo Copying files
rm `cat /etc/apache2/sites-enabled/* | grep -Eo '[^ ]+var/www.*'`/* 2> /dev/null
cp htdocs/* `cat /etc/apache2/sites-enabled/* | grep -Eo '[^ ]+var/www.*'` -r -u
chmod o+rX `cat /etc/apache2/sites-enabled/* | grep -Eo '[^ ]+var/www.*'` -R

printf "Please enter the mysql password for root (or leave blank for default): "

read pass

if [ -z "$pass" ] ; then
  pass=andriy2432
fi

if mysql -u root -e "SET PASSWORD FOR 'root'@'localhost' = PASSWORD('$pass');" > /dev/null 2>&1 ; then
  # all is good, password is set
  echo -n #place holder
elif ! mysql -u root -p"$pass" -e ";" > /dev/null 2>&1; then
  if mysql -u root -ppassword -e ";" > /dev/null 2>&1; then
    mysql -u root -ppassword -e "SET PASSWORD FOR 'root'@'localhost' = PASSWORD('$pass');" > /dev/null 2>&1
  else
    echo mysql password incorrect, maybe try the default one?
    exit
  fi
fi

echo Creating database and tables
mysql -u root -p"$pass" << EOF
DROP DATABASE IF EXISTS hspc;

CREATE DATABASE hspc;
use hspc;

CREATE TABLE hspc.teams (
  team_id INT NOT NULL,
  team_name VARCHAR(45) NULL,
  team_password VARCHAR(60) NULL,
  PRIMARY KEY (team_id));

CREATE TABLE hspc.submissions (
  submission_id INT NOT NULL,
  submission_name VARCHAR(8) NULL,
  team_id INT NULL,
  problem_id INT NULL,
  time INT NULL,
  grade INT NULL,
  submission_ip VARCHAR(15) NULL,
  PRIMARY KEY (submission_id));
EOF

echo
echo to set up accounts, run \`./create_teams.sh\` in the command line
echo
echo
echo Also make sure to change the timestamp in the `cat /etc/apache2/sites-enabled/* | grep -Eo '[^ ]+var/www.*'`/hspc/scoreboard.php file on line 147\(I think\)
#echo To setup user accounts, please navigate to http://www.localhost/createaccount.php