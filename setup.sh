sudo apt-get update
sudo apt-get install apache2
sudo apt-get install mysql-server libapache2-mod-auth-mysql php5-mysql
sudo mysql_install_db
sudo /usr/bin/mysql_secure_installation
sudo apt-get install apache2.2-common apache2-mpm-prefork apache2-utils libexpat1 ssl-cert
sudo apt-get install libapache2-mod-wsgi
sudo apt-get install python-pip
pip install Django
sudo apt-get install python-dev
sudo apt-get install libmysqlclient-dev
pip install mysql-python
pip install requests
sudo dd if=/dev/zero of=/swapfile bs=1024 count=2048k
sudo mkswap /swapfile
sudo swapon /swapfile
sudo chown root:root /swapfile
sudo chmod 0600 /swapfile
easy_install -U distribute
easy_install mysql-python