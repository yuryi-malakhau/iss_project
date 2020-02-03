import requests


# This function checks json file returned from the ISS API website
def check_json(data):
    if data['message'] == "success":
        return True
    else:
        print('Wrong (latitude, longitude) or the website is down')
        return False


def get_iss_people():
    host = 'http://api.open-notify.org/astros.json'
    response = requests.get(host)
    # Status_code == 200 if normal response; 400 if failed
    if response.status_code == 200:
        data = response.json()
        status = check_json(data)
        if status:
            return status, data
        else:
            return status, []
    else:
        status = False
        print('Wrong (latitude, longitude) or the website is down')
        return status, []


def get_iss_pass(lat, lon):
    host = 'http://api.open-notify.org/iss-pass.json?lat={lat:f}&lon={lon:f}'.format(lat=lat, lon=lon)
    response = requests.get(host)
    # Status_code == 200 if normal response; 400 if failed
    if response.status_code == 200:
        data = response.json()
        if check_json(data):
            status = True
            return status, data
        else:
            status = False
            return status, []
    else:
        print('Wrong longitude, latitude or the website is down')
        status = False
        return status, []


# This function gets ISS location as latitude and longitude
def get_iss_location():
    host = 'http://api.open-notify.org/iss-now.json'
    response = requests.get(host)
    if response.status_code == 200:
        data = response.json()
        if check_json(data):
            status = True
            return status, data
        else:
            status = False
            return status, []
    else:
        print('The website is not responding. Try again')
        status = False
        return status, []
