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


def foo (current_location,rides,old_time,current_time,k,r):
    k += 1
    if k == 4 or int(current_time.strftime("%H"))>21:
            return None, current_time, current_time, r
    min_ride = ''
    min_time = float('inf')
    end_time = ''
    next_r = ''
    for ride_name in rides.keys():
        ride = rides[ride_name]
        est_time = calculate_total_time(current_location,ride,old_time,current_time)
        new_time = current_time + datetime.timedelta(minutes=est_time)
        rides2 = copy.deepcopy(rides)
        del rides2[ride_name]
        next_ride, final_time, new_time, r = foo(ride_name,rides2,current_time,new_time,k,r)
        span = time_pkg.get_time_difference(final_time,current_time)
        if span < min_time:
            min_time = span
            min_ride = ride.name
            end_time = new_time
            next_r = next_ride
    r.append(next_ride)
    return min_ride, final_time, new_time,r

n = 3

all_rides = ride_pkg.load_rides('mkRides.csv')
all_rides = sorted(all_rides.items())
all_rides = dict(all_rides)
walk_times = api_pkg.load_walk('walk_times.csv')
wait_record = data_pkg.load_record('wait_record.csv')
#wait_times = wait_pkg.load_wait('web_wait.csv')
day_type = time_pkg.get_day_type()
month = time_pkg.get_month()
wait_times = wait_pkg.find_wait(all_rides)

current_time = datetime.datetime.now()
rides = copy.deepcopy(all_rides)
current_location = 'The Hall of Presidents'
k = 0
r=[]
choice1, final1, end1, r = foo(current_location,all_rides,current_time,current_time,0,r)
# rides2 = copy.deepcopy(all_rides)
# del rides2[choice1]
# choice2, final2, end2 = foo(choice1,rides2,end1,end1,1)
# rides3 = copy.deepcopy(rides2)
# del rides3[choice2]
# choice3, final3, end3 = foo(choice2,rides3,end2,end2,2)
print('1. '+ choice1)
# print('2. '+ choice2)
# print('3. '+ choice3)
# print(final1,end3)