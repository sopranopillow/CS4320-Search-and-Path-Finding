#! /usr/bin/python
import sys, os
import numpy as np
import graph
import matplotlib.pyplot as plt
import random
import time

# dimensions must be a tuple (r,c)
def generate_test_data(dimensions):
    # goal location is on the right half and start location on the left half to avoid getting the same coordinate.
    start_location = (random.randint(0, dimensions[0]-1), random.randint(0, dimensions[1]//2))
    goal_location = (random.randint(0, dimensions[0]-1), random.randint( dimensions[1]//2, dimensions[1]-1))

    # generating random map
    map = [[random.randint(0,5) for j in range(dimensions[1])] for i in range(dimensions[0])]

    # making sure goal_location and start_location are not 0
    if map[start_location[0], start_location[1]] == 0:
        map[start_location[0], start_location[1]] = random.randint(1, 5)
    if map[goal_location[0], goal_location[1]] == 0:
        map[goal_location[0], goal_location[1]] = random.randint(1, 5)

    return populate_graph(map, dimensions), start_location, goal_location

def get_data(path):
    # using this to remove next line escape char and convert to int
    clean = lambda x: [int(i.strip('\n')) for i in x]

    f = open(path, 'r')
    dimensions = clean(f.readline().split(' '))
    start_location = clean(f.readline().split(' '))
    goal_location = clean(f.readline().split(' '))
    map = []

    # This first creates an array with all the weight values, i.e. the weight to get from 0,0 to 0,1 is map[0,1]
    for r in range(dimensions[0]):
        map.append(clean(f.readline().split(' ')))
    f.close()

    return populate_graph(map, dimensions), start_location, goal_location

def populate_graph(map, dimensions):
    # coordinate[0] and dimensions[0] ==> rows
    # coordinate[1] and dimensions[1] ==> columns
    check_bounds = lambda coordinate: (coordinate[0] < dimensions[0] and coordinate[0] >= 0) and \
            (coordinate[1] < dimensions[1] and coordinate[1] >= 0)

    g = graph.Graph(dimensions)

    # This populates the graph, for every coordinate r,c it will try to create the edges [r+1,c] [r-1,c] [r, c-1], [r, c+1]
    for r in range(dimensions[0]):
        for c in range(dimensions[1]):
            for change in [1, -1]:
                if check_bounds((r + change, c)):
                    g.insert_edge(r, c, r + change, c, map[r + change][c])
                if check_bounds((r, c + change)):
                    g.insert_edge(r, c, r, c + change, map[r][c + change])
    return g

def process_args(argv):
    argv = argv[1:]
    files = []

    if '-f' not in argv and '-d' not in argv:
        print('File/folder was not provided, use -f to provide file or -d to provide a directory')
        sys.exit(1)

    if '-f' in argv:
        files.append(argv[argv.index('-f') + 1])
    else:
        directory = argv[argv.index('-d') + 1]
        files += [directory + ('' if directory[-1] == '/' else '/') + file for file in os.listdir(directory)]

    if '-A*':
        algorithm = 'a*'
    elif '-IDS':
        algorithm = 'iter'
    elif '-BFS':
        algorithm = 'bfs'
    else:
        print("Algorithm wasn't provided")
        sys.exit(1)

    return algorithm, files

def A_s(g, start_goal, goal_location):
    pass

def iterative_deepening(g, start_goal, goal_location):
    pass

def bfs(g, start_goal):
    start_time = time.time()
    visited = np.zeros(g.dimensions, dtype=bool)
    nodes_expanded = 0
    prev = np.zeros((g.dimensions[0], g.dimensions[1], 2), dtype=int) - 1 # this will allow to trace back the path
    q = []
    q.append(start_goal)
    visited[start_goal[0], start_goal[1]] = True

    while q:
        if time.time() - start_time >= 180:
            print("BFS took will take more than 3 minutes, returned values are computed results.")
            return prev, nodes_expanded
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
    algorithm, files = process_args(sys.argv)
    for file in files:
        g, start_location, goal_location = get_data(file)
        path, nodes_expanded = bfs(g, start_location)
        print_path(path)
        g.draw_graph()
    plt.show()
