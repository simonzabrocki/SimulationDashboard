__author__ = 'Iris'
__status__ = 'Pending Validation'

"""
TO DO.
"""

from ggmodel_dev.graphmodel import GraphModel, concatenate_graph_specs
from ggmodel_dev.utils import get_model_properties

import numpy as np


VEHC_nodes = {
    'VEHC': {'type': 'output',
             'unit': 'vehicles per 1000 capita',
             'name': 'Vehicle ownership rate',
             'computation': lambda MAX_sat, VEHC_mid, VEHC_rate, GDPC, **kwargs:  MAX_sat * np.exp (-VEHC_mid * np.exp (-VEHC_rate * GDPC))
             },
    'MAX_sat': {'type': 'parameter', # Name to be changed ! 
              'unit': 'vehicles per 1000 capita',
              'name': 'max saturation level',
              },
    'VEHC_mid': {'type': 'parameter',
              'unit': '1',
              'name': 'Vehicle ownership halfway point'},

    'VEHC_rate': {'type': 'parameter',
             'unit': 'capita / constant 2010 US dollar',
             'name': 'Vehicle ownership growth rate'},

    'GDPC': {'type': 'input',
             'unit': 'constant 2010 US dollars per capita',
             'name': 'gross domestic product per capita'}
}

VEHC_model = GraphModel(VEHC_nodes)

model_dictionnary = {
    'VEHC_model': VEHC_model
}