from __future__ import division

from mesa import Agent

class SchellingAgent(Agent):
    '''Agent class for Schelling segregation model'''

    def __init__(self, pos, group):
        self.unique_id = pos
        self.pos = pos
        self.group = group
        self.similar = 0

    def step(self, model):
        if self.similar < model.homophily:
            model.grid.move_to_empty(self)

        count = 0
        for neighbour in model.grid.iter_neighbors(self.pos, moore=True):
            if neighbour.group == self.group:
                count += 1
        self.similar = count