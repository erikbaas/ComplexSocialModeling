from __future__ import division
from Graph import *
from RandomGraph import *
from GraphWorld import *
from SmallWorldGraph import *
from ScalingNetworkGraph import *
from matplotlib import pyplot as plt
from generator import AlphaNumGen
import string
import random
import math
import swampy

from itertools import chain

try:
    from Gui import Gui, GuiCanvas
except ImportError:
    from swampy.Gui import Gui, GuiCanvas


def something():
    n = 10
    p = 1

    # create n Vertices
    n = int(n)
    labels = string.ascii_lowercase + string.ascii_uppercase
    vs = [Vertex(c) for c in labels[:n]]

    # create a graph and a layout
    # g = RandomGraph(vs, p)
    g = Graph(vs, [])
    g.add_regular_edges(4)
    layout = CircleLayout(g)

    # draw the graph
    gw = GraphWorld()
    gw.show_graph(g, layout)
    gw.mainloop()

def connect_vs_p(n, trials):
    ''' Plot average connectedness of graph w/ degree (n) over p = 0:100, (trials) times'''

    connected = []
    xs = [i/100 for i in xrange(101)]
    vs = [Vertex('v'+str(i)) for i in xrange(n)]
    for i in xs:
        print i
        subconnected = []
        for j in xrange(trials):
            g = RandomGraph(vs)
            g.add_random_edges(i)
            if g.is_connected():
                subconnected.append(1)
            else:
                subconnected.append(0)
        connected.append(subconnected)

    ys = [sum(sub)/trials for sub in connected]
    return xs, ys

def Cp_over_C0():
    vs = [Vertex('v'+str(i)) for i in xrange(100)]
    clust_list = []
    xs = [x/100.0 for x in xrange(101)]
    g = []
    for p in xs:
        g.append([SmallWorldGraph(vs, 5, p) for el in xrange(20)])
        print p

    print 'Created graphs'
    gLs = [[ele.length for ele in sublist] for sublist in g]
    print 'Got lengths'
    gCs = [[ele.clust for ele in sublist] for sublist in g]
    print 'Got clustering'


    clust = [avg(lst) for lst in gCs]
    lens = [avg(lst) for lst in gLs]
    yCs = [val/float(clust[0]) for val in clust]
    yLs = [val/float(lens[0]) for val in lens]

    plt.semilogx(xs, yCs, basex=10)
    plt.semilogx(xs, yLs, basex=10)
    plt.title('Normalized clustering and avg. path lengths for p values in SWG')
    plt.xlabel('p values (log)')
    plt.ylabel('Normalized Values')
    plt.legend(['Clustering', 'Path Lengths'])
    plt.show()

def test_graph_methods():
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

def compare_cvp():
    x1s, y1s = connect_vs_p(5, 40)
    x2s, y2s = connect_vs_p(25, 40)
    x3s, y3s = connect_vs_p(125, 40)

    plt.subplot(3,1,1)
    plt.scatter(x1s, y1s)
    plt.title('Connectedness for degree 5/25/125 random graphs')
    plt.xlabel('p Values')
    plt.ylabel('Average Connectedness')

    plt.subplot(3,1,2)
    plt.scatter(x2s, y2s)
    plt.xlabel('p Values')
    plt.ylabel('Average Connectedness')

    plt.subplot(3,1,3)
    plt.scatter(x3s, y3s)
    plt.xlabel('p Values')
    plt.ylabel('Average Connectedness')
    plt.show()

def test_scaling():

    vs = [Vertex(str(i)) for i in xrange(1000)]
    # g = Graph(vs, [])
    g_scale = ScalingNetworkGraph(.1, 100, 900)
    print g_scale.avg_deg

    # g = [SmallWorldGraph(vs, int(round(g_scale.avg_deg)), 0) for i in xrange(20)]

    # gL = avg([ele.length for ele in g])
    # gC = avg([ele.clust for ele in g])

    # g = SmallWorldGraph(vs, int(round(g_scale.avg_deg)), .1)
    # # g.add_regular_edges(11)
    layout = CircleLayout(g_scale)

    # # draw the graph
    gw = GraphWorld()
    gw.show_graph(g_scale, layout)
    gw.mainloop()


    # layout = CircleLayout(gscale)
    # gw = GraphWorld()
    # gw.show_graph(g_norm, layout)
    # gw.mainloop()


    print gL, gC
    # print g_scale.clust/gL, g_scale.length/gC

def avg(lst):
    return sum(lst)/float(len(lst))

if __name__=='__main__':
    # compare_cvp()
    test_scaling()

    # test_scaling()
    # Cp_over_C0()
    # g = SmallWorldGraph([Vertex('v'), Vertex('x'), Vertex('y'), Vertex('z')], 2, .3)
    # print g.cluster_coef()

    # n = int(6)
    # k = 3
    # p = .8
    # labels = string.ascii_lowercase + string.ascii_uppercase
    # vs = [Vertex(c) for c in labels[:n]]

    # g = SmallWorldGraph(vs, k, p)
    # print g.length

    # layout = CircleLayout(g)

    # print g.clustering_coefficient()
    # raw_input('')
    # # draw the graph
    # gw = GraphWorld()
    # gw.show_graph(g, layout)
    # gw.mainloop()

