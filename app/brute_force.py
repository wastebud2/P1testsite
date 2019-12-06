import math
import random
import sys
import json

sys.setrecursionlimit(100000)

#def generateLocations(dots, dotRange):
#    for i in range(0,dots):
#        randomCoordinat = [i,random.randrange(0,dotRange),random.randrange(0,dotRange)]
#        dotLocation.append(randomCoordinat)

def getDistance(start,end):
    distance = math.sqrt((start[1]-end[1])**2 + (start[2]-end[2])**2)
    return distance

def totalDistance(array):
    totalDist = 0
    for i in range(0,len(array)-1):
        dist = getDistance(array[i],array[i+1])
        totalDist += dist
    return totalDist

def swap(a,i,j):
    holder = a[i]
    a[i] = a[j]
    a[j] = holder
    return a

def sortLocations(array):
    bestDistance = 0
    bestOrder = []

    for i in range(0, len(array)):
        array[i].append(i)

    #comparisons:
    while True:
        largestI = -1
        for i in range(0,len(array)-1):
            if array[i][0] < array[i + 1][0]:
                largestI = i

        if largestI == -1:
            break

        for j in range(0,len(array)):
            if array[largestI][0] < array[j][0]:
                largestJ = j

        #alterations to list
        swap(array,largestI,largestJ)
        end = array[largestI+1:len(array)]
        del array[largestI+1:]
        for i in end[::-1]:
            array.append(i)

        #calculate and compare distances
        currentDistance = totalDistance(array)
        if currentDistance < bestDistance or bestDistance == 0:
            bestDistance = currentDistance
            bestOrder = []
            for i in array:
                bestOrder.append(i[3]) # needs to refer to an index, and not the PK of the entry
            print(bestDistance)
            print(bestOrder)
        #loopArray = array
        #sortLocations(loopArray,bestDistance)
    #for i in range(0,len(bestLocation)):
    #    bestLocation[i].append(i)
    #print(bestLocation)
    return bestOrder

## Main ##
#dotLocation = []
#dots = 3
#dot_range = 10
#generateLocations(dots,dot_range)

#sortLocations(dotLocation)