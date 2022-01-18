import pandas as pd
import numpy as np
from itertools import permutations
from operator import itemgetter
import time
import sys
import random

def init(filename, n, cities):
    """
    Input:
         Filename of csv file to read.
         n, where n is the amount of different permutations to climb from.
         cities is the amount of different cities

    Modified version of read method in exhaust. This one allows for more
    permutations to be returned.

    Output:
          Returns dataframe, list of city names, routes(permutations of cities)
    """
    data = pd.read_csv(filename, sep=";")
    data = data.iloc[:cities, :cities]
    cities = []
    routes = np.zeros(n, dtype=object)

    for col in data.columns:
        cities.append(col)

    #Renames cities to numbers. Array cities[n] identifies the city
    i = 0
    for col in data.columns:
        data.rename(columns = {col : i}, inplace=True)
        i+=1

    #Creates n random permutations of the cities as starting points
    i = 0
    for i in range(n):
        routes[i] = np.random.permutation(data.columns)
        i += 1

    return data, cities, routes

def f(route, data):
    """
    Input:
          A route(list of numbers indicating which cities are visited in
          which order)
          Data, a dataframe in which distances between cities is kept

          Swaps two random cities in the route and compares distances between
          the new and old route.
    Output:
         Returns the new route if it is shorter than the previous, otherwise
         returns the previous route

    """
    prev = np.copy(route)
    old = dist(route, data)

    swap1 = np.random.randint(len(route))
    swap2 = np.random.randint(len(route))

    route[swap1], route[swap2] = route[swap2], route[swap1]
    new = dist(route, data)

    if new < old:
        return route
    else:
        return prev

def climb(route, data):

    i = 0
    while i < 1000:
        route = f(route, data)
        i+=1
    return route

def dist(route, data):
    """
    Input:
        route (array with sequence of numbers indicating which cities are visited
        in order)
    Calculates distance from the given route given the supplied data.

    Output: the total distance of the given route.
    """
    distance = 0
    i = 0
    for city in route:
        i += 1
        if i == len(route):
            #If we're at the last city, adds the distance from here to first.
            distance += data[city][route[0]]
        else:
            distance += data[city][route[i]]

    return distance

if __name__ == "__main__":
    """
    Run with arguments n and k where n is the amount of runs, k is amount of
    cities
    """
    n = int(sys.argv[1])
    k = int(sys.argv[2])
    data, cities, routes = init("european_cities.csv", n, k)
    t0 = time.perf_counter()

    #Performs a climb n amount of times
    i = 0
    results = np.zeros(n, dtype=object)
    for route in range(n):
        r = climb(routes[i], data)
        results[i] = r
        i += 1

    #Calculates distances of results
    i=0
    distances = np.zeros(n,dtype = np.float32)
    for route in results:
        r = dist(route,data)
        distances[i] = r
        i += 1
    t1 = time.perf_counter()
    print('{:.3f} sec'.format(t1-t0))
    print("Runs: ", n)
    print("Cities: ", k)
    print("Best: ", np.amin(distances))
    print("Worst: ", np.amax(distances))
    print("Average: ", np.mean(distances))
    print("Standard deviation: ", np.std(distances))

"""
Runs:  20
Cities:  24
Best:  13492.97
Worst:  16941.48
Average:  14781.401

Runs:  20
Cities:  10
Best:  7486.31
Worst:  8391.05
Average:  7700.3447
"""
