import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy.random as nrand
import random as r
import scipy.stats as stats


# class PoliNode:
#     def __init__(self, label, polarization, ideology):
#         self.label = label
#         self.polarization = polarization
#         self.ideology = ideology



n = 100
k = 20
p = .05
mu = 0
sigma = .33


def genSmallWorld(n, k, p, mu, sigma):

    pInitVals = dict(zip([i for i in range(n)], nrand.normal(mu, sigma, n)))
    iInitVals = dict(zip([i for i in range(n)], nrand.normal(mu, sigma, n)))

    G = nx.connected_watts_strogatz_graph(n, k, p)
    nx.set_node_attributes(G, 'polarization', pInitVals)
    nx.set_node_attributes(G, 'ideology', iInitVals)

    return G

def genPrefAttach(n, ):
    pass


def checkDistr(G):
    nodes = [i for i in G.nodes(data=True)]

    pVals = [node[1]['polarization'] for node in nodes]
    iVals = [node[1]['ideology'] for node in nodes]

    pMean = sum(pVals)/n
    iMean = sum(iVals)/n
    regress = stats.linregress(pVals, iVals)

    return [pMean, iMean, regress]

def step(G):


    label = r.randint(0, n-1)
    if G[label]:
        neighbors = G[label].keys()
    else:
        return

    article = findArticle(G, label)

    influence = .3

    for num in neighbors:
        currIdeo = G.node[num]['ideology']
        ideoChange = influence*(article - currIdeo)
        G.node[num]['ideology'] += ideoChange


def findArticle(G, label):

    # Find an article that is close to agent's ideological preference
    ideo = G.node[label]['ideology']

    # TODO: Leeway based on how polarized that agent is
    lower = ideo - .3
    upper = ideo + .3

    if lower < -1:
        lower = -1

    if upper > 1:
        upper = 1

    article = r.uniform(lower, upper)

    return article

def run(G):

    ideos = []
    for i in range(300):
        step(swG)
        vals = [node[1]['ideology'] for node in G.nodes(data=True)]
        ideos.append(vals)

    return ideos


def animate(colors, layout, G):
    nx.draw_networkx(G, pos=layout, cmap=plt.get_cmap('bwr'), vmin=-1, vmax=1, node_color=colors, with_labels=False)


if __name__=='__main__':
    swG = genSmallWorld(n, k, p, mu, sigma)

    layout = nx.circular_layout(swG)
    colors = run(swG)

    plt.clf()
    nx.draw_networkx(swG, pos=layout, cmap=plt.get_cmap('bwr'), vmin=-1, vmax=1, node_color=colors[0], with_labels=False)

    fig = plt.gcf()
    ani = animation.FuncAnimation(fig, animate, frames=colors, fargs=(layout, swG), interval=10, repeat=False)
    plt.show()



