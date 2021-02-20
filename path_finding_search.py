#!/usr/bin/python
import os
import sys
import re
import numpy as np

class Graph:
    def __init__(self, dimensions):  # assuming all are weighted and directed
        self.edges = np.zeros(dimensions, dtype=int)

    def insert_edge(self, s, d, w):
        self.edges[s, d] = w

    def A_s(g, start_goal, goal_location, dimensions):
        pass

    def iterative_deepening(g, start_goal, goal_location, dimensions):
        pass

    def bfs(map, start_goal, goal_location, dimensions):
        q = []
        visited = [False for i in range(dimensions[0] * dimensions[1])]
        q.append(start_goal)

def get_data(path):
    # using this to remove next line escape char and convert to int
    clean = lambda x: [int(i.strip('\n')) for i in x]

    f = open(path, 'r')
    dimensions = clean(f.readline().split(' '))
    start_location = clean(f.readline().split(' '))
    goal_location = clean(f.readline().split(' '))
    g = Graph(dimensions)

    for r in range(dimensions[0]):
        v = clean(f.readline().split(' '))
        for c in range(dimensions[1]):
            g.insert_edge(r, c, v[c])

    f.close()
    return dimensions, start_location, goal_location, g

def process_args(argv):
    argv = argv[1:]

    if '-p' not in argv:
        print('Path was not provided, use -p to provide path')
        sys.exit(1)

    if '-A':
        algorithm = 'a*'
    elif '-I':
        algorithm = 'iter'
    elif '-B':
        algorithm = 'bfs'
    else:
        print("Algorithm wasn't provided")
        sys.exit(1)

    path = argv[argv.index('-p') + 1]
    return algorithm, path

if __name__ == "__main__":
    algorithm, path = process_args(sys.argv)
    dimensions, start_location, goal_location, g = get_data(path)
