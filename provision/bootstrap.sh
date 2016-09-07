BASE_PATH="/vagrant"
NGINX_CONFIG_FILE="/provision/nginx.conf"
SERVER_PATH="/server"

echo "installing NGINX..."
echo "==================="
sudo apt-get update
sudo apt-get install -y python python-pip python-virtualenv nginx gunicorn

sudo pip install Flask

if [ -f $BASE_PATH$NGINX_CONFIG_FILE ];
then
    sudo cp $BASE_PATH$NGINX_CONFIG_FILE /etc/nginx/sites-available/default
    echo "Nginx config file was created!!!"
else
    echo "Nginx config file wasn't found!!"
fi

echo "installing NEO4J..."
echo "==================="

echo "installing java"
echo -ne '\n' | sudo add-apt-repository -y ppa:webupd8team/java
sudo apt-get update
echo debconf shared/accepted-oracle-license-v1-1 select true | /usr/bin/debconf-set-selections
echo debconf shared/accepted-oracle-license-v1-1 seen true | /usr/bin/debconf-set-selections
sudo apt-get install --yes oracle-java8-installer


cd ~
wget -O - http://debian.neo4j.org/neotechnology.gpg.key >> key.pgp
sudo apt-key add key.pgp
echo 'deb http://debian.neo4j.org/repo stable/' | sudo tee -a /etc/apt/sources.list.d/neo4j.list > /dev/null
sudo apt-get update &&  sudo apt-get install -y neo4j=2.2.5
sudo sed  -i 's/dbms.security.auth_enabled=true/dbms.security.auth_enabled=false/' /etc/neo4j/neo4j-server.properties
sudo service neo4j-service restart
sudo service nginx restart


sudo pip -v install jsonschema
sudo pip install neomodel

cd $BASE_PATH$SERVER_PATH
gunicorn app:app -b localhost:8000


