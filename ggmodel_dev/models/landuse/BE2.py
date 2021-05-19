__author__ = 'Hermen'
__status__ = 'Pending Validation'

"""
TO DO.
"""
from ggmodel_dev.graphmodel import GraphModel, concatenate_graph_specs
from ggmodel_dev.utils import get_model_properties
import pandas as pd

# To check naming, confusing with demand/prod + total not total
kg_to_1000tonnes = 1e-6
day_per_year = 365
ktonnes_to_hg = 1e7

FPi_nodes = {'FLOi': {
    'type': 'input',
    'unit': '1000 tonnes',
    'name': 'Food losses per food group'
},
    'FDKGi': {
    'type': 'input',
    'unit': 'kg/capita/day',
    'name': 'Kg food demand per day per food group'
},
    'SSRi': {
    'type': 'input',
    'unit': '1',
    'name': 'Self-sufficiency ratio per food group',
},
    'FDPi': {
    'type': 'variable',
    'unit': '1000 tonnes',
    'name': 'Total food production per food group',
    'computation': lambda FDKGi, Pop, FLOi, **kwargs: kg_to_1000tonnes * day_per_year * FDKGi * Pop * 1e3 + FLOi
},
    'OFi': {
    'type': 'variable',
    'unit': '1000 tonnes',
    'name': 'Other food demand',
    'computation': lambda SDi, NFDi, PDi, RDi, SVi, **kwargs: SDi + NFDi + PDi + RDi + SVi
},
    'SDi': {
    'type': 'input',
    'unit': '1000 tonnes',
    'name': 'Seed demand per food group'
},
    'NFDi': {
    'type': 'input',
    'unit': '1000 tonnes',
    'name': 'Non-food demand per food group'
},
    'PDi': {
    'type': 'input',
    'unit': '1000 tonnes',
    'name': 'Processed demand per food group'
},
    'RDi': {
    'type': 'input',
    'unit': '1000 tonnes',
    'name': 'Residual demand per food group'
},
    'SVi': {
    'type': 'input',
    'unit': '1000 tonnes',
    'name': 'Stock variation per food group'
},
    'FPi': {
    'type': 'output',
    'name': 'Food production per food group',
    'unit': '1000 tonnes',
    'computation': lambda SSRi, OFi, FDi, FDPi, **kwargs: (OFi + FDi + FDPi) * SSRi
},
    'FDi': {
    'type': 'input',
    'unit': '1000 tonnes',
    'name': 'Feed demand per food group'
},
    'Pop': {
    'type': 'input',
    'unit': 'capita',
    'name': 'Population'
}
}

TCLDi_nodes = {'TCLDi': {
    'type': 'output',
    'name': 'Cropland demand',
    'unit': 'ha',
    'computation': lambda CYi, FPi, **kwargs: ktonnes_to_hg * FPi / CYi
},
    'CYi': {
    'type': 'input',
    'unit': 'hg/ha',
    'name': 'Crop yields per crop type'
},
    'FPi': {
    'type': 'input',
    'name': 'Food production per food group',
    'unit': '1000 tonnes'
},
}

CL_nodes = {'TCLDi': {
    'type': 'input',
    'name': 'Cropland demand',
    'unit': 'ha',
},
    'CL_corr_coef': {
    'type': 'input',
    'name': 'Correction coefficient',
    'unit': '1',
},
    'CL': {
    'type': 'output',
    'name': 'Cropland',
    'unit': '1000 ha',
    # Strange to check !
    'computation': lambda TCLDi, CL_corr_coef, **kwargs: TCLDi.groupby(level=['ISO', 'Year']).sum() * 1e-3 * CL_corr_coef
},
}

IL_FL_nodes = {'CL': {
    'type': 'input',
    'name': 'Cropland',
    'unit': '1000 ha',
},
    'CL_baseline': {
    'type': 'input',
    'name': 'Cropland stock baseline',
    'unit': '1000 ha',
},
    'delta_CL': {
    'type': 'variable',
    'name': 'Change in cropland',
    'unit': '1000 ha',
    'computation': lambda CL, CL_baseline, **kwargs: CL - CL_baseline
},
    'IL_baseline': {
    'type': 'input',
    'unit': '1000 ha',
    'name': 'Inactive land baseline'
},
    'FL_baseline': {
    'type': 'input',
    'unit': '1000 ha',
    'name': 'Forest land baseline'
},
    'IL': {
    'type': 'output',
    'name': 'Inactive land stock',
    'unit': '1000 ha',
    # to double check
    'computation': lambda delta_CL, IL_baseline, **kwargs: (IL_baseline - delta_CL).clip(lower=0)
},
    'FL': {
    'type': 'output',
    'name': 'Forest land stock',
    'unit': '1000 ha',
    # to double check
    'computation': lambda delta_CL, FL_baseline, IL_baseline, **kwargs: FL_baseline + (IL_baseline - delta_CL).clip(upper=0)
}
}

BE2_nodes = {'TLA': {
    'type': 'input',
    'unit': '1000 ha',
    'name': 'Total land area'
},
    'FL': {
    'type': 'input',
    'unit': '1000 ha',
    'name': 'Forest land stock'
},
    'IL': {
    'type': 'input',
    'unit': '1000 ha',
    'name': 'Inactive land stock'
},
    'R_rate': {
    'type': 'parameter',
    'unit': '%',
    'name': 'Rate of reforestation'
},
    'FL_RF': {
    'type': 'variable',
    'name': 'Forest land stock after reforestation policy',
    'unit': '1000 ha',
    'computation': lambda FL, R_rate, IL, **kwargs: FL + 1e-2 * R_rate * IL
},
    'BE2': {
    'type': 'output',
    'name': 'Share of forest area to total land area',
    'unit': '%',
    'computation': lambda FL_RF, TLA, **kwargs: 1e2 * FL_RF / TLA
}
}


FPi_model = GraphModel(FPi_nodes)
TCLDi_partial_model = GraphModel(TCLDi_nodes)
TCLDi_model = GraphModel(concatenate_graph_specs([TCLDi_nodes, FPi_nodes]))
IL_FL_model = GraphModel(IL_FL_nodes)
BE2_partial_model = GraphModel(BE2_nodes)
BE2_model = GraphModel(concatenate_graph_specs(
    [BE2_nodes, IL_FL_nodes, CL_nodes, TCLDi_nodes, FPi_nodes]))

model_dictionnary = {
    'TCLDi_model': TCLDi_model,
    'TCLDi_partial_model': TCLDi_model,
    'FPi_model': FPi_model,
    'IL_FL_model': IL_FL_model,
    'BE2_partial_model': BE2_partial_model,
    'BE2_model': BE2_model
}

model_properties = get_model_properties('models/landuse/BE2_properties.json')