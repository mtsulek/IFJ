#!/usr/bin/env python3.6
import json
import getpass
import os
import platform
import time
import hashlib
import random
import multiprocessing
import signal

# INSECURE
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
# Local libs
from cosmicWatchByspenceraxani import CosmicWatch, sys
from DataTemplates import *
from RequestTemplates import HttpRequest


# APPLICATION SETUP
"""Constant App parameters"""
configFileName = '.CosmicConfig.json'
app_version = 0.10
distro, version, kernel = platform.linux_distribution()
system_version = platform.system() + platform.release() + " " + distro + version
device_model = "Desktop"
device_type = "CosmicWatch"

"""Functions"""
def signal_handler(sig, frame):
        print('You pressed Ctrl+C!')
        for process in processes:
            process.killMe()
        Detector.killMe()
        schedulePings.killMe()
        requestPingsProcess.killMe()
        sys.exit(0)

def generateUniqueID(device_model, device_type, user_name):
    id_ = hashlib.md5(bytes(f"{device_model}{device_type}{user_name}", 'utf-8')).hexdigest()
    id_ = str(id_) + str(int(time.time()))
    return id_

def errors(statusCode, content):
    """Chcecks for 400 and 500 status code from server"""
    if statusCode == 400 or statusCode == 500:
        print(f"There is {statusCode} status Code from serwer: \"{json.loads(content)['message']}\"")
        return True
    else:
        return False

def IfConfigExist():
    """Check if configFile exists. If exests return data from file, if not returns false"""
    try:
        with open(configFileName) as configFile:
            _data_ = json.load(configFile)
            return(_data_)
    except:
        return False

def InitiateCosmicWatch():
    """Guide thruu registering process, returns JSON template for http request"""
    print("No config file detected!")
    print("Register your detector:")
    print("email:")
    email = input()
    print("username:")
    user_name = input()
    print("displayName:")
    display_Name = input()

    password = getpass.getpass('password:')
    passwordRepeat = getpass.getpass('repeat your password:')
    if password != passwordRepeat:
        print("Passwords are not the same!")
        InitiateCosmicWatch()
        return 0

    print("team:")
    team = input()
    print("language:")
    language = input()
    
    template = JsonTemplate("Register")
    device_id = generateUniqueID(device_model, device_type, user_name)
    return template(email, user_name, display_Name, password, team, language, device_id, device_type, device_model, system_version, app_version)

def LoginToServer():
    """Asks for username and login and returns JSON template with data for http request"""
    print("To start data streaming, please login:")
    print("username:")
    username = input()
    password = getpass.getpass('password:')
    template = JsonTemplate("Login")
    return template(username, password, device_id, device_type, device_model, system_version, app_version)

class Task(object):
    """Definition of a task for schedule"""
    def __init__(self, counter, whatToDo):
        self.whatToDo = whatToDo
        self.counter = counter
    def __call__(self):
        return [self.counter, self.whatToDo]

class HttpProcess(multiprocessing.Process):
    """Multiprocess for sending data"""
    def __init__(self, task_queue, result_queue):
        multiprocessing.Process.__init__(self)
        self.task_queue = task_queue
        self.result_queue = result_queue
        self.proc_name = self.name
    def run(self):
        q = True
        next_task, answer = None, None
        while True:
            if q == True:
                next_task = self.task_queue.get()
                answer = next_task()
            try:
                sendResult = sendRequest(answer[1], AuthenticationToken)
                print(f'{self.proc_name}: {sendResult[2]}; counter:{answer[0]}')
                self.task_queue.task_done()
                self.result_queue.put(answer)
                q = True
            except:
                time.sleep(1)
                q = False
                pass
        
    def killMe(self):
        self.terminate()

