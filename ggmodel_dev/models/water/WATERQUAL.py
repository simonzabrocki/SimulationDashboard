__author__ = 'Sarah P. Gerrard'
__status__ = 'Pending Validation'

"""
TO DO.
"""


from ggmodel_dev.graphmodel import GraphModel
from ggmodel_dev.utils import get_model_properties

WATERQUAL_nodes = {
    'OPENDEF': {
        'type': 'input',
        'unit': '%',
        'name': 'Fraction of open defection'
    },
    'Pop': {
        'type': 'input',
        'name': 'Population',
        'unit': 'capita'
    },
    'URBRUPOPi':{
        'type': 'input',
        'name': 'Population fraction per area',
        'unit': '1'
    },
    'OPENDEFPOPi':{
        'type': 'variable',
        'name': 'Population under open defecation',
        'unit': 'capita',
        'computation': lambda OPENDEF, URBRUPOPi, Pop, **kwargs: OPENDEF * URBRUPOPi * Pop
    },
    'SEWREMEFFi':{
        'type': 'input',
        'name': 'Removal efficiency in sewage system per pollutant',
        'unit': '1'
    },
    'WASTEWATTREATDISi':{
        'type': 'input',
        'name': 'Waste water treatment distribution',
        'unit': '1',
    },
    'WASTEWATTREATEFF':{
        'type': 'variable',
        'name': 'Pollutant removal efficiency of waste water treatment',
        'unit': '1',
        'computation': lambda SEWREMEFFi, WASTEWATTREATDISi, **kwargs: (WASTEWATTREATDISi * SEWREMEFFi).sum()
    },
    'CONSEWSYS':{
        'type': 'input',
        'name': 'Connection to sewage system',
        'unit': '%'
    },
    'SEWSYSPOPi':{
        'type': 'variable',
        'name': 'Population connected to sewage system',
        'unit': 'capita',
        'computation': lambda Pop, URBRUPOPi, CONSEWSYS, **kwargs:  Pop * URBRUPOPi * CONSEWSYS
    },
    'GDPCPPP':{
        'type': 'input',
        'name': 'Gross domestic product per capita purchasing power parity',
        'unit': '$/capita'
    },
    'PROTCONS':{
        'type': 'input',
        'name': 'National protein consumption',
        'unit':'g/capita/day'
    },
    'NHUMEMI': {
        'type': 'input',
        'name': 'Human nitrogen emissions',
        'unit': 'kg/capita'
    },
    'PHUMANEMI':{
        'type': 'input',
        'name': 'Human phosphorous emissions',
        'unit': 'kg/capita'
    },
    'PCONSEW':{
        'type': 'input',
        'name': 'Phosphorous pollution from connected sewage network',
        'unit': 'kg'
    },
    'NOPENDEFF':{
        'type': 'input',
        'name': 'Nitrogen pollution from open defecation',
        'unit': 'kg'
    },
    'POPENDEFF':{
        'type': 'input',
        'name': 'Phosphorous pollution from open defecation',
        'unit': 'kg'
    },
    'PRIVER':{
        'type': 'input',
        'name': 'Phosphorous pollution to river system',
        'unit': 'kg'
    },
    'NRIVER':{
        'type': 'input',
        'name': 'Nitrogen pollution to river system',
        'unit': 'kg'
    },
    'BASINAREAi':{
        'type': 'input',
        'name': 'Sub basin area per basin',
        'unit': 'km2'
    },
    'PLOADi':{
        'type': 'variable',
        'name': 'Phosphorous pollution per basin area',
        'unit': 'kg/km2',
        'computation': lambda BASINAREAi, PRIVER, **kwargs: PRIVER / BASINAREAi

    },
    'NLOADi':{
        'type': 'variable',
        'name': 'Nitrogen pollution per basin area',
        'unit': 'kg/km2',
        'computation': lambda BASINAREAi, NRIVER, **kwargs: NRIVER / BASINAREAi
    },
}

# models
WATERQUAL_model = GraphModel(WATERQUAL_nodes)



# Dictionnary for easier access in the interface
model_dictionnary = {'WATERQUAL_model': WATERQUAL_model}

model_properties = get_model_properties('models/water/WATERQUAL_properties.json')