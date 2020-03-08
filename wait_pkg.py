import requests, bs4, csv
import ride_pkg

def find_wait(all_rides):
    wait_times = {}
    url = 'https://queue-times.com/en-US/parks/6/queue_times'

    response = requests.get(url)
    response.raise_for_status()

    soup = bs4.BeautifulSoup(response.text, 'html.parser')

    ride_blocks = soup.select('.panel-block')

    for block in ride_blocks:
        name = block.select('.has-text-weight-normal')[0]
        name = name.text.split('(')[0]
        name = name.strip()
        wait = block.select('.has-text-weight-bold')[0].text
        wait = wait.strip()
        if name in all_rides.keys():
            if wait == 'Closed':
                wait = -1
            elif wait == 'Open':
                wait = 0
            else:
                wait = int(wait.split()[0])
            wait_times[name] = wait

    return wait_times

def data2file(filename, wait_times):
    for w in wait_times:
        print("\"" + w + "\"" + "," + str(wait_times[w]))

def load_wait(filename):
    wait_times = {}
    with open(filename) as csvfile:
        csvreader = csv.reader(csvfile)
        for row in csvreader:
            ride = row[0].strip()
            wait = int(row[1].strip())
            wait_times[ride] = wait
    return wait_times

# all_rides = ride_pkg.load_rides('mkRides.csv')
# wait_times = find_wait(all_rides)
# data2file('web_wait.csv', wait_times)