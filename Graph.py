class Graph(dict):
    def __init__(self, vs=[], es=[]):
        ''' Create a new graph. (vs) is a list of vertices; (es) is a list of edges'''

        [self.add_vertex(v) for v in vs]

        [self.add_edge(e) for e in es]

    def add_vertex(self, v):
        ''' Add (v) to the graph'''
        self[v] = {}

    def add_edge(self, e):
        ''' Add (e) to the graph by adding an entry in both directions.
            Replaces previous edge if any
        '''

        v, w = e
        self[v][w] = e
        self[w][v] = e

    def get_edge(self, v0, v1):
        ''' Return the edge between (v0) and (v1) if it exists'''

        try:
            return self[v0][v1]
        except:
            return None

    def remove_edge(self, e):
        ''' Remove all references to (e) if it exists'''

        # for v in self.keys():
        #     for w in self[v].keys():
        #         if self[v][w] is e:
        #             del self[v][w]

        [self[v].pop(w) for v in self.keys() for w in self[v].keys() if (self[v][w] is e)]

    def vertices(self):
        ''' Returns a list of vertices in graph'''
        return self.keys()

    def edges(self):
        ''' Returns a list of edges in the graph'''
        return [val for v in self.vertices() for val in self[v].values()]

    def out_vertices(self, v):
        ''' Returns a list of adjacent vertices to (v)'''
        return self[v].keys()

    def out_edges(self, v):
        ''' Returns a list of adjacent edges to (v)'''
        return [self[v][w] for w in self[v].keys()]

    def add_all_edges(self):
        ''' Turns an edgeless Graph into a complete graph'''

        [self.add_edge(Edge(v,w)) for v in self.vertices() for w in self.vertices() if v!=w]

    def add_regular_edges(n):
        ''' Turns an edgeless graph into a degree (n) regular graph'''

        v_num = len(self.vertices())

        if n == v_num - 1:
            self.add_all_edges

        elif n > v_num - 1:
            print 'Not enough vertices'

        else:
            [self.add_edge(Edge(v,w)) for v in self.vertices()]


class Vertex(object):
    def __init__(self, label=''):
        self.label = label
    def __repr__(self):
        return 'Vertex(%s)' % repr(self.label)

    __str__ = __repr__

class Edge(tuple):
    def __new__(cls, e1, e2):
        return tuple.__new__(cls, (e1, e2))

    def __repr__(self):
        return 'Edge(%s, %s)' % (repr(self[0]), repr(self[1]))

    __str__ = __repr__


if __name__=='__main__':
    v = Vertex('v')
    w = Vertex('w')
    x = Vertex('x')
    e = Edge(v, w)
    f = Edge(v, x)
    g = Graph([v, w, x], [e, f])

    # Test get_edge
    print '----Graph.get_edge Test----'
    print g.get_edge(x, w)
    print g.get_edge(v, w)

    # Test remove_edge
    print '\r ----Graph.remove_edge Test----'
    g.remove_edge(e)
    print g

    #Test vertices
    print '\r ----Graph.vertices Test----'
    print g.vertices()

    #Test edges
    print '\r ----Graph.edges Test----'
    print g.edges()

    #Test out_vertices
    print '\r ----Graph.out_vertices Test----'
    g.add_edge(e)
    print g.out_vertices(v)
    g.remove_edge(f)
    print g.out_vertices(v)

    #Test out_edges
    print '\r ----Graph.out_edges Test----'
    g.add_edge(f)
    print g.out_edges(v)
    g.remove_edge(f)
    print g.out_edges(v)

    #Test add_all_edges
    g.remove_edge(e)
    g.remove_edge(f)
    g.add_all_edges()
    print g.edges()