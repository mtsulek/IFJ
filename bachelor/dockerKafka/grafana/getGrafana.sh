#!/bin/sh
#Grafana install
sudo add-apt-repository "deb https://packagecloud.io/grafana/stable/debian/ jessie main"
curl https://packagecloud.io/gpg.key | sudo apt-key add -
sudo apt-get update
sudo apt-get install grafana
sudo service grafana-server start
