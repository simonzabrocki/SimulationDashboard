from ggmodel_dev.graphmodel import GraphModel, concatenate_graph_specs
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


ELECWW_nodes = {'ELECWWi': {'type': 'output',
                      'unit': 'm3',
                      'name': 'Water withdrawal per electric plant',
                      'computation': lambda WWFUELCOOLi, ELECPRODi, **kwargs: (ELECPRODi * WWFUELCOOLi).reorder_levels(ELECPRODi.index.names)
                        },
             'WWFUELCOOLi': {'type': 'input',
                      'unit': 'm3 / GWh',
                      'name': 'water withdrawal intensity per fuel and cooling sytem'
                      },
            'ELECPRODi': {'type': 'input',
                      'unit':  'GWh',
                      'name': 'Electricity production per electric plant'
                      },
             }


ELEC_nodes = concatenate_graph_specs([ELECGHG_nodes, ELECWW_nodes])



ELECGHG_model = GraphModel(ELECGHG_nodes)
ELECWW_model = GraphModel(ELECWW_nodes)
ELEC_model = GraphModel(ELEC_nodes)

# Dictionnary for easier access in the interface
model_dictionnary = {'ELECGHG_model': ELECGHG_model,
                     'ELECWW_model': ELECWW_model,
                     'ELEC_model': ELEC_model}

model_properties = get_model_properties('models/energy/ELEC_properties.json')