import json
import requests
import getpass
import os
import platform
import time
# COSMIC WATCH
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

# APPLICATION SETUP
configFileName = '.CosmicConfig.json'
app_version = 0.01
distro, version, kernel = platform.linux_distribution()
system_version = platform.system() + platform.release() + " " + distro + version
device_model = "Xiaomi Air 13"
device_type = "PC_CosmicWatch"
device_id = "CosmicWatchTest000000000000001"


def errors(statusCode, content):
    """Chcecks for 400 and 500 status code from server"""
    if statusCode == 400 or statusCode == 500:
        print(f"There is {statusCode} status Code from serwer: \"{json.loads(content)['message']}\"")
        return True
    else:
        return False

def IfConfigExist():
    """Check if configFile exists. If exests return data from file, if not returns false"""
    # try:
    with open(configFileName) as configFile:
        _data_ = json.load(configFile)
        return(_data_)
    # except:
    return False

def InitiateCosmicWatch():
    """Guide thruu registering process, returns JSON template for http request"""
    print("No config file detected!")
    print("Register your detector:")

    print("email:")
    email = input()
    print("username:")
    username = input()
    print("displayName:")
    displayName = input()

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
    return template(email, username, displayName, password, team, language, device_id, device_type, device_model, system_version, app_version)

def LoginToServer():
    """Asks for username and login and returns JSON template with data for http request"""
    print("To start data streaming, please login:")
    print("username:")
    username = input()
    password = getpass.getpass('password:')
    template = JsonTemplate("Login")
    return template(username, password, device_id, device_type, device_model, system_version, app_version)

"""Data Templates"""
def MakeDataFrame(accuracy, altitude, height, id_, latitude, longitude, provider ,timestamp, width):
    """Generate JSON data frame of detector event"""
    frame = {
        "accuracy": accuracy,
        "altitude": altitude,
        # "frame_content": pictureFrameContent,
        "height": height,
        "id": id_,
        "latitude": latitude,
        "longitude": longitude,
        "provider": provider,
        "timestamp": timestamp,
        "width": width
    }
    return frame

def JsonTemplate(whichTemplate):
    """get one of parameter: Register, Login, SendData and return template as a function"""
    def Register(email, username, displayName, password, team, language, device_id, device_type, device_model, system_version, app_version):
        """Return Register JSON template"""
        template_ = {
            "email": email,
            "username": username,
            "display_name": displayName,
            "password": password,
            "team": team,
            "language": language,
            "device_id": device_id,
            "device_type": device_type,
            "device_model": device_model,
            "system_version": system_version,
            "app_version": app_version
        }
        return template_

    def Login(username, password, device_id, device_type, device_model, system_version, app_version):
        """Return Login JSON template"""
        template_ = {
            "username": username,
            "password": password,
            "device_id": device_id,
            "device_type": device_type,
            "device_model": device_model,
            "system_version": system_version,
            "app_version": app_version
        }
        return template_

    def SendData(dataJsonList, device_id, device_type, device_model, system_version, app_version):
        """Return Data JSON template"""
        template_ = {
        "detections": 
                dataJsonList,
            "device_id": device_id,
            "device_type": device_type,
            "device_model": device_model,
            "system_version": system_version,
            "app_version": app_version
        }
        return template_

    if whichTemplate == "Register":
        return Register
    elif whichTemplate == "Login":
        return Login
    elif whichTemplate == "Data":
        return SendData

def HttpRequest(IP, whichRequest):
    """choose IP adress of server and select type of request: Register, Login, SendData."""
    def RegisterRequest(dataJSON):
        """Http Register request to server"""
        _adress = str(IP) + "/api/v2/user/register"
        r = requests.post(_adress, json=dataJSON, verify=False, headers={'Content-Type': 'application/json'})
        return(r.status_code, r.reason, r.content)
    def LoginRequest(dataJSON):
        """Http Login request to server"""
        _adress = str(IP) + "/api/v2/user/login"
        r = requests.post(_adress, json=dataJSON, verify=False, headers={'Content-Type': 'application/json'})
        return(r.status_code, r.reason, r.content)
    def SendDataRequest(dataJSON, token):
        """Http SendData request to server"""
        _adress = str(IP) + "/api/v2/detection"
        header = {'Content-Type': 'application/json', 'Authorization': 'Token {}'.format(token)}
        r = requests.post(_adress, json=dataJSON, verify=False, headers=header)
        return(r.status_code, r.reason, r.content)

    if whichRequest == "Register":
        return RegisterRequest
    elif whichRequest == "Login":
        return LoginRequest
    elif whichRequest == "Data":
        return SendDataRequest

# Initialization of Detector
config = IfConfigExist()
if config == False:
    registrationTemplate = InitiateCosmicWatch()
    registerRequest = HttpRequest("https://api.credo.science", "Register")
    registerResult = registerRequest(registrationTemplate)
    if errors(registerResult[0], registerResult[2]) == False:
        configFile = open(configFileName,'w')
        configFile.write(json.dumps(registrationTemplate))
        configFile.close
        config = IfConfigExist()
    else:
        exit

# Loggin into server
loginTemplate = LoginToServer()
loginRequest = HttpRequest("https://api.credo.science", "Login")
loginResult = loginRequest(loginTemplate)
if errors(loginResult[0], loginResult[2]) == False:
    pass
else:
    exit
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
print(str(port_list[int(ArduinoPort)-1])+'\n')
# fname = input("Enter file name (eg. save_file.txt):")
fname = "data.txt"
# id = input("Enter device ID:")
id = "1"
print("Taking data ...")
print("Press ctl+c to terminate process")

signal.signal(signal.SIGINT, signal_handler)
#ComPort = serial.Serial('/dev/cu.wchusbserialfa130') # open the COM Port
ComPort = serial.Serial(port_list[int(ArduinoPort)-1]) # open the COM Port

ComPort.baudrate = 9600          # set Baud rate
ComPort.bytesize = 8             # Number of data bits = 8
ComPort.parity   = 'N'           # No parity
ComPort.stopbits = 1    

# file = open(fname, "w",0)

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
    dataFrameTemplate = MakeDataFrame(1, 210.73, 0, counter, 50.0922, 19.9148, "ip", int(time.time()*1000), 0)  #DATA FRAME TO SEND
    dataContent = dataTemplate([dataFrameTemplate], device_id, device_type, device_model, system_version, app_version)   #WHOLE DATA TO SEND
    counter +=1
    sendResult = sendRequest(dataContent, AuthenticationToken)

    # print(dataContent)
    if errors(loginResult[0], loginResult[2]) == False:
        pass
    else:
        exit

    print(sendResult)
    
ComPort.close()     
file.close() 
