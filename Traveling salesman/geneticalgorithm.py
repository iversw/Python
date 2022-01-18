import pandas as pd
import numpy as np
from itertools import permutations
from operator import itemgetter
import time
import sys
import random
from hill import init
from hill import dist
import matplotlib.pyplot as plt

def parent_selection(pop, data):
    """
    Input:
          population of individuals
          dataframe of distances between cities
    Selects the half of the population with the best fitness(shortest distance)
    and returns a list of these.

    Output:
          The half of the population with the highest fitness
    """
    fitness = lambda route:dist(route, data)
    pop.sort(key=fitness)
    half = len(pop)//2
    mating_pool = pop[:half]

    return mating_pool

def survivor_selection(pop, n, data):
    """
    Input:
          pop: A population of individuals(routes)
          n where n is max amount of individuals
          data, the dataframe containing distances between cities

    Determines which part of the population survives. The n best solutions are
    kept, while 5 random new permutations are added for some diversity.

    Output:
          list of routes with best fitness if the population is higher than max.
          Else: returns the population
    """
    fitness = lambda route:dist(route, data)
    if len(pop) > n:
        pop.sort(key=fitness)
        survivors = pop[:n-5]

        for i in range(5):
            wild = np.random.permutation(data.columns)
            survivors.append(wild)
        return survivors
    else:
        return pop

def mutation(o):
    """
    Input:
         A route / offpsring o

    Swaps two random cities in the sequence.

    Output:
          The offspring with swapped cities
    """
    swap1 = np.random.randint(len(o))
    swap2 = np.random.randint(len(o))

    o[swap1], o[swap2] = o[swap2], o[swap1]
    return o

def evolve(pop, data, min_pop, max_pop):
    """
    Input:
          pop, a population of individuals
          data, a dataframe of distances between cities
          min_pop, the amount of starting permutations
          max_pop, the max amount of individuals allowed in population

    Performs parent selection, crossover, mutation and survival selection.

    Output:
          The best individual after 100 generations as a route.
    """
    #t0 = time.perf_counter()
    generations = 100
    while generations > 0:
        mating_pool = parent_selection(pop, data)
        for p in range(len(mating_pool) -1):
            #Mates parents in pairs next to each other
            #Shuffle parents at random for more diversity?
            o1,o2 = pmx_pair(mating_pool[p],mating_pool[p+1])

            #5% chance of mutating offspring
            m = np.random.random()
            if m < 0.05:
                o1 = mutation(o1)
                o2 = mutation(o2)
            pop.append(o1)
            pop.append(o2)
            p += 1
        pop = survivor_selection(pop, max_pop, data)
        generations -= 1

    fitness = lambda route:dist(route, data)
    pop.sort(key=fitness)
    t1 = time.perf_counter()
    # print('{:.3f} sec'.format(t1-t0))
    # print(dist(pop[0],data))
    return pop[0]#Returns best route

def pmx(a, b, start, stop):
    """
    Input:
          parent a (route)
          parent b (route)
          start index of slice
          stop index of slice

    Partially mapped crossover

    Output: offspring of the two parents as route.
    """
    child = [None]*len(a)
    child[start:stop] = a[start:stop]
    for ind, x in enumerate(b[start:stop]):
        ind += start
        if x not in child:
            while child[ind] != None:
                ind = np.where(b == a[ind])
                ind = ind[0][0]
            child[ind] = x
    for ind, x in enumerate(child):
        if x == None:
            child[ind] = b[ind]

    return child


def pmx_pair(a, b):
    """
    Input:
          parent a (route)
          parent b (route)
    Pairs the two parents and returns two offspring

    Output:
           two offspring (routes)
    """
    half = len(a) // 2
    start = np.random.randint(0, len(a)-half)
    stop = start+half
    return pmx(a, b, start, stop), pmx(b, a, start, stop)

def multiple_runs(n, min_pop, c):
    """
    Input:
         n where n is a amount of runs
         min_pop, amount of starting permutations
         c, amount of cities to include
    Returns best individuals of n populations in a list
    """
    #results = [np.zeros(n, dtype=object)]
    results = []
    max_pop = min_pop+20

    for i in range(n):
        data, cities, population = init("european_cities.csv", min_pop, c)
        population = population.tolist()
        r = evolve(population, data, min_pop, max_pop)
        results.append(r)

    return np.asarray(results)

if __name__ == '__main__':
    """
    Run with arguments n, min_pop and cities. n is amount of different populations
    to gather results from, min_pop is the starting size of the population and
    cities is the amount of cities.

    The program runs three times, one for the supplied min_pop population size,
    an additional time for min_pop+10 and one last time for min_pop+20

    NB: takes quite a while, I suggest you test with low n and min_pop
    """

    n = int(sys.argv[1])
    min_pop = int(sys.argv[2])
    cities = int(sys.argv[3])

    #Just to have the data
    data, c, routes = init("european_cities.csv", 1, cities)

    r1 = multiple_runs(n, min_pop, cities)
    r2 = multiple_runs(n, min_pop+10, cities)
    r3 = multiple_runs(n, min_pop+20, cities)
    r1_dist = np.zeros(n, dtype=object)
    r2_dist = np.zeros(n, dtype=object)
    r3_dist = np.zeros(n, dtype=object)

    for i in range(len(r1)):
        r1_dist[i] = dist(r1[i], data)

    for i in range(len(r2)):
        r2_dist[i] = dist(r2[i], data)
    for i in range(len(r3)):
        r3_dist[i] = dist(r3[i], data)

    plt.plot(r1_dist, label = min_pop)
    plt.plot(r2_dist, label = min_pop+10)
    plt.plot(r3_dist, label = min_pop+20)
    plt.show()

    #First n amount of runs with min_pop as supplied
    print("== RUN 1: ==")
    print("Best distance: ", np.amin(r1_dist))
    print("Worst distance: ", np.amax(r1_dist))
    print("Average: ", np.mean(r1_dist))
    print("Standard deviation: ", np.std(r1_dist))

    #Second n amount of runs with min_pop +10
    print("\n== RUN 2: ==")
    print("Best distance: ", np.amin(r2_dist))
    print("Worst distance: ", np.amax(r2_dist))
    print("Average: ", np.mean(r2_dist))
    print("Standard deviation: ", np.std(r2_dist))

    #Third n amount of runs with min_pop +20
    print("\n== RUN 3: ==")
    print("Best distance: ", np.amin(r3_dist))
    print("Worst distance: ", np.amax(r3_dist))
    print("Average: ", np.mean(r3_dist))
    print("Standard deviation: ", np.std(r3_dist))
