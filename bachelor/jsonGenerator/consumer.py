import time
import json
import random
import threading
import sys
from kafka import KafkaConsumer
import logging
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-t","--topic", help="name of kafka topic", type=str)
parser.add_argument("-s","--server", help="Kafka server adress and port", type=str)
args = parser.parse_args()

if args.topic:
    print("\tSelected "+ str(args.topic) + " kafka topic")
    topic = args.topic
else:
    topic = "staticDetectors"
    print("\tDefault topic name " + str(topic))

if args.server:
    print("\tSelected "+ str(args.server) + " serwer ip and port")
    server = args.server
else:
    server = "127.0.0.1:9092"
    print("\tlistening on " + str(server))

class myConsumer (threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.stop_event = threading.Event()

    def run(self):
        consumer = KafkaConsumer(bootstrap_servers=server, auto_offset_reset='earliest', consumer_timeout_ms=1000, value_deserializer=lambda m: json.loads(m.decode('ascii')))
        consumer.subscribe([topic])
        while not self.stop_event.is_set():
            for message in consumer:
                print(message.value)
                if self.stop_event.is_set():
                    break

myConsumer().start()


