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

    # This first creates an array with all the weight values, i.e. the weight to get from 0,0 to 0,1 is map[0,1]
    for r in range(dimensions[0]):
        map.append(clean(f.readline().split(' ')))

    # This populates the graph, for every coordinate r,c it will try to create the edges [r+1,c] [r-1,c] [r, c-1], [r, c+1]
    for r in range(dimensions[0]):
        for c in range(dimensions[1]):
            for change in [1, -1]:
                if check_bounds((r + change, c)):
                    g.insert_edge(r, c, r + change, c, map[r + change][c])
                if check_bounds((r, c + change)):
                    g.insert_edge(r, c, r, c + change, map[r][c + change])
    f.close()
    return g, start_location, goal_location

def process_args(argv):
    argv = argv[1:]

    if '-p' not in argv:
        print('Path was not provided, use -p to provide path')
        sys.exit(1)

    if '-A*':
        algorithm = 'a*'
    elif '-IDS':
        algorithm = 'iter'
    elif '-BFS':
        algorithm = 'bfs'
    else:
        print("Algorithm wasn't provided")
        sys.exit(1)

    return algorithm, argv[argv.index('-p') + 1]

def A_s(g, start_goal, goal_location):
    pass

def iterative_deepening(g, start_goal, goal_location):
    pass

def bfs(g, start_goal):
    visited = np.zeros(g.dimensions, dtype=bool)
    nodes_expanded = 0
    prev = np.zeros((g.dimensions[0], g.dimensions[1], 2), dtype=int) - 1 # this will allow to trace back the path
    q = []
    q.append(start_goal)
    visited[start_goal[0], start_goal[1]] = True

    while q:
        u = q.pop(0)
        nodes_expanded += 1
        for edge in g.edges[str(u[0]) + ', ' + str(u[1])]:
            if not visited[edge[0][0], edge[0][1]]:
                visited[edge[0][0], edge[0][1]] = True
                prev[edge[0][0], edge[0][1]] = u
                q.append(edge[0])
    return prev, nodes_expanded

def print_path(path):
    for i in path:
        for j in i:
            print(j, end=' ')
        print()

if __name__ == "__main__":
    algorithm, file_path = process_args(sys.argv)
    g, start_location, goal_location = get_data(file_path)
    path, nodes_expanded = bfs(g, start_location)
    print_path(path)

    # draw graph
    g.draw_graph()
    plt.show()
