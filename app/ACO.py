import csv
import math
import random

import sys

#Get a list of locations from csv file:
#locations_list = open(r'C:\Users\aggen\Desktop\AAU\P1\routing\ACO\locations.csv', 'r')
#locations = [[int(j) for j in i] for i in csv.reader(locations_list,delimiter=',')]

"""LIST OF ACTIONS IN ALGORITHEM:"""
#Randomly place ants at the locations.

#For each ant:
    #1. Choose a not yet visited city, until a tour is complete
    #2. Optimize the tour
    #3. Update pheromone (pheromon on path xy += 1/lenght(tour))

#Evaporate pheromone. (peromone(xy) = (1-p)*peromone(xy))


def accumu(lis): #Function for calculating the accumulative som for a list:
    total = 0
    for k in lis:
        total += k
        yield total

"""ALGORITHEM"""
def sort_ACO(locs):
    """PREPARE LIST"""
    for a,loc in enumerate(locs):
        loc.insert(0,a)

    """SETUP/INITIALIZATION:"""
    # intialization part
    runs = 10
    iterations = 100
    n_ants = 10
    n_citys = len(locs)

    # Values controlling the algorithem
    m = n_ants
    n = n_citys
    e = 0.2        #evaporation rate
    alpha = 1       #pheromone factor
    beta = 2.5        #visibility factor

    x,y = 2,3 #position of x and y coordinates in location sublists
    lowest_cost = 0
    shortest_route_global = []
    
    sorted_route = []   #What the function will return

    for k in range(runs):
        #calculating a distance matix for all possible routs:
        dist_matrix = [[math.sqrt(math.pow(k[x] - h[x],2) + math.pow(k[y] - h[y],2)) for h in locs] for k in locs]

        #creating the visibility of the next city visibility(i,j)=1/d(i,j)
        visibility = [[1/h if h != 0 else h for h in k] for k in dist_matrix]

        #creating the initial pheromone matrix, peromone(m,n):
        pheromone = [[.1 for h in k] for k in dist_matrix]

        #intializing the rute of the ants with size rute(n_ants,n_citys+1) 
        #note adding 1 because we want to come back to the source city
        route = [[0 for h in range(n+1)] for k in range(m)]

        for ite in range(iterations):
            #Setting starting/ending positon of every ant to 1:
            for k in route:
                k[0],k[-1] = 1,1

            for i in range(m):
                #temporary copy of visibility for each ant:
                visibility = [[1/h if h != 0 else h for h in k] for k in dist_matrix]
                temporary_visibility = visibility

                #Establishing starting point
                current_route = [1]

                for j in range(n-1):
                    #intializing combine_feature and cumulative probability arrays to 0:
                    combine_feature = [0 for k in range(n)]
                    cumulative_prob = [0 for k in range(n)]

                    #Setting the visibility in the current city to 0
                    for k in range(n):
                        temporary_visibility[k][current_route[-1]-1] = 0

                    #Calculate pheramone and distance influence for each city:
                    #print(current_route[-1])
                    p_feature = [math.pow(k,beta) for k in pheromone[current_route[-1]-1]]
                    v_feature = [math.pow(k,alpha) for k in temporary_visibility[current_route[-1]-1]]
                    #print(v_feature)
                    combine_feature = [p_feature[k] * v_feature[k] for k in range(n)] #ombined score for each city
                    #print(combine_feature)
                    total = sum(combine_feature) #Sum of attractiveness of all cities   

                    #for a,k in enumerate(combine_feature)
                    probs = [k/total if total != 0 else 0 for a,k in enumerate(combine_feature)] #using the total to calculate the probability for each city
                    #print(probs)
                    cumulative_prob = list(accumu(probs)) #Accumulated probability
                    #print(cumulative_prob)
                    r = random.random()
                    city = [cumulative_prob.index(k) for k in cumulative_prob if k > r and cumulative_prob.index(k)+1 not in current_route][0]+1

                    current_route.append(city)
                    route[i][j+1] = city
            
            route_costs = []
            
            for k in range(m):
                dist_sum = 0
                for h in range(n-1):
                    dist_sum += dist_matrix[route[k][h]-1][route[k][h+1]-1]
                route_costs.append(dist_sum)
            
            shortest_route_index = route_costs.index(sorted(route_costs)[0])
            shortest_route = route[shortest_route_index]
            #print(pheromone)
            pheromone = [[(1-e)*h for h in k] for k in pheromone]
            #print(pheromone)
            for k in range(m):
                dt = 1/route_costs[k]
                for h in range(n-1):
                    pheromone[route[k][h]-1][route[k][h+1]-1] = pheromone[route[k][h]-1][route[k][h+1]-1] + dt
            
        print(shortest_route)

        if route_costs[0] < lowest_cost or lowest_cost == 0:
            lowest_cost = route_costs[0]
            shortest_route_global = shortest_route
    
    for num in shortest_route_global:     #Sorting the original list for shortest route
        for loc in locs:
            if len(loc) == 4 and num == loc[0]:
                sorted_route.append(loc)
                sorted_route.append(sorted_route[0])
                loc.pop(0)
    
    return  sorted_route, lowest_cost