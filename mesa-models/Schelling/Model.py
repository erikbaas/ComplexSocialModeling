from __future__ import division

import random
from mesa import Model
from mesa.time import RandomActivation
from mesa.space import SingleGrid
from mesa.datacollection import DataCollector

from Agents import SchellingAgent

class SchellingModel(Model):
    '''Model class for Schelling segregation model'''

    def __init__(self, height=20, width=20, density=.8, group_ratio=.66, minority_ratio=.5, homophily=3):
        self.height = height
        self.width = width
        self.density = density
        self.group_ratio = group_ratio
        self.minority_ratio = minority_ratio
        self.homophily = homophily
        self.happy = 0
        self.segregated = 0

        self.schedule = RandomActivation(self)
        self.grid = SingleGrid(height, width, torus=False)

        self.place_agents()
        self.datacollector = DataCollector( {'happy': (lambda m: m.happy), 'segregated': (lambda m: m.segregated)})
        self.running = True


    def step(self):
        '''Run one step of model'''
        self.schedule.step()
        self.calculate_stats()
        self.datacollector.collect(self)

        if self.happy == self.schedule.get_agent_count():
            self.running = False


    def place_agents(self):
        for cell in self.grid.coord_iter():
            x, y = cell[1:3]
            if random.random() < self.density:
                if random.random() < self.group_ratio:
                    if random.random() < self.minority_ratio:
                        group = 0
                    else:
                        group = 1
                else:
                    group = 2

                agent = SchellingAgent((x,y), group)
                self.grid.position_agent(agent, (x,y))
                self.schedule.add(agent)

        for agent in self.schedule.agents:
            count = 0
            for neighbour in self.grid.iter_neighbors(agent.pos, moore=False):
                if neighbour.group == agent.group:
                    count += 1
            agent.similar = count


    def calculate_stats(self):
        happy_count = 0
        avg_seg = 0
        for agent in self.schedule.agents:
            avg_seg += agent.similar
            if agent.similar >= self.homophily:
                happy_count += 1

        self.happy = happy_count
        self.segregated = avg_seg/self.schedule.get_agent_count()