#Confluent for apt-get Deb/Ubuntu
sudo add-apt-repository ppa:webupd8team/java -y
sudo apt-get update -y
sudo apt-get install oracle-java9-installer -y
wget -qO - https://packages.confluent.io/deb/4.0/archive.key | sudo apt-key add -
sudo add-apt-repository "deb [arch=amd64] https://packages.confluent.io/deb/4.0 stable main"
sudo apt-get update -y && sudo apt-get install confluent-platform-oss-2.11 -y

