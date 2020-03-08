import requests, os, bs4
import ride_pkg
import api
import csv
import json

#location = 'Disneyworld, Florida'
def find_distance(all_rides, location):
    distances = {}
    ride_names = list(all_rides.keys())
    ride_number = len(all_rides)
    for i in range(ride_number-1):
        for j in range(i+1,ride_number):
            ride1 = ride_names[i]
            ride2 = ride_names[j]
            d = api.matrix_api_call(ride1,ride2,location)
            distances[(ride1,ride2)] = d
    return distances

def data2file(filename, distance):
    for d in distance:
        print(d[0] + "," + d[1] + "," + str(distance[d]))

def load_walk(filename):
    walk_times = {}
    with open(filename) as csvfile:
        csvreader = csv.reader(csvfile)
        for row in csvreader:
            ride1 = row[0].strip()
            ride2 = row[1].strip()
            walk_times[(ride1,ride2)] = int(row[2])
    return walk_times