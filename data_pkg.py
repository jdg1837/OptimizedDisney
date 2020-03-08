import os, csv
import datetime 
import calendar 

def parse_filename(filename):
    slash = filename.find('/')
    values = filename[slash+1:].split()
    month = values[0]
    year = values[1]
    year = year[:4]
    return month, year
    
def parse_header(header):
    ride_info = []
    for i in range (len(header)):
        ride_info.append(header[i])
    return ride_info

def parse_timestamp(timestamp):
    if '/' in timestamp:
        dt_object = datetime.datetime.strptime(timestamp, "%m/%d/%Y %H:%M")
    else:
        dt_object = datetime.datetime.strptime(timestamp[:-3], "%Y-%m-%d %H:%M")
    #dt_object = datetime.datetime.strptime(timestamp, "%m/%d/%Y %H:%M")
    if dt_object.weekday() <= 5:
        day_type = 'weekday'
    else:
        day_type = 'weekend'
    time = dt_object.strftime('%H:%M')
    return day_type, time

def read_data(filename):
    
    record = {}
    daytype_count = {'weekday':0,'weekend':0}
    dates_counted = []

    with open(filename) as csvfile:
        month, year = parse_filename(filename)
        csvreader = csv.reader(csvfile)
        header = next(csvreader)
        ride_info = parse_header(header)
        for row in csvreader:
            datetime_info = row[0].split()
            date = datetime_info[0]
            timestamp = str(datetime_info[0] + ' ' + datetime_info[1])
            #print(timestamp)
            day_type, time = parse_timestamp(timestamp)
            if date not in dates_counted:
                dates_counted.append(date)
                daytype_count[day_type] += 1
            if time[-2:] != '00' and time[-2:] != '30':
                continue
            # if int(time[:2]) < 9 or int(time[:2]) > 21:
            #     continue
            for col in range (2,len(row)):
                ride = ride_info[col]
                cell = row[col]
                if cell == '':
                    continue
                val = int(cell)
                curr_set = [month,day_type,time,ride]
                frozen = frozenset(curr_set)
                if frozen not in record:
                    record[frozen] = val
                else:
                    record[frozen] += val

    for entry in record:
        entry_list = list(entry)
        count = 1
        if 'weekend' in entry_list:
            count = daytype_count['weekend']
        else:
            count = daytype_count['weekday']
        record[entry] /= count

    return record

def record2file(record):
    for entry in record.keys():
        entry_list = list(entry)
        out = "\""
        for i in range(len(entry_list)):
            val = entry_list[i]
            out += val
            if i == len(entry_list) - 1:
                out += "\","
            else:
                out += ","
        out += str(record[entry])
        print(out)

def average_record(record1,record2):
    record_avg = {}
    for entry in record1.keys():
        val1 = record1[entry]
        val2 = record2[entry]
        avg = (val1 + val2)/2
        record_avg[entry] = avg
    return record_avg

def average_finder():
    month_list = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    record = {}

    for i in range(12):
        off = 0
        if i <= 3:
            off = 1

        pre = 'dataset/'
        month = month_list[i]
        year = 2017+off
        post = '.csv'
        file1 = pre+month+' '+str(year)+post
        file2 = pre+month+' '+str(year+1)+post

        if i <= 9:
            record1 = read_data(file1)
            record2 = read_data(file2)
            curr_record = average_record(record1,record2)
        else:
            curr_record = read_data(file2)
        
        if i == 1:
            record = curr_record
        else:
            record.update(curr_record)

    return record

def load_record(filename):
    wait_record = {}
    with open(filename) as csvfile:
        csvreader = csv.reader(csvfile)
        for row in csvreader:
            values = row[0].strip().split(',')
            frozen = frozenset(values)
            wait_record[frozen] = float(row[1])
    return wait_record

# record = average_finder()
# record2file(record)