class PingProcess(multiprocessing.Process):
    """Multiprocess for sending data"""
    def __init__(self, task_queue):
        multiprocessing.Process.__init__(self)
        self.task_queue = task_queue
        self.proc_name = self.name

    def run(self):
        q = True
        next_task = None
        answer = None
        while True:
            if q == True:
                next_task = self.task_queue.get()
                answer = next_task()
            try:
                sendResult = pingRequest(answer[1], AuthenticationToken)
                print(f'{self.proc_name}: {sendResult[2]}')
                self.task_queue.task_done()
                q = True
            except:
                time.sleep(1)
                q = False
                pass
        
    def killMe(self):
        self.terminate()

class PingScheduler(multiprocessing.Process):
    """Multiprocess with ping - ping inform for how much time device is up"""
    def __init__(self, sleepTime, pingTasks):
        multiprocessing.Process.__init__(self)
        self.proc_name = self.name
        self.startTime = int(time.time()*1000)
        self.sleepTime = sleepTime
        self.task_queue = pingTasks
    def run(self):
        pingTemplate = JsonTemplate("Ping")
        HttpRequest("https://api.credo.science", "Ping")

        while True:
            currentTime = int(time.time()*1000)
            pingFrame = pingTemplate(currentTime, 0, currentTime - self.startTime, device_id, device_type, device_model, system_version, app_version)
            self.task_queue.put(Task(0, pingFrame))
            time.sleep(self.sleepTime)
    
    def killMe(self):
        self.terminate()


"""Main"""
# Initialization of Detector
config = IfConfigExist()
if config == False:
    registrationTemplate = InitiateCosmicWatch()
    registerRequest = HttpRequest("https://api.credo.science", "Register")
    registerResult = registerRequest(registrationTemplate)
    configFile = open(configFileName,'w')
    device_id = registrationTemplate['device_id']
    if errors(registerResult[0], registerResult[2]) == False:
        del registrationTemplate['password'] 
        configFile.write(json.dumps(registrationTemplate, indent=4))
        configFile.close
        config = IfConfigExist()
    elif json.loads(registerResult[2])['message'] == "Registration failed. Reason: User with given username or email already exists.":
        del registrationTemplate['password']
        configFile.write(json.dumps(registrationTemplate, indent=4))
        configFile.close
        config = IfConfigExist()
        print('Config file recreated!')
else:
    file_ = open(configFileName).read()
    device_id = json.loads(file_)['device_id']
    # file_.close

# Loggin into server
loginTemplate = LoginToServer()
loginRequest = HttpRequest("https://api.credo.science", "Login")
loginResult = loginRequest(loginTemplate)
if errors(loginResult[0], loginResult[2]) == False:
    pass
else:
    sys.exit()
AuthenticationToken = json.loads(loginResult[2])['token']

# Generate data json
dataTemplate = JsonTemplate("Data")

# Send Data and Ping
sendRequest = HttpRequest("https://api.credo.science", "Data")
pingRequest = HttpRequest("https://api.credo.science", "Ping")

# Multiprocessing Tasks
tasks = multiprocessing.JoinableQueue()
results = multiprocessing.Queue()

# Start number of Processes
num_processes = multiprocessing.cpu_count()
processes = [ HttpProcess(tasks, results)
                for i in range(num_processes) ]
for w in processes:
    w.start()

# Initialize Cosmic Watch
Detector = CosmicWatch()
counter = 0
print("Taking data ...")
print("Press ctl+c to terminate process")
signal.signal(signal.SIGINT, signal_handler)

# Run ping processes
pingTasks = multiprocessing.JoinableQueue()
schedulePings = PingScheduler(10, pingTasks)
requestPingsProcess = PingProcess(pingTasks)
schedulePings.start(), requestPingsProcess.start()
# Schedule data to send
while True:
    data = Detector.GatherTheData()    # Wait and read data 
    if counter != 0:
        amplitude = (str(data).split(" ")[3])
        dataFrameTemplate = MakeDataFrame(1, 210.73, 50.0922, 19.9148, "manual", int(time.time()*1000), amplitude, None, None, None) # data framme 
        dataContent = dataTemplate([dataFrameTemplate], device_id, device_type, device_model, system_version, app_version) # whole data frame
        tasks.put(Task(counter, dataContent)) # put task with data to http requests queue
    counter +=1
