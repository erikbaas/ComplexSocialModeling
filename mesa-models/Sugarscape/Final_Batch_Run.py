
# coding: utf-8

# In[16]:

from __future__ import division

import numpy as np
import pandas as pd
from Model import SugarscapeModel
from mesa.batchrunner import BatchRunner

from time import time


# In[12]:

def get_avg_pollution(model):
    '''Data collecting method to return total wealth of a model'''
    dc = model.datacollector
    m_data = dc.get_model_vars_dataframe()
    m_data = m_data.dropna()
    return m_data.describe().Wealth.iloc[1]

model_reporters = {"Wealth": get_avg_pollution}


# ### Create all parameter sets

# In[13]:

#This model has growth-affecting pollution and no inheritance
params_growth = {"height": 50,
          "width": 50,
          "init_agents": range(100,600,100),
          "max_metabolism": 3,
          "max_vision": 10,
          "max_init_sugar": 5,
          "min_age": 30,
          "max_age": 60,
          "init_poll": np.linspace(1,10, 10),
          "ex_ratio": np.linspace(1,100, 20),
          "poll_growth_rule": True,
          "inheritance_rule": False}

#This model has amenity-affecting pollution and no inheritance
params_amenity = {"height": 50,
          "width": 50,
          "init_agents": range(100,600,100),
          "max_metabolism": 3,
          "max_vision": 10,
          "max_init_sugar": 5,
          "min_age": 30,
          "max_age": 60,
          "ex_ratio": np.linspace(1,100, 20),
          "poll_growth_rule": False,
          "inheritance_rule": False}

#This model has growth_affecting pollution and inheritance
params_inh_growth = {"height": 50,
          "width": 50,
          "init_agents": range(100,600,100),
          "max_metabolism": 3,
          "max_vision": 10,
          "max_init_sugar": 5,
          "min_age": 30,
          "max_age": 60,
          "init_poll": np.linspace(1,10, 10),
          "ex_ratio": np.linspace(1,100, 20),
          "poll_growth_rule": True,
          "inheritance_rule": True}

#This model has amenity_affecting pollution and inheritance
params_inh_amenity = {"height": 50,
          "width": 50,
          "init_agents": range(100,600,100),
          "max_metabolism": 3,
          "max_vision": 10,
          "max_init_sugar": 5,
          "min_age": 30,
          "max_age": 60,
          "init_poll": np.linspace(1,10, 10),
          "ex_ratio": np.linspace(1,100, 20),
          "poll_growth_rule": False,
          "inheritance_rule": True}


# ### Create Batch Runs With Specific Rule Sets

# In[26]:

sweep_growth = BatchRunner(SugarscapeModel,
                          params_growth,
                          iterations=10,
                          max_steps=300,
                          model_reporters=model_reporters)


sweep_amenity = BatchRunner(SugarscapeModel,
                            params_amenity,
                            iterations=10,
                            max_steps=300,
                            model_reporters=model_reporters)

sweep_inh_growth = BatchRunner(SugarscapeModel,
                          params_inh_growth,
                          iterations=10,
                          max_steps=300,
                          model_reporters=model_reporters)

sweep_inh_amenity = BatchRunner(SugarscapeModel,
                          params_inh_amenity,
                          iterations=10,
                          max_steps=300,
                          model_reporters=model_reporters)


# ### Sweep and store all data

# In[30]:

def sweep_store(batchrunner, name):
    start = time()
    batchrunner.run_all()
    data = batchrunner.get_model_vars_dataframe()
    data.to_csv('Data/' + name + '.csv')
    end = time()
    print('Finished sweep: ' + name + str(end-start))


sweep_store(sweep_growth, 'growth')
sweep_store(sweep_amenity, 'amenity')
sweep_store(sweep_inh_growth, 'inh_growth')
sweep_store(sweep_inh_amenity, 'inh_amenity')


# In[ ]:



