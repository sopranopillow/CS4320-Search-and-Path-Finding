#! /usr/bin/python
import os
import sys
import re
import numpy as np
import graph
import matplotlib.pyplot as plt

def get_data(path):
    # using this to remove next line escape char and convert to int
    clean = lambda x: [int(i.strip('\n')) for i in x]

    f = open(path, 'r')
    dimensions = clean(f.readline().split(' '))
    start_location = clean(f.readline().split(' '))
    goal_location = clean(f.readline().split(' '))
    g = graph.Graph(dimensions)
    map = []

    # coordinate[0] and dimensions[0] ==> rows
    # coordinate[1] and dimensions[1] ==> columns
    check_bounds = lambda coordinate: (coordinate[0] < dimensions[0] and coordinate[0] >= 0) and \
            (coordinate[1] < dimensions[1] and coordinate[1] >= 0)

    for r in range(dimensions[0]):
        map.append(clean(f.readline().split(' ')))

    for r in range(dimensions[0]):
        for c in range(dimensions[1]):
            for change in [1, -1]:
                if check_bounds((r + change, c)):
                    g.insert_edge(r, c, r + change, c, map[r + change][c])
                if check_bounds((r, c + change)):
                    g.insert_edge(r, c, r, c + change, map[r][c + change])


    f.close()
    g.draw_graph()
    return g, start_location, goal_location, dimensions

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
    g, start_location, goal_location, dimensions = get_data(path)
    g.bfs(g, start_location, goal_location, dimensions)
    plt.show()
