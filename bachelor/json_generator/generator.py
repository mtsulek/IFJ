import time
import json
import random
import threading
import sys
from kafka import KafkaProducer
# GLOBAL
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
        self.producer = KafkaProducer(bootstrap_servers='192.245.169.38',client_id="python-test-consumer")

    def run(self):
        while True:
            self.data = {"detectorID": self.threadID, "latitude": self.coordinateLatitude, "longitude": self.coordinateLongitude, "altitude": self.coordinateAltitude, "timestamp": time.time()}
            print(str(self.data) + '\n')
            # self.producer.flush(self.data)
            self.producer.send('foobar',value=b'dane jakies',key=None)
            time.sleep(random.uniform(0.1,1.5))

def createRandomDetector(count):
    threads = list(range(0,count))
    for thread in range(0, count):
        # try:
        threads[thread] = myThread(thread, "Detector-" + str(thread), thread) #, th_curs
        detectors.append(threads[thread])
        # except: 
        #     print('cant do shit! - create detector')

def startStreaming(count):
    for detector in range (0, count):
        try:
            detectors[detector].start()
        except: 
            print('cant do shit! - stream')

    

# MAIN #####################
numberOfDetectors=5
createRandomDetector(numberOfDetectors)
startStreaming(numberOfDetectors)



