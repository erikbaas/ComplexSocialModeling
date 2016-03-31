from __future__ import division

from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import CanvasGrid, ChartModule

from Model import SugarscapeModel
from Agents import SugarPatch, ScapeAgent

def scape_draw(agent):
    # sugar_dict = ['Yellow', 3:'Gold', 2:'Orange', 1:'DarkOrange', 0:'White'}
    color_list = ['White', 'DarkOrange', 'Orange', 'Gold', 'Yellow']

    if agent is None:
        portrayal = {'Shape':'circle', 'r':1, 'Filled':'true', 'Layer':0, 'Color':'Black'}

    if type(agent) is SugarPatch:
        portrayal = {'Shape':'rect', 'w':1, 'h':1, 'Filled':'true','Layer':0}
        portrayal['Color'] = color_list[agent.sugar]

    if type(agent) is ScapeAgent:
        portrayal = {'Shape':'circle', 'r':.7, 'Filled':'true', 'Layer':1}
        if agent.wealth <= 0:
            portrayal['Color'] = 'Red'
        else:
            portrayal['Color'] = 'Green'

    return portrayal

if __name__=='__main__':
    canvas_element = CanvasGrid(scape_draw, 50, 50, 500, 500)
    agent_count = ChartModule([{'Label':'Agents', 'Color':'Black'}])
    server = ModularServer(SugarscapeModel, [canvas_element, agent_count], 'Sugarscape')
    server.launch()