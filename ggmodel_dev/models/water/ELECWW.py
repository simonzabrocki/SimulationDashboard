from ggmodel_dev.graphmodel import GraphModel
from ggmodel_dev.utils import get_model_properties


ELECWW_nodes = {'ELECWWi': {'type': 'output',
                      'unit': 'm3',
                      'name': 'Water withdrawal per electric plant',
                      'computation': lambda WWFUELCOOLi, ELECPRODi, **kwargs: ELECPRODi * WWFUELCOOLi
                        },
             'WWFUELCOOLi': {'type': 'input',
                      'unit': 'm3 / GWh',
                      'name': 'Water withdrawal intensity per fuel and cooling sytem'
                      },
            'ELECPRODi': {'type': 'input',
                      'unit':  'GWh',
                      'name': 'Electricity production per electric plant'
                      },
             }

ELECWW_model = GraphModel(ELECWW_nodes)

# Dictionnary for easier access in the interface
model_dictionnary = {'ELECWW_model': ELECWW_model}

model_properties = get_model_properties('models/water/ELECWW_properties.json')