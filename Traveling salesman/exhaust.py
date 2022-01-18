import pandas as pd
import numpy as np
from itertools import permutations
from operator import itemgetter
import time
import sys

def read(filename):
    """
    Input: filename of csv file.

           Reads data in file and puts it into pandas dataframe.
           Renames rows to match column names.
    Output: returns the dataframe
    """

    data = pd.read_csv(filename, sep=";")

    #Renames rows to cities instead of numbers
    i = 0
    for col in data.columns:
        data.rename(columns = {col : col}, index={i: col}, inplace=True)
        i+=1

    return data

def exhaust(data,n):
    """
    Input: pandas dataframe, n where n is amount of cities to perform an
           exhaustive search on.

           Finds the shortest route between the cities by brute force.
    Output: Prints the shortest route and its distance.
    """

    subset = data.iloc[:n, :n]
    routes = list(permutations(subset))
    short_dist = -1
    short_route = []

    #Brute force
    for route in routes:
        distance = 0
        i = 0
        for city in route:
            i += 1
            if i == len(route):
                #If we're at the last city, adds the distance from here to first.
                distance += subset[city][route[0]]
            else:
                distance += subset[city][route[i]]
        if short_dist == -1 or distance < short_dist:
            short_dist = distance
            short_route = route

    print(short_route)
    print(short_dist)


if __name__ == '__main__':
    #Run with argument 1 as n, where n is amount of cities.
    n = int(sys.argv[1])
    data = read("european_cities.csv")
    print("Number of cities: ", n)
    t0 = time.perf_counter()
    exhaust(data,n)
    t1 = time.perf_counter()
    print('{:.3f} sec'.format(t1-t0))



"""
Number of cities: 6
('Barcelona', 'Belgrade', 'Bucharest', 'Budapest', 'Berlin', 'Brussels')
5018.8099999999995
0.164 sec

Number of cities:  7
('Berlin', 'Copenhagen', 'Brussels', 'Barcelona', 'Belgrade', 'Bucharest', 'Budapest')
5487.889999999999
1.296 sec

Number of cities:  8
('Brussels', 'Dublin', 'Barcelona', 'Belgrade', 'Bucharest', 'Budapest', 'Berlin', 'Copenhagen')
6667.489999999999
11.951 sec

Number of cities:  9
('Berlin', 'Copenhagen', 'Hamburg', 'Brussels', 'Dublin', 'Barcelona', 'Belgrade', 'Bucharest', 'Budapest')
6678.549999999999
142.738 sec

Number of cities:  10
('Copenhagen', 'Hamburg', 'Brussels', 'Dublin', 'Barcelona', 'Belgrade', 'Istanbul', 'Bucharest', 'Budapest', 'Berlin')
7486.309999999999
1759.300 sec
"""
