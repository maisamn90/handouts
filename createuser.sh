#!/bin/bash

# Creates a user record for the current Cloud9 user
# or removes the root password if the student is using regular AWS Cloud9
# Author: Matt Rudge

if [[ "$C9_USER" == "root" ]]
then
   echo "Resetting the root password, this will take a moment..."
   sudo cp /etc/mysql/mysql.conf.d/mysqld.cnf /etc/mysql/mysql.conf.d/mysqld.cnf.bak
   echo "Adjusting privileges"
   echo "skip-grant-tables" | sudo tee -a /etc/mysql/mysql.conf.d/mysqld.cnf
   echo "Restarting mysql"
   sudo /etc/init.d/mysql restart
   echo "Removing password"
   sudo mysql -e "USE mysql; UPDATE user SET authentication_string = PASSWORD(''), plugin='mysql_native_password' WHERE User='root'; FLUSH PRIVILEGES;"
   sudo mv /etc/mysql/mysql.conf.d/mysqld.cnf.bak /etc/mysql/mysql.conf.d/mysqld.cnf
   echo "Restarting mysql"
   sudo /etc/init.d/mysql restart
else
   echo "Creating the ${C9_USER} user in MySQL"
   sudo mysql -e "CREATE USER '${C9_USER}'@'%' IDENTIFIED BY '';"
   echo "Granting privileges"
   sudo mysql -e "GRANT ALL PRIVILEGES ON *.* TO '${C9_USER}'@'%' WITH GRANT OPTION;"
fi

echo "Done"
