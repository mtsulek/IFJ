import time
import json
import random
import threading
import sys
from kafka import KafkaProducer
import logging
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-t","--topic", help="name of kafka topic", type=str)
parser.add_argument("-n","--threads", help="number of detectors to be simulated", type=int)
parser.add_argument("-d","--density", help="upper time limit of muon time arrival", type=int)
args = parser.parse_args()

if args.topic:
    print("\tSelected "+ str(args.topic) + " kafka topic")
    topic = args.topic
else:
    topic = "staticDetectors"
    print("\tDefault topic name " + str(topic))

if args.density:
    print("\tSelected "+ str(args.density) + " upper arrival time limit")
    density = args.density
else:
    density = 1.5
    print("\tDefault topic name " + str(density))

if args.threads:
    print("\tSelected "+ str(args.threads) + " number of detectors")
    numberOfDetectors = args.threads
else:
    numberOfDetectors = 2
    print("\tDefault number of detectors: " + str(numberOfDetectors))

# DETECTOR LIST
detectors = []

class myThread (threading.Thread):
    #INITIALIZATION
    def __init__(self, threadID, name, counter): #, cursor
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter
        self.stopped = False
        self.coordinateLatitude = random.uniform(0,90)
        self.coordinateLongitude = random.uniform(0,180)
        self.coordinateAltitude = random.uniform(-500,4000)
        self.producer = KafkaProducer(value_serializer=lambda v: json.dumps(v).encode('utf-8'), bootstrap_servers='10.10.100.94:9092',api_version=(0,10))

    def run(self):
        while True:
            self.data = {"dupa":"dupa","detectorID": self.threadID, "latitude": self.coordinateLatitude, "longitude": self.coordinateLongitude, "altitude": self.coordinateAltitude, "dtimestamp": int(time.time())}
            print(str(self.data) + '\n')
            self.producer.send(topic, value=self.data)
            time.sleep(random.uniform(0.1,density))

def createRandomDetector(count):
    threads = list(range(0,count))
    for thread in range(0,count):
        try:
            threads[thread] = myThread(thread, "Detector-" + str(thread), thread) #, th_curs
            detectors.append(threads[thread])
        except: 
            print('Error - create detector')
            raise 

def startStreaming(count):
    for detector in range (0,count):
        try:
            detectors[detector].start()
        except: 
            print('Error - stream')
            raise

    
# MAIN #####################
logging.basicConfig(level=logging.INFO)
createRandomDetector(numberOfDetectors)
startStreaming(numberOfDetectors)



