__author__ = 'Sarah P. Gerrard'
__status__ = 'Pending Validation'

"""
TO DO.
"""


from ggmodel_dev.graphmodel import GraphModel
from ggmodel_dev.utils import get_model_properties

WATERQUAL_nodes = {
    'PROTINTAKE':{
        'type': 'input',
        'name': 'National protein consumption',
        'unit':'g/capita/day',
    },
    'GDPC_PPP':{
        'type': 'input',
        'name': 'Gross domestic product per capita purchasing power parity',
        'unit': '$/capita'
    },
    'PROTINTAKE_min':{
        'type': 'variable',
        'name': 'Minimum protein consumption',
        'unit':'g/capita/day',
        'computation': lambda PROTINTAKE, **kwargs: PROTINTAKE.groupby(['Year']).max()
    },
    'PROTINTAKE_max':{
        'type': 'variable',
        'name': 'Maximum protein consumption',
        'unit':'g/capita/day',
        'computation': lambda PROTINTAKE, **kwargs: PROTINTAKE.groupby(['Year']).min()
    },
    'GDPC_PPP_max':{
        'type': 'variable',
        'name': 'Maximum gross domestic product per capita purchasing power parity',
        'unit': '$/capita',
        'computation': lambda GDPC_PPP, **kwargs: GDPC_PPP.groupby(['Year']).max()
    },
    'NHUMEMI':{
        'type': 'variable',
        'name': 'Human nitrogen emissions',
        'unit': 'kg/capita',
        'computation': lambda GDPC_PPP_max, PROTINTAKE_max, PROTINTAKE_min, GDPC_PPP, **kwargs: 0.365 * 0.16 * (PROTINTAKE_min + (PROTINTAKE_max - PROTINTAKE_min) * (GDPC_PPP / GDPC_PPP_max) ** (0.3))
    },
    'PHUMANEMI':{
        'type': 'variable',
        'name': 'Human phosphorous emissions',
        'unit': 'kg/capita',
        'computation': lambda NHUMEMI, **kwargs: 1/6 * NHUMEMI
    },
    'CRYPTOEXCR':{
        'type': 'input',
        'unit': 'oocyst',
        'name': 'Crypto emissions',
    },
    'POP_grid_san':{
        'type': 'input',
        'unit': 'capita',
        'name': 'Population per sanitation type per grid'
    },
    'POP_grid_con':{
        'type': 'variable',
        'unit': 'capita',
        'name': 'Population connected to sewage per sanitation type per grid',
        'computation': lambda POP_grid_san, **kwargs: POP_grid_san.loc[:, :, :, :,  ['Sewer connections'], :]
    },
    'POP_grid_noncon':{
        'type': 'variable',
        'unit': 'capita',
        'name': 'Population not connected to sewage per sanitation type per grid',
        'computation': lambda POP_grid_san, **kwargs: POP_grid_san.loc[:, :, :, :,  ['Open defecation', 'Unimproved'], :]
    },
    'WATERPOLEMi':{
        'type': 'variable',
        'unit': 'kg or oocyst',
        'name': 'Water pollutant emissions per pollutant type',
        'computation': lambda CRYPTOEXCR, PHUMANEMI, NHUMEMI, **kwargs: pd.concat([CRYPTOEXCR, PHUMANEMI, NHUMEMI], keys=['cryptosporidium', 'phosphorus', 'nitrogen'], names=['pollutant'])

    }, 
    'WATERTREATEFFi':{
        'type': 'input',
        'name': 'Water treatment efficiency',
        'unit': '1',
    },
    'POLLUTEFFi': {
        'type': 'input',
        'name': 'Pollutant removal efficiency',
        'unit': '1'
    },
    'WASTEWATTREATEFFi':{
        'type': 'variable',
        'name': 'Pollutant removal efficiency of waste water treatment by pollutant',
        'unit': '1',
        'computation': lambda POLLUTEFFi, WATERTREATEFFi, **kwargs: (WATERTREATEFFi * POLLUTEFFi).groupby(['ISO', 'pollutant']).sum()
    },
    'WATPOL_con':{
        'type': 'variable',
        'name': 'Pollution from connected sewage',
        'unit': 'kg or oocyst',
        'computation': lambda WASTEWATTREATEFFi, WATERPOLEMi, POP_grid_con, **kwargs: ((1 - WASTEWATTREATEFFi) * WATERPOLEMi * POP_grid_con).dropna()
    },
    'WATPOL_noncon':{
        'type': 'variable',
        'name': 'Pollution from non connected sewage',
        'unit': 'kg or oocyst',
        'computation': lambda WATERPOLEMi, POP_grid_noncon, **kwargs: (WATERPOLEMi * POP_grid_noncon).dropna()
    },
}

# models
WATERQUAL_model = GraphModel(WATERQUAL_nodes)


# Dictionnary for easier access in the interface
model_dictionnary = {'WATERQUAL_model': WATERQUAL_model}

model_properties = get_model_properties('models/water/WATERQUAL_properties.json')