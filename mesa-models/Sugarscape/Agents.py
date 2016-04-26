from __future__ import division

import random
from mesa import Agent

class SugarPatch(Agent):
    ''' An agent which does not move, regrows sugar, and transfers sugar
        when a ScapeAgent occupies the same space
    '''
    def __init__(self, unique_id, pos, max_sugar, growth_rate=1, init_poll=1):
        self.pos = pos
        self.max_sugar = max_sugar
        self.sugar = max_sugar
        self.growth_rate = growth_rate
        self.unique_id = unique_id
        self.pollution = init_poll
        self.amenity = max_sugar

    def step(self, model):
        ''' Agent step function: regrows sugar if below max '''

        if self.sugar < self.max_sugar:
            # Growth can be affected by pollution or remain constant:
            if model.poll_growth_rule:
                self.sugar += 1.01**(-self.pollution)
            else:
                self.sugar += 1


        if model.diffusion_rule:
            self.pollution = self.diffuse(model)

        # If growth is affected by pollution, amenity should be equal to sugar:
        if model.poll_growth_rule:
            self.amenity = self.sugar
        else:
            self.amenity = self.sugar/(1+self.pollution)

    def diffuse(self, model):
        '''Distribute pollution evenly across agent's neighborhood'''

        flux = 0
        for cell in model.grid.iter_neighbors(self.pos, moore=False, include_center=True, radius=1):
            if type(cell) == SugarPatch:
                flux += cell.pollution
            elif type(cell) == tuple:
                for obj in cell:
                    if type(obj) == SugarPatch:
                        flux += obj.pollution

        return flux/5.0

    def add_pollution(self, val):
        self.pollution += val

class ScapeAgent(Agent):
    ''' An agent which searches for the richest sugar patches around it, and
        moves to that location, consuming sugar
    '''

    def __init__(self, unique_id, pos, wealth, metabolism, vision, max_age, curr_patch, ex_ratio):
        self.pos = pos
        self.wealth = wealth
        self.metabolism = metabolism
        self.vision = vision
        self.unique_id = unique_id
        self.age = 0
        self.max_age = max_age
        self.curr_patch = curr_patch
        self.ex_ratio = ex_ratio

    def step(self, model):
        ''' Agent step function: searches, moves, consumes sugar, checks for
            death condition
        '''

        best_patch = self.best_location(model)
        worst_patch = self.worst_location(model)

        self.wealth -= self.metabolism

        if model.pollution_rule:
            self.curr_patch.pollution += self.metabolism

        if model.push_rule:
            if model.expend_rule:
                #Agent can spend half its wealth to move pollution
                expend = self.wealth/self.ex_ratio

                if self.curr_patch.pollution >= expend:
                    self.curr_patch.pollution -= expend
                    worst_patch.pollution += expend
                    self.wealth -= expend
                else:
                    worst_patch.pollution += self.curr_patch.pollution
                    self.curr_patch.pollution = 0
                    self.wealth -= self.curr_patch.pollution
            else:
                worst_patch.pollution += self.curr_patch.pollution
                self.curr_patch.pollution = 0


        model.grid.move_agent(self, best_patch.pos)
        self.curr_patch = best_patch
        self.consume(model, best_patch)
        self.age += 1


        if model.replacement_rule:
            if (self.wealth <= 0) or (self.age == self.max_age):
                model.schedule.remove(self)
                model.grid._remove_agent(self.pos, self)
                model.new_agent(self.unique_id)
        else:
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

            if type(cell) == SugarPatch:
                options.append(cell)

        random.shuffle(options)
        options_amenity = [patch.amenity for patch in options]
        maximum = max(options_amenity)
        best_ind = options_amenity.index(maximum)

        return options[best_ind]

    def worst_location(self, model):
        ''' Find the worst polluted/least amenable location in agent's neighborhood,
            according to vision attribute
        '''

        options = []
        for cell in model.grid.iter_neighbors(self.pos, moore=False, include_center=False, radius=self.vision):
            free = True
            patch = None

            if type(cell) == SugarPatch:
                options.append(cell)

        random.shuffle(options)
        options_metric = [patch.amenity for patch in options]
        # options_metric = [patch.pollution for patch in options]
        minimum = min(options_metric)
        worst_ind = options_metric.index(minimum)

        return options[worst_ind]


    def consume(self, model, patch):
        ''' Transfers SugarPatch's contents to agent and pollutes'''
        gained = patch.sugar
        self.wealth += gained
        patch.sugar = 0
        if model.pollution_rule:
            patch.pollution += .5*gained
