"""Data Templates"""
def MakeDataFrame(accuracy, altitude, latitude, longitude, provider ,timestamp ,pulse ,temperature, humidity, pressure):
    """Generate JSON data frame of detector event"""
    frame = {
        "accuracy": accuracy,
        "altitude": altitude,
        "latitude": latitude,
        "longitude": longitude,
        "provider": provider,
        "timestamp": timestamp,
        "pulse_height": pulse,
        "temperature": temperature,
        "humidity": humidity,
        "pressure": pressure
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
