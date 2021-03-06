#! /usr/bin/python
import sys, os
import numpy as np
import graph
import matplotlib.pyplot as plt
import random
import time
from queue import PriorityQueue

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

    f = open('test_files/' + str(dimensions[0]) + 'x' + str(dimensions[1]) + '.txt', mode='w+')
    f.write(str(dimensions[0]) + ' ' + str(dimensions[1])+'\n')
    f.write(str(start_location[0]) + ' ' + str(start_location[1])+'\n')
    f.write(str(goal_location[0]) + ' ' + str(goal_location[1])+'\n')

    for i in map:
        f.write(str(i)[1:-1].replace(',','') + '\n')
    f.close()

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
    elif '-d' in argv:
        directory = argv[argv.index('-d') + 1]
        data += [get_data(directory + ('' if directory[-1] == '/' else '/') + file) for file in os.listdir(directory)]
    else:
        for i in [[5, 5], [10, 10], [15, 15], [20, 20]]:
            data.append(generate_test_data(i))

    if '-A*' in argv:
        algorithm = lambda d: A_s(d[0], d[1], d[2])
    elif '-IDS' in argv:
        algorithm = lambda d: iterative_deepening(d[0], d[1], d[2])
    elif '-BFS' in argv:
        algorithm = lambda d: bfs(d[0], d[1], d[2])
    else:
        print("Algorithm wasn't provided")
        sys.exit(1)

    return algorithm, data

def manhattan_distance(a, b):
    return abs(b[0] - a[0]) + abs(b[1] - a[1])

def A_s(g, start_location, goal_location):
    start_time = time.time()
    q = PriorityQueue()
    came_from = np.zeros((g.dimensions[0], g.dimensions[1], 2), dtype=int) - 1
    cost_so_far = {} # {location([int, int]): cost(float)}
    max_nodes_in_mem = 0
    nodes_expanded = 0

    q.put(start_location, 0)
    cost_so_far[str(start_location[0]) + ', ' + str(start_location[1])] = 0

    while not q.empty():
        max_nodes_in_mem = max(max_nodes_in_mem, q.qsize())
        current = q.get()
        nodes_expanded += 1
        current_str = str(current[0]) + ', ' + str(current[1])

        if time.time() - start_time >= 180:
            print("A* will take more than 3 minutes, returned values are computed results.")
            return get_path(came_from, goal_location), nodes_expanded, (time.time() - start_time) * 1000, max_nodes_in_mem

        if current[0] == goal_location[0] and current[1] == goal_location[1]:
            break

        for edge in g.edges[current_str]:
            new_cost = cost_so_far[current_str] + edge[1]
            edge_str = str(edge[0][0]) + ', ' + str(edge[0][1])
            if edge_str not in cost_so_far or new_cost < cost_so_far[edge_str]:
                cost_so_far[edge_str] = new_cost
                priority = new_cost + manhattan_distance(edge[0], goal_location)
                q.put(edge[0], priority)
                came_from[edge[0][0], edge[0][1]] = current
    return get_path(came_from, goal_location), nodes_expanded, (time.time() - start_time) * 1000, max_nodes_in_mem



def DLS(g, path, goal_location, maxDepth):
    current = path[-1]
    if current[0] == goal_location[0] and current[1] == goal_location[1]:
        return path
    if maxDepth <= 0:
        return None
    for edge in g.edges[str(current[0]) + ', ' + str(current[1])]:
        new_path = path.copy()
        new_path.append(edge[0])
        result = DLS(g, new_path, goal_location, maxDepth-1)
        if result is not None:
            return result


def iterative_deepening(g, start_location, goal_location):
    start_time = time.time()
    maxDepth = g.dimensions[0] * g.dimensions[1]
    path = [start_location]
    nodes_expanded = 0
    max_nodes_in_mem = 0

    for depth in range(maxDepth):
        
         if time.time() - start_time >= 180:
            print("IDS will take more than 3 minutes, returned values are computed results.")
            return result, nodes_expanded, (time.time() - start_time) * 1000, max_nodes_in_mem
            
        result = DLS(g, path, goal_location, depth)
        nodes_expanded += 1
        if result:
            return result, nodes_expanded, (time.time() - start_time) * 1000, max_nodes_in_mem
    return result, nodes_expanded, (time.time() - start_time) * 1000, max_nodes_in_mem

def bfs(g, start_location, goal_location):
    start_time = time.time()
    visited = np.zeros(g.dimensions, dtype=bool)
    nodes_expanded = 0
    max_nodes_in_mem = 0
    prev = np.zeros((g.dimensions[0], g.dimensions[1], 2), dtype=int) - 1 # this will allow to trace back the path
    q = []
    q.append(start_location)
    visited[start_location[0], start_location[1]] = True

    while q:
        if time.time() - start_time >= 180:
            print("BFS will take more than 3 minutes, returned values are computed results.")
            return get_path(prev, goal_location), nodes_expanded, (time.time() - start_time) * 1000, max_nodes_in_mem
        u = q.pop(0)
        max_nodes_in_mem = max_nodes_in_mem if max_nodes_in_mem > len(q) else len(q)
        nodes_expanded += 1
        for edge in g.edges[str(u[0]) + ', ' + str(u[1])]:
            if not visited[edge[0][0], edge[0][1]]:
                visited[edge[0][0], edge[0][1]] = True
                prev[edge[0][0], edge[0][1]] = u
                q.append(edge[0])
    return get_path(prev, goal_location), nodes_expanded, (time.time() - start_time) * 1000, max_nodes_in_mem

def get_path(path, goal):
    path_sequence = []
    prev = goal
    current = path[prev[0]][prev[1]]

    while current[0] != -1 and current[1] != -1:
        path_sequence.append(prev)
        prev = current
        current = path[current[0]][current[1]]
    path_sequence.append(prev)
    return path_sequence

# extracts cost from given path with structure: [start ... goal]
def get_path_cost(path, graph_info):
    cost = 0
    g, _, _ = graph_info
    for i in range(1, len(path)):
        cost += g.get_weight(path[i-1], path[i])
    return cost

if __name__ == "__main__":
    algorithm, data = process_args(sys.argv)
    # d has the structure [g, start_location, goal_location]
    for d in data:
        path, nodes_expanded, runtime, max_nodes_in_mem = algorithm(d)
        cost = get_path_cost(path, d)
        print('Cost:', cost)
        print('Number of nodes expanded:', nodes_expanded)
        print('Max number of nodes held in memory:', max_nodes_in_mem)
        print('Runtime in milliseconds:', runtime)
        print('Path sequence:', end=' ')
        for step in path:
            print(step, end=' ')
        print('\n\n')
        d[0].draw_graph()
    plt.show()
