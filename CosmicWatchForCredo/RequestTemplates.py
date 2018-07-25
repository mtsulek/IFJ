"""Request"""
import requests

def HttpRequest(IP, whichRequest):
    """choose IP adress of server and select type of request: Register, Login, SendData."""
    def RegisterRequest(dataJSON):
        """Http Register request to server"""
        _adress = str(IP) + "/api/v2/user/register"
        r = requests.post(_adress, json=dataJSON, verify=False, headers={'Content-Type': 'application/json'}, timeout=1)
        return(r.status_code, r.reason, r.content)
        
    def LoginRequest(dataJSON):
        """Http Login request to server"""
        _adress = str(IP) + "/api/v2/user/login"
        r = requests.post(_adress, json=dataJSON, verify=False, headers={'Content-Type': 'application/json'}, timeout=1)
        return(r.status_code, r.reason, r.content)

    def SendDataRequest(dataJSON, token):
        """Http SendData request to server"""
        _adress = str(IP) + "/api/v2/detection"
        header = {'Content-Type': 'application/json', 'Authorization': 'Token {}'.format(token)}
        r = requests.post(_adress, json=dataJSON, verify=False, headers=header, timeout=1)
        return(r.status_code, r.reason, r.content)

    def Ping(dataJSON, token):
        """Http Ping request to server"""
        _adress = str(IP) + "/api/v2/ping"
        header = {'Content-Type': 'application/json', 'Authorization': 'Token {}'.format(token)}
        r = requests.post(_adress, json=dataJSON, verify=False, headers=header, timeout=1)
        return(r.status_code, r.reason, r.content)

    if whichRequest == "Register":
        return RegisterRequest
    elif whichRequest == "Login":
        return LoginRequest
    elif whichRequest == "Data":
        return SendDataRequest
    elif whichRequest == "Ping":
        return Ping