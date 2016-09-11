from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import CanvasGrid, ChartModule, TextElement
from mesa.visualization.TextVisualization import (
    TextData, TextGrid, TextVisualization
)

from model import SchellingModel


class SchellingTextVisualization(TextVisualization):
    '''
    ASCII visualization for schelling model
    '''

    def __init__(self, model):
        '''
        Create new Schelling ASCII visualization.
        '''
        self.model = model

        # grid_viz = TextGrid(self.model.grid, self.ascii_agent)
        # happy_viz = TextData(self.model, 'happy')
        # self.elements = [grid_viz, happy_viz]

    # @staticmethod
    # def ascii_agent(a):
    #     '''
    #     Minority agents are X, Majority are O.
    #     '''
    #     if a.type == 0:
    #         return 'O'
    #     if a.type == 1:
    #         return 'X'


class HappyElement(TextElement):
    '''
    Display a text count of how many happy agents there are.
    '''
    def __init__(self):
        pass

    def render(self, model):
        return "Happy agents: " + str(model.happy)


def schelling_draw(agent):
    '''
    Portrayal Method for canvas
    '''
    if agent is None:
        return
    portrayal = {"Shape": "circle", "r": 0.5, "Filled": "true", "Layer": 0}

    if agent.a_type == 0:
        portrayal["Color"] = "Red"
    elif agent.a_type == 1:
        portrayal["Color"] = "Blue"
    elif agent.a_type == 2:
        portrayal["Color"] = "Green"
    elif agent.a_type == 3:
        portrayal["Color"] = "Yellow"
    elif agent.a_type == 4:
        portrayal["Color"] = "Orange"
    elif agent.a_type == 5:
        portrayal["Color"] = "Purple"
    elif agent.a_type == 6:
        portrayal["Color"] = "Black"
    elif agent.a_type == 7:
        portrayal["Color"] = "Brown"
    return portrayal

happy_element = HappyElement()
canvas_element = CanvasGrid(schelling_draw, 20, 20, 500, 500)
happy_chart = ChartModule([{"Label": "happy", "Color": "Black"}])
server = ModularServer(SchellingModel,
                       [canvas_element, happy_element, happy_chart],
                       "Schelling", 50, 50, 0.8, [.6, .2, .2])
server.launch()
