import time
import json
import random
import threading
import sys
from kafka import KafkaConsumer
import logging
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-t","--topic", help="name of ksql topic", type=str)
args = parser.parse_args()

if args.topic:
    print("\tSelected "+ str(args.topic) + " kafka topic")
    topic = args.topic
else:
    topic = "event60"
    print("\tDefault topic name " + str(topic))

class myConsumer (threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.stop_event = threading.Event()

    def run(self):
        consumer = KafkaConsumer(bootstrap_servers='10.10.100.94:9092',auto_offset_reset='earliest',consumer_timeout_ms=1000, value_deserializer=lambda m: json.loads(m.decode('ascii')))
        consumer.subscribe([topic])
        while not self.stop_event.is_set():
            for message in consumer:
                print(message.value)
                if self.stop_event.is_set():
                    break


myConsumer().start()


