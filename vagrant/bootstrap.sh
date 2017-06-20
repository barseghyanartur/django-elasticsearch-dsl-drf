# ElasticSearch 2.x installer for Vagrant.
# Separatad in steps. Most of the steps are obligatory. Optional steps could be skipped. 
# Install Java 8
echo "Java 8 installation"
apt-get install --yes python-software-properties
apt-get install --yes software-properties-common
add-apt-repository ppa:webupd8team/java
apt-get update -qq
echo debconf shared/accepted-oracle-license-v1-1 select true | /usr/bin/debconf-set-selections
echo debconf shared/accepted-oracle-license-v1-1 seen true | /usr/bin/debconf-set-selections
apt-get install --yes oracle-java8-installer
yes "" | apt-get -f install

# Install ElasticSearc 2.x
echo "ElasticSearch 2.x installation"
wget -qO - https://packages.elastic.co/GPG-KEY-elasticsearch | sudo apt-key add -
echo "deb http://packages.elastic.co/elasticsearch/2.x/debian stable main" | sudo tee -a /etc/apt/sources.list.d/elasticsearch-2.x.list
sudo apt-get update && sudo apt-get install elasticsearch

# Configure ElasticSearch
echo "ElasticSearch 2.x configuration"
sudo update-rc.d elasticsearch defaults 95 10

# Install additional ElasticSearch plugins (this step can be skipped!)
cd /usr/share/elasticsearch
./bin/plugin install mobz/elasticsearch-head

# Either of the next two lines is needed to be able to access "localhost:9200" from the host os
sudo echo "network.bind_host: 0" >> /etc/elasticsearch/elasticsearch.yml
sudo echo "network.host: 0.0.0.0" >> /etc/elasticsearch/elasticsearch.yml
#sudo echo "http.port: 9200" >> /etc/elasticsearch/elasticsearch.yml

# Enable CORS
sudo echo "http.cors.enabled: true" >> /etc/elasticsearch/elasticsearch.yml

# Start the ElasticSearch
sudo /etc/init.d/elasticsearch start
