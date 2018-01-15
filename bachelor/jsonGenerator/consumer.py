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
        consumer = KafkaConsumer(bootstrap_servers='127.0.0.1:29092',auto_offset_reset='earliest',consumer_timeout_ms=1000, value_deserializer=lambda m: json.loads(m.decode('ascii')))
        consumer.subscribe(['mateuszTest2'])
        while not self.stop_event.is_set():
            for message in consumer:
                print(message.value)
                if self.stop_event.is_set():
                    break


myConsumer().start()


