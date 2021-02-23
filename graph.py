import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import BoxStyle
import math

class Graph:
    def __init__(self, dimensions):  # assuming all are weighted and directed
        self.edges = {}
        self.dimensions = dimensions

    def __str__(self):
        return str(self.edges)

    def __len__(self):
        return self.dimensions[0] * self.dimensions[1]

    def draw_graph(self):
        fig, ax = plt.subplots()
        n = len(self)
        r = 30
        coords = {}

        # set coordinates coords = [[x, y]]
        for r in range(self.dimensions[0]):
            for c in range(self.dimensions[1]):
                coords[str(r) + ', ' + str(c)] = [.2*c, -.2*r]

        # draw edges
        for r in range(self.dimensions[0]):
            for c in range(self.dimensions[1]):
                coordinate = str(r) + ', ' + str(c)
                if self.edges.get(coordinate):
                    for e in self.edges[coordinate]:
                        src = coords[coordinate]
                        dest = coords[str(e[0][0]) + ', ' + str(e[0][1])]
                        ax.plot([src[0], dest[0]],[src[1], dest[1]],linewidth=1,color="k")
                        ax.arrow(src[0], src[1],
                            (dest[0]-src[0])-(.07 if src[0] != dest[0] else 0),
                            (dest[1]-src[1])-(.07 if src[1] != dest[1] else 0),
                            head_width=0.04, head_length=0.04, lw=1)

        # draw nodes
        for coord in coords:
            ax.text(coords[coord][0], coords[coord][1], coord, size=10, ha="center", va="center",
                bbox=dict(facecolor='w',boxstyle=BoxStyle("Round", pad=.4)))

        # ax.set_aspect(1.0)
        ax.axis('off')

    def insert_edge(self, r, c, w): # all edges are connected from the sides
        # coordinate[0] and dimensions[0] ==> rows
        # coordinate[1] and dimensions[1] ==> columns
        check_bounds = lambda coordinate: (coordinate[0] < self.dimensions[0] and coordinate[0] >= 0) and \
                (coordinate[1] < self.dimensions[1] and coordinate[1] >= 0)

        if check_bounds((r, c)):
            

        if self.edges.get(source) == None:
            self.edges[source] = [[[r,c],w]]
        else:
            self.edges[source].append([[r,c],w])

        # connections = {'r':[[r-1, c], [r+1, c]], 'c': [[r, c-1], [r, c+1]]} # possible connections
        # for i in ['r', 'c']:
        #     for connection in connections[i]:
        #         if check_bounds(connection):
        #             source = str(connection[0]) + ', ' + str(connection[1])
        #             if self.edges.get(source) == None:
        #                 self.edges[source] = [[[r,c],w]]
        #             else:
        #                 self.edges[source].append([[r,c],w])