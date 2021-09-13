from ggmodel_dev.graphmodel import GraphModel
from ggmodel_dev.utils import get_model_properties
import pandas as pd
from scipy.stats import norm


def compute_LDi(LDi_mu, LDi_std, INFLOWi):

    LDi = pd.concat([
        LDi_mu.to_frame(name='mu_'),
        LDi_std.to_frame(name='std_')
    ],axis=1).reset_index().rename(columns={'index': 'Item'})
    
    dt = (
        INFLOWi.reset_index()[['Item', 'Year']]
                         .drop_duplicates()
    )

    current_year = max(INFLOWi.index.get_level_values('Year'))
    

    dt['Value'] = current_year - dt['Year']
    dt = dt.set_index(['Item', 'Year']).Value
    
    compute_df = dt.to_frame(name='dt').reset_index().merge(LDi, on='Item')
    LDi = norm.pdf(compute_df.dt.values, loc=compute_df.mu_.values, scale=compute_df.std_.values)
    return pd.Series(LDi, index=dt.index)


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
           'computation': lambda DMCi, PLOSSi, **kwargs: DMCi * PLOSSi
           },
    'RMSi_t_minus_1': {'type': 'input',
                       'unit': 'tonnes',
                       'name': 'Recycled Material Stock previous year',
                 },
    'INFLOWi': {'type': 'variable',
            'unit': 'tonnes',
            'name': 'Material Inflow per material',
            'computation': lambda SBMi, MLOSSi, RMSi_t_minus_1,  **kwargs: (SBMi + RMSi_t_minus_1) * MLOSSi
            },
    'LDi_mu': {'type': 'input', ##pre-calculate for aggregated metals and non-metals
                'unit': '1',
                'name': 'Lifetime Distribution Function mean per material'
                  },
    'LDi_std': {'type': 'input', ##pre-calculate for aggregated metals and non-metals
                'unit': '1',
                'name': 'Lifetime Distribution Function standard deviation per material'
                  },
    'LDi': {'type': 'variable', ##pre-calculate for aggregated metals and non-metals
                'unit': '1',
                'name': 'Lifetime Distribution Function per material',
                'computation': lambda INFLOWi, LDi_std, LDi_mu, **kwargs: compute_LDi(LDi_mu, LDi_std, INFLOWi) 
                  },
    'DMSi': {'type': 'variable', 
            'unit': 'tonnes', 
            'name': 'Discarded Material Stock per material',
            'computation': lambda INFLOWi, LDi, **kwargs: (INFLOWi * LDi).groupby('ISO').cumsum().reorder_levels(order=["ISO", 'Item', "Year"])
            },
    'RRi': {'type': 'parameter',
            'unit': '1',
            'name': 'Recycling Rate'
              },    
    'RMSi': {'type': 'variable',
                 'unit': 'tonnes',
                 'name': 'Recycled Material Stock',
                 'computation': lambda DMSi, RRi, **kwargs: DMSi * RRi
                 },
    'WASTEi': {'type': 'output',
              'unit': 'tonnes',
              'name': 'Material Waste to Landfill per material',
              'computation': lambda DMSi, RMSi, **kwargs: DMSi - RMSi
              }
}

RECYCLE_model = GraphModel(RECYCLE_nodes)


model_dictionnary = {"RECYCLE_model": RECYCLE_model}

model_properties = get_model_properties('models/material/RECYCLE_properties.json')