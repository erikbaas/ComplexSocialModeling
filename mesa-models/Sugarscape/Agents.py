from __future__ import division

import random
from mesa import Agent


class SugarPatch(Agent):
    ''' An agent which does not move, regrows sugar, and transfers sugar
        when a ScapeAgent occupies the same space
    '''
    def __init__(self, unique_id, pos, max_sugar, growth_rate=1):
        self.pos = pos
        self.max_sugar = max_sugar
        self.sugar = max_sugar
        self.growth_rate = growth_rate
        self.unique_id = unique_id

    def step(self, model):
        ''' Agent step function: regrows sugar if below max '''

        if self.sugar < self.max_sugar:
            self.sugar += 1


class ScapeAgent(Agent):
    ''' An agent which searches for the richest sugar patches around it, and
        moves to that location, consuming sugar
    '''
    def __init__(self, unique_id, pos, wealth, metabolism, vision):
        self.pos = pos
        self.wealth = wealth
        self.metabolism = metabolism
        self.vision = vision
        self.unique_id = unique_id
        self.age = 0

    def step(self, model):
        ''' Agent step function: searches, moves, consumes sugar, checks for
            death condition
        '''

        patch = self.best_location(model)
        model.grid.move_agent(self, patch.pos)
        self.wealth -= self.metabolism
        self.consume(model, patch)

        if self.wealth <= 0:
            model.schedule.remove(self)
            model.grid._remove_agent(self.pos, self)

    def best_location(self, model):
        ''' Find the wealthiest sugar patch in the agent's neighbourhood,
            according to vision attribute
        '''

        options = []
        for cell in model.grid.iter_neighbors(self.pos, moore=False, include_center=True, radius=self.vision):
            free = True
            patch = None
            if type(cell) is tuple:
                for obj in cell:
                    if type(obj) == ScapeAgent:
                        free = False
                    if type(obj) == SugarPatch:
                        patch = obj
            else:
                if type(cell) == ScapeAgent:
                    free = False
                if type(cell) == SugarPatch:
                    patch = cell

            if free and (patch != None):
                options.append(patch)

        random.shuffle(options)
        options_wealth = [patch.sugar for patch in options]
        maximum = max(options_wealth)
        best_ind = options_wealth.index(maximum)

        return options[best_ind]

    def consume(self, model, patch):
        ''' Transfers SugarPatch's contents to agent '''
        self.wealth += patch.sugar
        patch.sugar = 0