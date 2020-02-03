import datetime
import requests
from pathlib import Path
import iss_api_wrapper as iss


def iss_on_map_string():
    status, data = iss.get_iss_location()
    if status:
        lat = float(data['iss_position']['latitude'])
        lon = float(data['iss_position']['longitude'])

        file_path = Path('../etc/world_map.txt')
        message_list = []
        try:
            with open(file_path) as inputfile:
                for line in inputfile:
                    message_list.append(line.split('|'))
        except:
            'Could not find the map file'

        height = len(message_list)
        # Taking into account '\n' symbol, subtract 1
        width = len(message_list[0])-1


        x_res = 360/width
        y_res = 180/height
        # i = height/2 - i'
        # j = width/2 + j'
        idx_i = int(height/2) - int(lat/y_res)
        idx_j = int(width/2) + int(lon/x_res)
        message_list[idx_i][idx_j] = '0'
        message = ''
        for line in message_list:
            temp_str = ''.join(line)
            message = message + temp_str
        return status, message
    else:
        return status, ''


def iss_location_string():
    status, data = iss.get_iss_location()
    if status:
        # Time formatting
        now = datetime.datetime.now()
        time = now.strftime("%H:%M:%S %b %d %Y")

        lat = data['iss_position']['latitude']
        lon = data['iss_position']['longitude']
        location = '(' + lat + ',' + lon + ')'

        message = "The ISS current location at {} is {}\n".format(time, location)
        return status, message
    else:
        return status, ''


# This function returns a string with ISS information
# 'The ISS will be overhead {lat, lon}{city} at {time} for {seconds} seconds'
def iss_overhead_string():
    my_location_status, my_location = get_my_location()
    if my_location_status:
        coordinates, city = my_location
        lat, lon = coordinates
        iss_status, iss_data = iss.get_iss_pass(lat, lon)
        if iss_status:
            # Get a time stamp and convert to local time
            utc_time_stamp = iss_data['response'][0]['risetime']
            time = datetime.datetime.fromtimestamp(utc_time_stamp)
            time = time.strftime("%H:%M:%S %b %d %Y")

            duration = iss_data['response'][0]['duration']

            message = 'The ISS will be overhead {}{} at {} for {} seconds\n'.format(
                coordinates, city, time, duration)
            return iss_status, message
        else:
            return iss_status, ''
    else:
        return my_location_status, ''


def iss_people_string():
    status, data = iss.get_iss_people()
    if status:
        people = [item['name'] for item in data['people']]
        message = '\n'.join(people)
        message = 'This is a team of people at the ISS:\n' + message + '\n'
        return status, message
    else:
        return status, ''


# This function gets my geographical location based on IP
# Output: (latitude, longitude) in degrees
#           city a string of the location
def get_my_location():
    host = 'http://ipinfo.io'
    response = requests.get(host)
    if response.status_code == 200:
        data = response.json()
        city = '(' + ','.join((data['city'], data['region'], data['country'])) + ')'
        location = data['loc']
        lat, lon = location.split(',')
        lat = float(lat)
        lon = float(lon)
        status = True
        return status, [(lat, lon), city]
    else:
        print('Could not access your location or website is down')
        status = False
        return status, []


# This function checks the internet connection
# DNS is not used deliberately
# google.com IP 216.58.192.142 is hardcoded and may change in the future!
def is_internet_on():
    google_ip = 'http://216.58.192.142'
    response = requests.get(google_ip)
    if response.status_code == 200:
        return True
    else:
        print('The Internet is down. This software does not work without Internet')
        return False
