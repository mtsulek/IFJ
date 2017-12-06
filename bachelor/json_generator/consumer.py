import time
import json
import random
import threading
import sys
from kafka import KafkaConsumer
import logging

class myConsumer (threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.stop_event = threading.Event()

    def run(self):
        consumer = KafkaConsumer(bootstrap_servers='54.229.196.207:9092',auto_offset_reset='earliest',consumer_timeout_ms=1000)
        consumer.subscribe(['cosmicWatchTest'])
        while not self.stop_event.is_set():
            for message in consumer:
                print(message)
                if self.stop_event.is_set():
                    break

myConsumer().start()
