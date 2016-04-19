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
        self.pollution = 0
        self.amenity = max_sugar

    def step(self, model):
        ''' Agent step function: regrows sugar if below max '''

        if self.sugar < self.max_sugar:
            # Growth can be affected by pollution or remain constant:
            # self.sugar += 1
            self.sugar += 1.01**(-self.pollution)

        if model.diffusion_rule:
            self.pollution = self.diffuse(model)

        # If growth is affected by pollution, amenity should be equal to sugar:
        self.amenity = self.sugar
        # self.amenity = self.sugar/(1+self.pollution)

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
        prev = self.pollution
        self.pollution += val
        if self.pollution != (prev + val):
            print('WTF')

class ScapeAgent(Agent):
    ''' An agent which searches for the richest sugar patches around it, and
        moves to that location, consuming sugar
    '''

    def __init__(self, unique_id, pos, wealth, metabolism, vision, max_age, curr_patch):
        self.pos = pos
        self.wealth = wealth
        self.metabolism = metabolism
        self.vision = vision
        self.unique_id = unique_id
        self.age = 0
        self.max_age = max_age
        self.curr_patch = curr_patch

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
            check1 = worst_patch.pollution + self.curr_patch.pollution
            error = 'Worst: ' + str(worst_patch.pollution) + ' Curr: ' + str(self.curr_patch.pollution)

            worst_patch.add_pollution(self.curr_patch.pollution)
            self.curr_patch.pollution = 0

            check2 = worst_patch.pollution + self.curr_patch.pollution

            if check1 != check2:
                print(error)
                print('And Worst: ', worst_patch.pollution, ' Curr: ', self.curr_patch.pollution)

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
            patch.pollution += gained
