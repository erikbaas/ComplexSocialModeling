from __future__ import division

from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import CanvasGrid, ChartModule, TextElement
from mesa.visualization.TextVisualization import (TextData, TextGrid, TextVisualization)

from Model import SchellingModel

class HappyElement(TextElement):
    '''Display a count of how many happy agents there are'''
    def __init__(self):
        pass

    def render(self, model):
        return 'Happy agents: ' + str(model.happy)

class SegregatedElement(TextElement):
    '''Display the average segregation of each agent'''
    def __init__(self):
        pass

    def render(self, model):
        return 'Average Segregation: ' + str(model.segregated)

def schelling_draw(agent):

    if agent is None:
        return

    portrayal = {'Shape': 'circle', 'r': .5, 'Filled': 'true', 'Layer': 0}

    if agent.group == 0:
        portrayal['Color'] = 'Red'
    elif agent.group == 1:
        portrayal['Color'] = 'Blue'
    else:
        portrayal['Color'] = 'Green'

    return portrayal

if __name__ == '__main__':
    happy = HappyElement()
    segregated = SegregatedElement()
    canvas = CanvasGrid(schelling_draw, 50, 50)
    happy_chart = ChartModule([{'Label': 'happy', 'Color':'Black'}])
    seg_chart = ChartModule([{'Label': 'segregated', 'Color':'Blue'}])
    server = ModularServer(SchellingModel, [canvas, happy, segregated, happy_chart, seg_chart], 'Schelling', 50, 50)
    server.launch()