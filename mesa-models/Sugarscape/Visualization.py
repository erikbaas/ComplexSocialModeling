from __future__ import division

from math import log
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import CanvasGrid, ChartModule

from Model import SugarscapeModel
from Agents import SugarPatch, ScapeAgent

def scape_draw(agent, model):
    '''Draw method for CanvasGrid'''

    # sugar_dict = ['Yellow', 3:'Gold', 2:'Orange', 1:'DarkOrange', 0:'White'}
    sugar_color = ['White', 'DarkOrange', 'Orange', 'Gold', 'Yellow']
    poll_color = ['White', ]

    if agent is None:
        portrayal = {'Shape':'circle', 'r':1, 'Filled':'true', 'Layer':0, 'Color':'Black'}

    if type(agent) is SugarPatch:
        portrayal = {'Shape':'rect', 'w':1, 'h':1, 'Filled':'true','Layer':0}
        # portrayal['Color'] = sugar_color[agent.sugar]
        if agent.pollution > 80:
            portrayal['Color'] = 'Black'
        elif agent.pollution > 35:
            portrayal['Color'] = 'Red'
        elif  agent.pollution > 18:
            portrayal['Color'] = 'DarkOrange'
        elif agent.pollution > 5:
            portrayal['Color'] = 'Orange'
        elif agent.pollution > 0:
            portrayal['Color'] = 'Yellow'
        else:
            portrayal['Color'] = 'White'

    if type(agent) is ScapeAgent:
        portrayal = {'Shape':'circle', 'r':log(agent.wealth,model.total_wealth), 'Filled':'true', 'Layer':1}
        if agent.wealth <= 0:
            portrayal['Color'] = 'Red'
        else:
            portrayal['Color'] = 'Green'

    return portrayal

if __name__=='__main__':
    canvas_element = CanvasGrid(scape_draw, 50, 50, 500, 500)
    agent_count = ChartModule([{'Label':'Pollution', 'Color':'Black'}])
    server = ModularServer(SugarscapeModel, [canvas_element, agent_count], 'Sugarscape')
    server.launch()