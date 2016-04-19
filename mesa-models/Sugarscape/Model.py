from __future__ import division

import random
from collections import defaultdict

from mesa import Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector

from Agents import SugarPatch, ScapeAgent


class SugarscapeModel(Model):
    def __init__(self, height=50, width=50, init_agents=500, max_metabolism=3, max_vision=10, max_init_sugar=5, min_age=30, max_age=60):
        self.height = height
        self.width = width
        self.init_agents = init_agents
        self.max_metabolism = max_metabolism
        self.max_vision = max_vision
        self.max_init_sugar = max_init_sugar
        self.min_age = min_age
        self.max_age = max_age

        self.replacement_rule = True
        self.pollution_rule = False
        self.diffusion_rule = False
        self.push_rule = False

        self.map = self.import_map()
        self.grid = MultiGrid(height, width, torus=True)
        self.schedule = RandomActivationByType(self)
        self.datacollector = DataCollector({'Pollution': (lambda m: m.total_pollution)},
                                           {'Wealth': self.collect_wealth,
                                            'Metabolism': self.collect_metabolism,
                                            'Vision': self.collect_vision})

        self.total_wealth = 1500
        self.total_pollution = 0

        self.populate_sugar()
        self.populate_agents()


    def step(self):
        ''' Step method run by the visualization module'''
        self.schedule.step([ScapeAgent, SugarPatch])
        self.datacollector.collect(self)

        if self.schedule.time == 20:
            self.pollution_rule = True
        if self.schedule.time == 30:
            self.push_rule = True

        self.total_wealth = 0
        self.total_pollution = 0
        for agent in self.schedule.agents_by_type[ScapeAgent]:
            self.total_wealth += agent.wealth
        for patch in self.schedule.agents_by_type[SugarPatch]:
            self.total_pollution += patch.pollution


    def import_map(self):
        ''' Imports a text file into an array to be used when generating and
            placing the sugar Agents into the grid
        '''

        f = open('sugar_map.txt', 'r')
        map_list = []
        for line in f:
            num_list = line.split(' ')
            for num in num_list:
                map_list.append(int(num[0]))

        return map_list

    def new_agent(self, uid):
        ''' Place a new agent on the sugarscape in order to replace a death'''
        free = False
        while not free:
            location = random.choice([cell for cell in self.grid.coord_iter()])
            if len(location[0]) == 1:
                free = True

        pos = (location[1], location[2])
        patch = self.grid.get_cell_list_contents([pos])[0]
        agent = ScapeAgent(uid, pos, random.randint(1,self.max_init_sugar), random.randint(1,self.max_metabolism), random.randint(1,self.max_vision), random.randint(self.min_age, self.max_age), patch)

        self.grid.place_agent(agent, agent.pos)
        self.schedule.add(agent)

    def populate_agents(self):
        ''' Place ScapeAgent's in random unoccupied locations on the grid with randomomized
            sets of parameters
        '''

        cells = [(cell[1], cell[2]) for cell in self.grid.coord_iter()]
        for i in range(self.init_agents):
            uid = 'a' + str(i)
            location = random.choice(cells)
            cells.remove(location)
            patch = self.grid.get_cell_list_contents([location])[0]
            agent = ScapeAgent(uid, location, random.randint(1,self.max_init_sugar), random.randint(1,self.max_metabolism), random.randint(1,self.max_vision), random.randint(self.min_age, self.max_age), patch)
            self.grid.place_agent(agent, location)
            self.schedule.add(agent)

    def populate_sugar(self):
        ''' Place SugarPatch's on every cell with maximum sugar content
            according to the imported 'sugar_map.txt' file
        '''

        map_i = 0
        for cell in self.grid.coord_iter():
            x = cell[1]
            y = cell[2]
            uid = 's'+str(y)+str(x)
            # patch = SugarPatch(uid, (x,y), 3)
            patch = SugarPatch(uid, (x,y), self.map[map_i])
            self.grid.place_agent(patch, (x,y))
            self.schedule.add(patch)
            map_i += 1

    def collect_wealth(self, agent):
        '''Method for datacollector'''
        if isinstance(agent, ScapeAgent):
            return agent.wealth

    def collect_metabolism(self, agent):
        '''Method for datacollector'''
        if isinstance(agent, ScapeAgent):
            return agent.metabolism

    def collect_vision(self, agent):
        '''Method for datacollector'''
        if isinstance(agent, ScapeAgent):
            return agent.vision


class RandomActivationByType(RandomActivation):
    '''
    A scheduler which activates each type of agent once per step, in random
    order, with the order reshuffled every step.
    This is equivalent to the NetLogo 'ask breed...' and is generally the
    default behavior for an ABM.
    Assumes that all agents have a step(model) method.
    '''
    agents_by_type = defaultdict(list)

    def __init__(self, model):
        super().__init__(model)
        self.agents_by_type = defaultdict(list)

    def add(self, agent):
        '''
        Add an Agent object to the schedule
        Args:
            agent: An Agent to be added to the schedule.
        '''

        self.agents.append(agent)
        agent_class = type(agent)
        self.agents_by_type[agent_class].append(agent)

    def remove(self, agent):
        '''
        Remove all instances of a given agent from the schedule.
        '''

        while agent in self.agents:
            self.agents.remove(agent)

        agent_class = type(agent)
        while agent in self.agents_by_type[agent_class]:
            self.agents_by_type[agent_class].remove(agent)

    def step(self, by_type=True, type_order=[]):
        '''
        Executes the step of each agent breed, one at a time, in random order.
        Args:
            by_breed: If True, run all agents of a single breed before running
                      the next one.
        '''
        if by_type:
            if len(type_order) != 0:
                order = type_order
            else:
                order = self.agents_by_type

            for agent_class in order:
                self.step_type(agent_class)

            self.steps += 1
            self.time += 1
        else:
            super().step()

    def step_type(self, agent_type):
        '''
        Shuffle order and run all agents of a given breed.
        Args:
            breed: Class object of the breed to run.
        '''
        agents = self.agents_by_type[agent_type]
        random.shuffle(agents)
        for agent in agents:
            agent.step(self.model)

    def get_type_count(self, type_class):
        '''
        Returns the current number of agents of certain breed in the queue.
        '''
        return len(self.agents_by_type[type_class])