import json
import getpass
import os
import platform
import time
import hashlib
import random
# COSMIC WATCH LIBS
import serial 
import time
import glob
import sys
import signal
import json
from datetime import datetime
from multiprocessing import Process
import random
import logging
# LOCAL LIBS
from DataTemplates import *
from RequestTemplates import *

# APPLICATION SETUP
"""Constant App parameters"""
configFileName = '.CosmicConfig.json'
app_version = 0.02
distro, version, kernel = platform.linux_distribution()
system_version = platform.system() + platform.release() + " " + distro + version
device_model = "Desktop"
device_type = "CosmicWatch"

"""Functions"""
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
    file_.close

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

# Send Data
sendRequest = HttpRequest("https://api.credo.science", "Data")






def signal_handler(signal, frame):
        print('You pressed Ctrl+C!')
        ComPort.close()     
        file.close() 
        sys.exit(0)
def serial_ports():
    """ Lists serial port names
        :raises EnvironmentError:
            On unsupported or unknown platforms
        :returns:
            A list of the serial ports available on the system
    """
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')
        sys.exit(0)
    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result

#if __name__ == '__main__':
#This file is used to save real-time data from the detector. You will have to change the variable ComPort to the 
#   name of the USB port it is plugged into. If the Arduino is not recognized by your computer, make sure you have
#   installed the drivers for the Arduino.
port_list = serial_ports()
if len(port_list) > 1:
    print('Available serial ports:\n')
    for i in range(len(port_list)):
        print('['+str(i+1)+'] ' + str(port_list[i]))
    print('[h] help\n')
    ArduinoPort = input("Select Arduino Port:")
    if ArduinoPort == 'h':
        print('\n===================== help =======================')
        print('1. Is your Arduino connected to the serial USB port?\n')
        print('2. Check that you have the correct drivers installed:\n')
        print('\tMacOS: CH340 driver')
        print('\tWindows: no dirver needed')
        print('\tLinux: no driver needed')
        sys.exit()
else :
    ArduinoPort = 1
print("The selected port is:")
try:
    print(str(port_list[int(ArduinoPort)-1])+'\n')
except:
    print("No device connected!")
    sys.exit() 

fname = "data.dat"
id = device_id
print("Taking data ...")
print("Press ctl+c to terminate process")

signal.signal(signal.SIGINT, signal_handler)
#ComPort = serial.Serial('/dev/cu.wchusbserialfa130') # open the COM Port
ComPort = serial.Serial(port_list[int(ArduinoPort)-1]) # open the COM Port

ComPort.baudrate = 9600          # set Baud rate
ComPort.bytesize = 8             # Number of data bits = 8
ComPort.parity   = 'N'           # No parity
ComPort.stopbits = 1    

counter = 0
logging.basicConfig(level=logging.INFO)
while True:
    data = ComPort.readline()    # Wait and read data 
    # if counter == 0:
    #     file.write("######################################################################\n")
    #     file.write("### Desktop Muon Detector \n")
    #     file.write("### Questions? saxani@mit.edu \n")
    #     file.write("### Comp_time Counts Ardn_time[ms] Amplitude[mV] SiPM[mV] Deadtime[ms]\n")
    #     file.write("### Device ID: "+str(id)+"\n")
    #     file.write("######################################################################\n")
    # file.write(str(datetime.now())+" "+data)
    dataFrameTemplate = MakeDataFrame(1, 210.73, 50.0922, 19.9148, "manual", int(time.time()*1000), None, None, None, None)  #DATA FRAME TO SEND
    dataContent = dataTemplate([dataFrameTemplate], device_id, device_type, device_model, system_version, app_version)   #WHOLE DATA TO SEND
    sendResult = sendRequest(dataContent, AuthenticationToken)
    counter +=1

    # print(dataContent)
    if errors(loginResult[0], loginResult[2]) == False:
        pass
    else:
        exit
        print(sendResult)
    
ComPort.close()     
file.close() 

