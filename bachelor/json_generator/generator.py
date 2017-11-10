import time
import json
import random
import threading
import sys
from kafka import KafkaProducer
import logging

# GLOBAL VARIABLES
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
<<<<<<< HEAD
        self.producer = KafkaProducer(bootstrap_servers='192.245.169.38',client_id="python-test-consumer")
=======
        self.producer = KafkaProducer(value_serializer=lambda v: json.dumps(v).encode('utf-8'), bootstrap_servers='192.245.169.38:9092',api_version=(0,10))
>>>>>>> a79f55b2804a062abf2f9f4be3201f3823605f19

    def run(self):
        while True:
            self.data = {"detectorID": self.threadID, "latitude": self.coordinateLatitude, "longitude": self.coordinateLongitude, "altitude": self.coordinateAltitude, "timestamp": time.time()}
            print(str(self.data) + '\n')
<<<<<<< HEAD
            # self.producer.flush(self.data)
            self.producer.send('foobar',value=b'dane jakies',key=None)
=======
            self.producer.send('mateuszTest', value=self.data)
>>>>>>> a79f55b2804a062abf2f9f4be3201f3823605f19
            time.sleep(random.uniform(0.1,1.5))

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
numberOfDetectors=5
createRandomDetector(numberOfDetectors)
startStreaming(numberOfDetectors)



