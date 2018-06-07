import json
import requests
import getpass
import os
import platform

# APPLICATION SETUP
configFileName = '.CosmicConfig.json'
app_version = 0.01
distro, version, kernel = platform.linux_distribution()
system_version = platform.system() + platform.release() + " " + distro + version
device_model = "Xiaomi Air 13"
device_type = "PC_CosmicWatch"
device_id = "CosmicWatchTest000000000000001"

print(system_version)
def errors(statusCode, content):
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
        """Return SendData JSON template"""
        template = {
        "detections": [
                dataJsonList
            ],
            "device_id": device_id,
            "device_type": device_type,
            "device_model": device_model,
            "system_version": system_version,
            "app_version": app_version
        }

    if whichTemplate == "Register":
        return Register
    elif whichTemplate == "Login":
        return Login
    elif whichTemplate == "Login":
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
    def SendDataRequest(dataJSON):
        """Http SendData request to server"""
        _adress = str(IP) + "/api/v2/detection"
        r = requests.post(_adress, dataJSON)
        return(r.status_code, r.reason)

    if whichRequest == "Register":
        return RegisterRequest
    elif whichRequest == "Login":
        return LoginRequest
    elif whichRequest == "SendData":
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