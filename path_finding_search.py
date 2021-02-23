#!/usr/bin/python
import os
import sys
import re
import numpy as np
import graph
import matplotlib.pyplot as plt

def A_s(g, start_goal, goal_location, dimensions):
    pass

def iterative_deepening(g, start_goal, goal_location, dimensions):
    pass

def bfs(g, start_goal, goal_location, dimensions):
    q = []
    visited = np.zeros(dimensions, dtype=bool)

    q.append(start_goal)
    visited[start_goal] = True

    while q:
        s = q.pop(0)
        print(s)
        for i in range(len(g.edges[s[0]])):
            if visited[s[0], i] == False:
                print(q)
                q.append((s[0], i))
                visited[s[0], i] = True

def get_data(path):
    # using this to remove next line escape char and convert to int
    clean = lambda x: [int(i.strip('\n')) for i in x]

    f = open(path, 'r')
    dimensions = clean(f.readline().split(' '))
    start_location = clean(f.readline().split(' '))
    goal_location = clean(f.readline().split(' '))
    g = graph.Graph(dimensions)
    map = []

    for r in range(dimensions[0]):
        map.append(clean(f.readline().split(' ')))

    for r in range(dimensions[0]):
        for 

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
    # g.bfs(g, start_location, goal_location, dimensions)
    plt.show()
