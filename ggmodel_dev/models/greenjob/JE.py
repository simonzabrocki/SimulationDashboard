__author__ = 'Sarah'
__status__ = 'Pending Validation'

"""
TO DO.
"""
from ggmodel_dev.graphmodel import GraphModel, merge_models
from ggmodel_dev.utils import get_model_properties


VDMC_nodes = {'DEi': {'type': 'input',
                     'name': 'Domestic Extraction per material',
                     'unit': 'tonnes'},
              'IMPi': {'type': 'input', 'name': 'Imports per material', 'unit': 'tonnes'},
              'EXPi': {'type': 'input', 'name': 'Exports per material', 'unit': 'tonnes'},
              'DMCi': {'type': 'output',
                       'name': 'Domestic material consumption per material',
                       'unit': 'tonnes',
                       'computation': lambda DEi, IMPi, EXPi, **kwargs: DEi + IMPi - EXPi
                       }
              }


JE_nodes = {'DMCi': {'type': 'variable', 'name': 'Domestic material consumption per material', 'unit': 'tonnes'},
            'MI': {'type': 'input',
                   'name': 'Material Efficiency Improvement',
                   'unit': '%'},
            'APCi': {'type': 'parameter',
                   'name': 'Average Price per commodity',
                   'unit': '$/tonnes'},
            'EXWi': {'type': 'parameter',
                    'name': 'Export Weights',
                    'unit': '1'},
            'CMi': {'type': 'variable',
                   'name': 'Cost per material',
                   'unit': '$/tonnes',
                   'computation': lambda APCi, EXWi, **kwargs: APCi * EXWi
                  },
            'TMS': {'type': 'variable',
                    'name': 'Monetary Savings',
                    'unit': '$',
                    'computation': lambda MI, DMCi, CMi, **kwargs: MI * (DMCi * CMi).groupby(['ISO', 'Year']).sum()
                   },
            'AW': {'type': 'parameter', 'name': 'Average Wage', 'unit': '$'
                  },
            'JE': {'type': 'output',
                   'name': 'Job Equivalents',
                   'unit': '1',
                   'computation': lambda TMS, AW, **kwargs: TMS / AW
                  }
           }

VDMC_model = GraphModel(VDMC_nodes)
JE_model_partial = GraphModel(JE_nodes)

JE_model = merge_models([JE_model_partial, VDMC_model])

model_dictionnary = {
    'VDMC_model': VDMC_model,
    'JE_model': JE_model
}