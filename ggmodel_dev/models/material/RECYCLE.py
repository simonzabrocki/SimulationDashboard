from ggmodel_dev.graphmodel import GraphModel, concatenate_graph_specs
from ggmodel_dev.utils import get_model_properties
import pandas as pd
from scipy.stats import norm
import numpy as np



def compute_LDi(LDi_mu, LDi_std, INFLOWi, year):

    LDi = pd.concat([
        LDi_mu.to_frame(name='mu_'),
        LDi_std.to_frame(name='std_')
    ],axis=1).reset_index().rename(columns={'index': 'Item'})
    
    dt = (
        INFLOWi.reset_index()[['Item', 'Year']]
                         .drop_duplicates()
    )    

    dt['Value'] = year - dt['Year']
    dt = dt.set_index(['Item', 'Year']).Value
    
    compute_df = dt.to_frame(name='dt').reset_index().merge(LDi, on='Item')
    LDi = norm.pdf(compute_df.dt.values, loc=compute_df.mu_.values, scale=compute_df.std_.values)
    return pd.Series(LDi, index=dt.index)


SBMi_nodes={
    'PLOSSi': {'type': 'parameter', 
               'unit': '1',
               'name': 'Processing Losses per material'
           },
    'DMCi': {'type': 'input',
             'unit': 'Tonnes',
             'name': 'Domestic Material Consumption per material'
             },
    'SBMi': {'type': 'variable',
           'unit': 'tonnes',
           'name': 'Stock Building Materials per material',
           'computation': lambda DMCi, PLOSSi, **kwargs: DMCi * PLOSSi
           }
}


RECYCLE_nodes = {
    'PLOSSi': {'type': 'parameter', 
               'unit': '1',
               'name': 'Processing Losses per material'
           },
    'DMCi': {'type': 'input',
             'unit': 'tonnes',
             'name': 'Domestic Material Consumption per material'
             },
    'MLOSSi': {'type': 'parameter', 
           'unit': '1',
           'name': 'Manufacturing Losses'
           },
    'SBMi': {'type': 'variable',
           'unit': 'tonnes',
           'name': 'Stock Building Materials per material',
           'computation': lambda DMCi, PLOSSi, **kwargs: DMCi * (1 - PLOSSi)
           },
    'RMSi_t_minus_1': {'type': 'input',
                       'unit': 'tonnes',
                       'name': 'Recycled Material Stock previous year',
                 },
    'INFLOWi': {'type': 'variable',
            'unit': 'tonnes',
            'name': 'Material Inflow per material',
            'computation': lambda SBMi, MLOSSi, RMSi_t_minus_1,  **kwargs: (SBMi +  RMSi_t_minus_1) * (1 - MLOSSi)
            },
    'LDi_mu': {'type': 'input',
                'unit': '1',
                'name': 'Lifetime Distribution Function mean per material'
                  },
    'LDi_std': {'type': 'input', 
                'unit': '1',
                'name': 'Lifetime Distribution Function standard deviation per material'
                  },
    'LDi': {'type': 'variable',
                'unit': '1',
                'name': 'Lifetime Distribution Function per material',
                'computation': lambda INFLOWi, LDi_std, LDi_mu, year, **kwargs: compute_LDi(LDi_mu, LDi_std, INFLOWi, year) 
                  },
    'OUTFLOWi': {'type': 'variable', 
            'unit': 'tonnes', 
            'name': 'Material outflow per material',
            'computation': lambda INFLOWi, LDi, **kwargs: (INFLOWi * LDi).groupby(['ISO', 'Item']).sum()
            },
    'RRi': {'type': 'parameter',
            'unit': '1',
            'name': 'Recycling Rate'
              },    
    'RMSi': {'type': 'variable',
                 'unit': 'tonnes',
                 'name': 'Recycled Material Stock per material',
                 'computation': lambda OUTFLOWi, RRi, **kwargs: OUTFLOWi * RRi
                 },
    'WASTEi': {'type': 'output',
              'unit': 'tonnes',
              'name': 'Material Waste to Landfill per material',
              'computation': lambda OUTFLOWi, RMSi, **kwargs: OUTFLOWi - RMSi
              },
    'year': {
        'type': 'input',
        'unit': 'year',
        'name': 'current year'
    }
}

MS_nodes = {
    'OUTFLOWi': {'type': 'input', 
            'unit': 'tonnes', 
            'name': 'Material outflow per material',
            },
    'INFLOWi': {'type': 'input',
            'unit': 'tonnes',
            'name': 'Material Inflow per material',
            },
    'delta_MSi': {'type': 'variable', 
            'unit': 'tonnes', 
            'name': 'Material Stock variation per material',
            'computation': lambda INFLOWi, OUTFLOWi, **kwargs: (INFLOWi - OUTFLOWi)
            },
    'MSi':{'type': 'variable', 
            'unit': 'tonnes', 
            'name': 'Material Stock per material',
            'computation': lambda delta_MSi, **kwargs: (delta_MSi).groupby(['ISO', 'Item']).cumsum().reorder_levels(order=["ISO", 'Item', "Year"])
            },
}

RECYCLE_model = GraphModel(RECYCLE_nodes)
SBMI_model = GraphModel(SBMi_nodes)
MS_model = GraphModel(MS_nodes)
MUE_model = GraphModel(concatenate_graph_specs([RECYCLE_nodes, SBMi_nodes, MS_nodes]))

model_dictionnary = {
    'SBMi_model': SBMI_model,
    'RECYCLE_model': RECYCLE_model,
    'MS_model': MS_model,
    'MUE_model': MUE_model
}

model_properties = get_model_properties('models/material/RECYCLE_properties.json')

