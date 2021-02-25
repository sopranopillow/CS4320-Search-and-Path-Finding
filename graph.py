#! /usr/bin/python
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import BoxStyle
import math

class Graph:
    def __init__(self, dimensions):  # assuming all are weighted and directed
        """
        Instead of using a list, it uses a dictionary to count an edges as a coordinate instead of a flatened array.
        Dictionary has the following structure:
        {
            "row, column" : [[edge_1], [edge_2], [edge_3], ..., [edge_c]]
        }

        Each edge has the following strcuture:
        [[row, col], weight]
        Note: the coordinate inside the edge is where it connects to therefore and edge looks like this:
        {
            "edge_source": [[edge_destination], edge_weight]
        }

        """
        self.edges = {}
        self.dimensions = dimensions

    def __str__(self):
        return str(self.edges)

    def __len__(self):
        return self.dimensions[0] * self.dimensions[1]

    def draw_graph(self): # note that when there's no edges, drawing might look a little off
        fig, ax = plt.subplots()
        coords = {}

        # set coordinates coords = [[x, y]]
        for r in range(self.dimensions[0]):
            for c in range(self.dimensions[1]):
                coords[str(r) + ', ' + str(c)] = [1*c, -1*r]

        # draw edges
        for r in range(self.dimensions[0]):
            for c in range(self.dimensions[1]):
                coordinate = str(r) + ', ' + str(c)
                if self.edges.get(coordinate):
                    for e in self.edges[coordinate]:
                        src = coords[coordinate]
                        dest = coords[str(e[0][0]) + ', ' + str(e[0][1])]
                        ax.plot([src[0], dest[0]],[src[1], dest[1]],linewidth=1,color="k")

        # draw nodes
        for coord in coords:
            ax.text(coords[coord][0], coords[coord][1], coord, size=50//(max(self.dimensions)), ha="center", va="center",
                bbox=dict(facecolor='w',boxstyle=BoxStyle("Round", pad=.4)))

        ax.set_aspect(1.0)
        ax.axis('off')

    def insert_edge(self, s_r, s_c, d_r, d_c, w): # all edges are connected from the sides
        source = str(s_r) + ', ' + str(s_c) # this is the dictionary entry that represents the edges, basically 'row, column'
        if self.edges.get(source) == None:
            self.edges[source] = [[[d_r, d_c],w]]
        else:
            self.edges[source].append([[d_r, d_c],w])