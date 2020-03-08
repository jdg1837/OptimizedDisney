from collections import defaultdict
import ride_pkg
import data_pkg
import wait_pkg
import time_pkg
import api_pkg
import datetime
import copy

def calculate_total_time(current_location,ride,old_time,current_time):
    ride_name = ride.name
    points = [ride_name,current_location]
    points.sort()
    if points[0] == points[1]:
        walk = 0
    else:
        walk = walk_times[(points[0],points[1])]/60

    wait = wait_times[ride_name]
    if old_time != current_time:
        approx_current_time, approx_current_time_str = time_pkg.approximate_time(current_time)
        current_key = (approx_current_time_str,ride_name,month,day_type)
        frozen_current_key = frozenset(current_key)
        approx_old_time, approx_old_time_str = time_pkg.approximate_time(old_time)
        old_key = (approx_old_time_str,ride_name,month,day_type)
        frozen_old_key = frozenset(old_key)
        try:
            num1 = wait_record[frozen_current_key]
        except:
            num1 = wait_times[ride_name]
        try:
            num2 = wait_record[frozen_old_key]
        except:
            num2 = 0
        ratio_num = num1-num2
        ratio_den = time_pkg.get_time_difference(current_time,old_time)
        ratio = ratio_num/ratio_den
        if ratio != 0:
            wait *= ratio

    duration = ride.duration

    total = walk + wait + duration
    return round(total)


def foo (current_location,rides,old_time,current_time,k):
    k += 1
    if k == 4 or int(current_time.strftime("%H"))>21:
            return None, current_time, current_time
    min_ride = ''
    min_time = float('inf')
    end_time = ''
    for ride_name in rides.keys():
        ride = rides[ride_name]
        est_time = calculate_total_time(current_location,ride,old_time,current_time)
        new_time = current_time + datetime.timedelta(minutes=est_time)
        rides2 = copy.deepcopy(rides)
        del rides2[ride_name]
        next_ride, final_time, new_time = foo(ride_name,rides2,current_time,new_time,k)
        span = time_pkg.get_time_difference(final_time,current_time)

        if span < min_time:
            min_time = span
            min_ride = ride.name
            end_time = new_time

    return min_ride, final_time, new_time

def choose(var):
    n = 3

    global all_rides
    global walk_times 
    global wait_record 
    global wait_times 
    global day_type 
    global month 

    all_rides1 = ride_pkg.load_rides('mkRides.csv')
    all_rides1 = dict(all_rides1)
    all_rides = {}
    for r in range(len(all_rides1)):
        keys = list(all_rides1.keys())
        if var[r] == 1:
            x = keys[r]
            all_rides[x] = all_rides1[x]
    print(all_rides)
    walk_times = api_pkg.load_walk('walk_times.csv')
    wait_record = data_pkg.load_record('wait_record.csv')
    wait_times = wait_pkg.load_wait('web_wait.csv')
    day_type = time_pkg.get_day_type()
    month = time_pkg.get_month()
    #wait_times = wait_pkg.find_wait(all_rides)

    current_time = datetime.datetime.now()
    rides = copy.deepcopy(all_rides)
    current_location = 'The Hall of Presidents'
    k = 0
    choice, final, end = foo(current_location,all_rides,current_time,current_time,k)
    return choice