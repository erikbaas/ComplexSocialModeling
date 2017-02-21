import math
import random
import string
import sys

from Graph import Graph, Edge, Vertex
from GraphWorld import GraphWorld
from RandomGraph import RandomGraph
from SmallWorldGraph import SmallWorldGraph

class ScalingNetworkGraph(SmallWorldGraph):
    def __init__(self, p, m_0, t):
        vs = [Vertex('v'+str(i)) for i in xrange(m_0)]
        RandomGraph.__init__(self, vs, p)

        self.sum_k = sum([len(self[v]) for v in self])
        [self.add_prefer_vert(str(i+m_0)) for i in xrange(t)]

        self.assign_edge_lengths()
        self.clust = self.clustering_coefficient()
        self.length = self.average_length()
        self.avg_deg = self.average_degree()

    def add_prefer_vert(self, vid):
        vs = self.vertices()
        vert = Vertex(vid)
        self.add_vertex(vert)

        for v in vs:
            k_i = len(self[v])
            if random.random() > k_i/float(self.sum_k): continue
            self.add_edge(Edge(vert, v))
            self.sum_k += 1

    def average_degree(self):
        degs = [len(self.out_vertices(v)) for v in self.vertices()]
        return sum(degs)/float(len(degs))

g = ScalingNetworkGraph(.5, 100, 900)