import math
import csv
locations_list = open(r'C:\Users\Agge\Desktop\P1\Routing\ACO\locations.csv', 'r')
locations = [[int(j) for j in i] for i in csv.reader(locations_list,delimiter=',')]

index,x,y = 0,1,2
route = [0]
total_dist = 0

while len(route) < len(locations):
    current_location = route[-1]
    smallest_dist = 0
    for i in locations:
        if i[0] not in route:
            distance = math.sqrt(math.pow(locations[current_location][x] - i[x],2) + math.pow(locations[current_location][y] - i[y],2))
            if distance < smallest_dist or smallest_dist == 0:
                smallest_dist = distance
                smallest_dist_index = i[0]
    total_dist += smallest_dist
    route.append(smallest_dist_index)

total_dist += math.sqrt(math.pow(locations[0][x] - locations[route[-1]][x],2) + math.pow(locations[1][y] - locations[route[-1]][y],2))
route.append(0)

print(route)
print(total_dist)