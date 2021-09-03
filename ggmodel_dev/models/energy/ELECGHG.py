from ggmodel_dev.graphmodel import GraphModel
from ggmodel_dev.utils import get_model_properties


ELECGHG_nodes = {
            'ELECGHGi': {'type': 'output',
                      'unit': 'tonnes',
                      'name': 'CO2 emissions per electric plant',
                      'computation': lambda EFELECGHGi, ELECPRODi, **kwargs: 3.6 * ELECPRODi * EFELECGHGi
                        },
             'EFELECGHGi': {'type': 'input',
                      'unit': 'CO2 / TJ',
                      'name': 'CO2 emissions per TJ per fuel'
                      },
            'ELECPRODi': {'type': 'input',
                      'unit':  'GWh',
                      'name': 'Electricity production per electric plant'
                      },
             }

ELECGHG_model = GraphModel(ELECGHG_nodes)

# Dictionnary for easier access in the interface
model_dictionnary = {'ELECGHG_model': ELECGHG_model}

model_properties = get_model_properties('models/energy/ELECGHG_properties.json')