from Graph import Graph, Edge, Vertex
import random

class RandomGraph(Graph):
    def __init__(self, vs, p):
        Graph.__init__(self, vs, [])
        self.add_random_edges(p)

    def add_random_edges(self, p):
        if self.edges() != []:
            print 'This method only takes an edgeless graph'
        else:
            for v in self.vertices():
                for w in self.vertices():
                    if v != w:
                        rand = random.uniform(0, 1)
                        if rand < p:
                            self.add_edge(Edge(v, w))


if __name__ == '__main__':
    v = Vertex('v')
    w = Vertex('w')
    x = Vertex('x')
    y = Vertex('y')
    e = Edge(v, w)
    rand_graph = RandomGraph([v, w, x, y], .3)
    print rand_graph.edges()

    # rand_graph.add_random_edges(.3)
    # print rand_graph.edges()
