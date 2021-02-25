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
    if map[start_location[0]][start_location[1]] == 0:
        map[start_location[0]][start_location[1]] = random.randint(1, 5)
    if map[goal_location[0]][goal_location[1]] == 0:
        map[goal_location[0]][goal_location[1]] = random.randint(1, 5)

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
                for edge in [[r + change, c], [r, c + change]]:
                    if check_bounds(edge) and map[edge[0]][edge[1]] != 0:
                        g.insert_edge(r, c, edge[0], edge[1], map[edge[0]][edge[1]])
    return g

def process_args(argv):
    argv = argv[1:]
    data = []

    if '-f' not in argv and '-d' not in argv and '-g' not in argv:
        print('File/folder/test was not provided. Use -f to provide file, -d to provide a directory, or -g to generate test data randomly.')
        sys.exit(1)

    if '-f' in argv:
        data.append(get_data(argv[argv.index('-f') + 1]))
        print('f', data)
    elif '-d' in argv:
        directory = argv[argv.index('-d') + 1]
        data += [get_data(directory + ('' if directory[-1] == '/' else '/') + file) for file in os.listdir(directory)]
        print('d', data)
    else:
        for i in [[5, 5], [10, 10], [15, 15], [20, 20]]:
            data.append(generate_test_data(i))
        print('r', data)

    if '-A*':
        algorithm = 'a*'
    elif '-IDS':
        algorithm = 'iter'
    elif '-BFS':
        algorithm = 'bfs'
    else:
        print("Algorithm wasn't provided")
        sys.exit(1)

    return algorithm, data

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
    algorithm, data = process_args(sys.argv)
    # d has the structure [g, start_location, goal_location]
    for d in data:
        path, nodes_expanded = bfs(d[0], d[1])
        print_path(path)
        d[0].draw_graph()
        for i in d[0].edges:
            print(i)
            print(d[0].edges[i], end='\n\n')
    plt.show()
