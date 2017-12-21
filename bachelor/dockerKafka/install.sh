#!/bin/sh
#Get elements
bash ./confluent/getConfluent.sh
bash ./grafana/getGrafana.sh
bash ./wurstmeister/getWurstMeister.sh
bash ./ksql/getKSQL.sh
sudo apt-get install docker-compose -y
sudo apt-get install docker.io -y
rm ~/kafkaStreams/wurstmeister/kafka-docker/docker-compose.yml
cp ./myScripts/docker-compose.yml ~/kafkaStreams/wurstmeister/kafka-docker

#Start Kafka
docker pull wurstmeister/kafka
#docker-compose -f docker-compose.yml up
#docker-compose scale kafka=3
