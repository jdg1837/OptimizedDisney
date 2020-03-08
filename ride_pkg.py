import csv

class Ride:
    ride_open = False
    
    def __init__(self, name, main_type, tags, fast_pass, duration):
        self.name = name
        self.main_type = main_type
        self.tags = tags
        self.fast_pass = fast_pass
        self.duration = duration

    def is_open():
        return ride_open

def load_rides(filename):
    all_rides = {}
    with open(filename) as csvfile:
        csvreader = csv.reader(csvfile)
        next(csvreader)
        for row in csvreader:
            name = row[0].strip()
            main_type = row[1]
            tags = row[2].replace("\"","").split(",")
            fast_pass = int(row[3]) == 1
            duration_info = row[4].split(":")
            duration = float(duration_info[0]) + float(duration_info[1])/60
            ride = Ride(name, main_type, tags, fast_pass, duration)
            all_rides[name] = ride
    return all_rides