
import math
import random
import string
import sys

from Graph import Graph, Edge, Vertex
from GraphWorld import GraphWorld
from RandomGraph import RandomGraph

class SmallWorldGraph(Graph):
    def __init__(self, vs, k, p):
        Graph.__init__(self, vs, [])
        self.add_regular_edges(k)
        self.rewire(p)
        self.assign_edge_lengths()
        self.clust = self.clustering_coefficient()
        self.length = self.average_length()

    def assign_edge_lengths(self):
        """Gives each edge a length attribute."""
        for e in self.edges():
            e.length = 1

    def rewire(self, p):
        es = self.edges()
        vs = self.vertices()
        # Try to make this not random at some point
        random.shuffle(es)
        for e in es:
            if random.random() > p: continue

            v, w = e
            self.remove_edge(e)

            while True:
                w = random.choice(vs)
                if (w is not v) and (not self.has_edge(v, w)): break

            self.add_edge(Edge(v,w))

    def clustering_coefficient(self):
        C = []
        for v in self:
            adj = self.out_vertices(v)
            num_adj = len(adj)
            if num_adj < 2: max_pairs = 1
            else: max_pairs = num_adj*(num_adj-1)/2.0
            Cv = len([1 for v in adj for w in adj if self[v].get(w, False)])
            C.append(Cv/max_pairs)

        return avg(C)

    def shortest_path(self, vert):
        L = {v:float('Inf') for v in self.vertices()}
        L[vert] = 0
        queue = [vert]
        i = 1
        while queue:
            v = queue.pop(0)
            for w in self.out_vertices(v):
                if i < L[w]:
                    queue.append(w)
                    L[w] = i

            i += 1

        for key, value in L.iteritems():
            key.dist = value

    def char_length(self):
        """Computes the characteristic length of the graph according
        to the definition in Watts and Strogatz.

        Uses Dijkstra's algorithm from all vertices.

        Precondition: the graph is connected.
        """
        # for each vertex v, d[v] is the list of other vertices
        # and their distances
        d = {}
        for v in self:
            self.shortest_path_tree(v, d)
            t = [((w,v), w.dist) for w in self if w is not v]
            d.update(t)

        # return the average of all values
        return avg(d.values())

    def shortest_path_tree(self, s, hint=None):
        """Finds the length of the shortest path from Vertex (s) to the
        other Vertices; stores the path lengths as a dist attribute.
        (uses Dijkstra's algorithm).

        In theory this is a bad implementation of Dijkstra's algorithm:
        it keeps the priority queue as a sorted list and re-sorts after
        processing each vertex.

        But in practice this turns out to be pretty good, because Python's
        sort algorithm is fast for lists that are almost sorted.

        hint: a dictionary that maps from tuples (v,w) to already-known
        shortest path length from v to w.
        """
        if hint == None:
            hint = {}

        # initialize distance attribute for each vertex
        for v in self.iterkeys():
            v.dist = hint.get((s, v), Inf)
        s.dist = 0

        # start with all vertices in the queue
        queue = [v for v in self if v.dist < Inf]
        flag = True

        while len(queue) > 0:

            # re-sort the queue if necessary, then pop the lowest item
            if flag:
                queue.sort(key=lambda v: v.dist)
            flag = False
            v = queue.pop(0)

            # for each neighbor of v, see if we found a new shortest path
            for w, e in self[v].iteritems():
                new = v.dist + e.length
                if w.dist > new:
                    w.dist = new
                    queue.append(w)
                    flag = True

    def average_length(self):

        vs = self.vertices()
        tot_length = []
        for v in vs:
            self.shortest_path(v)
            lengths = [v.dist for v in vs]
            tot_length.append(avg(lengths))

        return avg(tot_length)

def avg(lst):
    return sum(lst)/float(len(lst))

Inf = float('Inf')












