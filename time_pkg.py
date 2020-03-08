import time
import datetime

def get_time():
    t = time.localtime()
    current_time = time.strftime("%H:%M", t)

def get_month():
    month_list = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    current_month = datetime.datetime.now().month
    return month_list[current_month-1]

def get_day_type():
    today = datetime.datetime.today()
    day = today.weekday()
    if day <= 5:
        return 'weekday'
    else:
        return 'weekend'

def get_time_difference(t1,t2):
    t3 = t1-t2
    minutes = t3.total_seconds()/60
    return minutes

def approximate_time(current_time):
    hours = int(current_time.strftime("%H"))
    minutes = int(current_time.strftime("%M"))
    if minutes <= 15:
        minutes = '00'
    elif minutes >= 45:
        minutes = '00'
        hours += 1
    else:
        minutes = '30'
    timestamp = str(hours) + ':' + str(minutes)
    round_time = datetime.datetime.strptime(timestamp, "%H:%M")
    round_time_str=round_time.strftime('%H:%M')
    return round_time, round_time_str