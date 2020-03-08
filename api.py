import requests
import json

def matrix_api_call(origin,destination,location):
    origin = origin + ',' + location
    destination = destination + ',' + location
    mode = 'walking'
    with open('key.txt') as f:
        key = f.readline()

    url = 'https://maps.googleapis.com/maps/api/distancematrix/json?' + 'origins=' + origin + '&destinations=' + destination + '&mode=' + mode + '&key=' + key

    response = requests.get(url).json()
    time = response['rows'][0]['elements'][0]['duration']['value']
    return time