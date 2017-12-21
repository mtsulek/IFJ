#!/bin/sh
#Download Konfluent
mkdir ~/kafkaStreams
mkdir ~/kafkaStreams/confluent
cd ~/kafkaStreams/confluent
wget http://packages.confluent.io/archive/4.0/confluent-oss-4.0.0-2.11.tar.gz 
tar -xzvf confluent-oss-4.0.0-2.11.tar.gz
#Exports
echo ""
echo "Please paste to .bashrc: 'export PATH=~/kafkaStreams/confluent/confluent-4.0.0/bin:\$PATH'"
echo "after that run: 'confluent start schema-registry'"

#Start Kafka Manually
#./bin/zookeeper-server-start ./etc/kafka/zookeeper.properties
#./bin/kafka-server-start ./etc/kafka/server.properties
#./bin/schema-registry-start ./etc/schema-registry/schema-registry.propertie
