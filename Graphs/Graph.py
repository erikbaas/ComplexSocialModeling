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

    has_edge = get_edge

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
        s = set()
        for d in self.itervalues():
            s.update(d.itervalues())
        return list(s)

    def out_vertices(self, v):
        ''' Returns a list of adjacent vertices to (v)'''
        return self[v].keys()

    def out_edges(self, v):
        ''' Returns a list of adjacent edges to (v)'''
        return [self[v][w] for w in self[v].keys()]

    def add_all_edges(self):
        ''' Turns an edgeless Graph into a complete graph'''

        [self.add_edge(Edge(v,w)) for v in self.vertices() for w in self.vertices() if v!=w]

    def add_regular_edges(self, n):
        ''' Turns an edgeless graph into a degree (n) regular graph'''

        vs = self.vertices()

        if n >= len(vs):
            raise ValueError, ('Not enough vertices in graph')

        if n == len(vs) - 1:
            self.add_all_edges

        if n%2 != 0:
            if len(vs)%2 != 0:
                raise ValueError, ('Cannot create this graph')
            self.add_regular_edges_even(n-1)
            self.add_regular_edges_odd()
        else:
            self.add_regular_edges_even(n)

    def add_regular_edges_even(self, k):
        ''' Make a regular graph if the degree is even '''

        vs = self.vertices()
        double = vs*2

        for i, v in enumerate(vs):
            for j in range(1, k/2 +1):
                w = double[i+j]
                self.add_edge(Edge(v,w))

    def add_regular_edges_odd(self):
        ''' Add extra 'crossing' edge for a graph with odd degree '''

        vs = self.vertices()
        double = vs*2

        for i in range(len(vs)/2):
            v = double[i]
            w = double[i + len(vs)/2]
            self.add_edge(Edge(v,w))


    def is_connected(self):
        ''' Returns True if the graph is connected, False otherwise'''

        queue = [self.keys()[0]]
        marked = [self.keys()[0]]

        while len(queue) > 0:
            v = queue.pop(0)
            for w in self.out_vertices(v):
                if w not in marked:
                    queue.append(w)
                    marked.append(w)


        if len(marked) == len(self.keys()):
            return True
        else:
            return False




class Vertex(object):
    def __init__(self, label=''):
        self.label = label
        self.mark = False
    def __repr__(self):
        return 'Vertex(%s)' % repr(self.label)

    def mark(self):
        self.mark = True

    __str__ = __repr__

class Edge(tuple):
    def __new__(cls, e1, e2):
        return tuple.__new__(cls, (e1, e2))

    def __repr__(self):
        return 'Edge(%s, %s)' % (repr(self[0]), repr(self[1]))

    __str__ = __repr__