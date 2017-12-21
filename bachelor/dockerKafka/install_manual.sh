#!/bin/sh
#Get elements
bash ./confluent/getConfluentManually.sh
bash ./wurstmeister/getWurstMeister.sh
sudo apt-get install docker-compose -y
sudo apt-get install docker.io -y
rm ~/kafkaStreams/wurstmeister/kafka-docker/docker-compose.yml
cp ./myScripts/docker-compose.yml ~/kafkaStreams/wurstmeister/kafka-docker

#Start Kafka
docker pull wurstmeister/kafka

#docker-compose -f docker-compose.yml up
#docker-compose scale kafka=3
