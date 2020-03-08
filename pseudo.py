ride_list = [ride.isWanted(wanted_tags) in all_rides]
location = entrance

soup = update_soup()
options = []
for ride in ride_list:
    name = ride.name
    wait = soup.get(name)
    distance = a_star(location,ride)
    time = time2ride(distance)
    options.add((name,time))

options.sort()

best = options.get_best(n)
ride_list.pop(best)