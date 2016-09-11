import random

from mesa import Model, Agent
from mesa.time import RandomActivation
from mesa.space import SingleGrid
from mesa.datacollection import DataCollector


class SchellingAgent(Agent):
    '''
    Schelling segregation agent
    '''
    def __init__(self, pos, model, agent_type):
        '''
         Create a new Schelling agent.

         Args:
            unique_id: Unique identifier for the agent.
            x, y: Agent initial location.
            agent_type: Indicator for the agent's type (minority=1, majority=0)
        '''
        super().__init__(pos, model)
        self.pos = pos
        self.a_type = agent_type
        self.model = model

    def step(self):
        similar = 0
        near = {self.a_type: 1}

        for neighbor in self.model.grid.neighbor_iter(self.pos):
            a_type = neighbor.a_type
            if a_type in near:
                near[a_type] += 1
            else:
                near[a_type] = 1

        print(near, )

        if (near[self.a_type]) >= max(near.values()):
            self.model.happy += 1
        else:
            self.model.grid.move_to_empty(self)


class SchellingModel(Model):
    '''
    Model class for the Schelling segregation model.
    '''

    def __init__(self, height, width, density, type_pcs=[.2, .2, .2, .2, .2]):
        '''
        '''

        self.height = height
        self.width = width
        self.density = density
        self.type_pcs = type_pcs

        self.schedule = RandomActivation(self)
        self.grid = SingleGrid(height, width, torus=False)

        self.happy = 0
        self.datacollector = DataCollector(
            {"happy": lambda m: m.happy},  # Model-level count of happy agents
            # For testing purposes, agent's individual x and y
            {"x": lambda a: a.pos[0], "y": lambda a: a.pos[1]})

        self.running = True

        # Set up agents
        # We use a grid iterator that returns
        # the coordinates of a cell as well as
        # its contents. (coord_iter)

        total_agents = self.height * self.width * self.density
        agents_by_type = [total_agents*val for val in self.type_pcs]

        for loc, types in enumerate(agents_by_type):
            for i in range(int(types)):
                pos = self.grid.find_empty()
                agent = SchellingAgent(pos, self, loc)
                self.grid.position_agent(agent, pos)
                self.schedule.add(agent)

    def step(self):
        '''
        Run one step of the model. If All agents are happy, halt the model.
        '''
        self.happy = 0  # Reset counter of happy agents
        self.schedule.step()
        self.datacollector.collect(self)

        if self.happy == self.schedule.get_agent_count():
            self.running = False
