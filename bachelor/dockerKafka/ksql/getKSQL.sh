#!/bin/sh
cd ~/kafkaStreams
git clone https://github.com/confluentinc/ksql.git
cd ksql/docs/quickstart
docker-compose up -d
docker-compose exec ksql-cli ksql-cli local --bootstrap-server kafka:29092

