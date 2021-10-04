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
    'NPROTINTAKE':{
        'type': 'variable',
        'name': 'National protein consumption',
        'unit':'g/capita/day',
        'computation': lambda NPROTCONTENT, GDPCPPP, **kwargs: NPROTCONTENT.min() + (NPROTCONTENT.max() - NPROTCONTENT.max()) * (GDPCPP / GDPCPP.max()) ** (1/3) # TO CLARIFY ! 
    },
    'NPROTCONTENT':{
        'type': 'input',
        'name': 'National protein consumption',
        'unit':'g/capita/day'
    },
    'OOCYSTEXCRRATE':{
      'type': 'input',
      'unit': 'oocyst/capita/day',
      'name': 'Average Oocyst Excretion Rate'
    },
    'CRYPTOCONSEW':{
        'type': 'variable',
        'unit': 'oocyst',
        'name': 'Crypto pollution input from connected sewage network',
        'computation': lambda OOCYSTEXCRRATE, SEWSYSPOPi, WASTEWATTREATEFF, **kwargs: (1 - WASTEWATTREATEFF) * OOCYSTEXCRRATE * SEWSYSPOPi
    },
    'NHUMEMI': {
        'type': 'variable',
        'name': 'Human nitrogen emissions',
        'unit': 'kg/capita',
        'computation': lambda NPROTINTAKE, **kwargs: 0.356 * NPROTINTAKE
    },
    'PHUMANEMI':{
        'type': 'variable',
        'name': 'Human phosphorous emissions',
        'unit': 'kg/capita',
        'computation': lambda NHUMEMI, **kwargs: 1/6 * NHUMEMI
    },
    'PCONSEW':{
        'type': 'variable',
        'name': 'Phosphorous pollution from connected sewage network',
        'unit': 'kg',
        'computation': lambda PHUMANEMI, SEWSYSPOPi, WASTEWATTREATEFF, **kwargs: (1 - WASTEWATTREATEFF) * PHUMANEMI * SEWSYSPOPi
    },
    'NCONSEW':{
        'type': 'variable',
        'name': 'Nitrogen pollution from connected sewage network',
        'unit': 'kg',
        'computation': lambda SEWSYSPOPi, NHUMEMI, WASTEWATTREATEFF, **kwargs:WASTEWATTREATEFF *  NHUMEMI * SEWSYSPOPi
    },
    'NOPENDEFF':{
        'type': 'variable',
        'name': 'Nitrogen pollution from open defecation',
        'unit': 'kg',
        'computation': lambda NHUMEMI, OPENDEFPOPi, **kwargs: NHUMEMI *  OPENDEFPOPi
    },
    'POPENDEFF':{
        'type': 'input',
        'name': 'Phosphorous pollution from open defecation',
        'unit': 'kg'
    },
    'PRIVER':{
        'type': 'variable',
        'name': 'Phosphorous pollution to river system',
        'unit': 'kg',
        'computation': lambda POPENDEFF, PCONSEW, **kwargs: PCONSEW + POPENDEFF
    },
    'NRIVER':{
        'type': 'variable',
        'name': 'Nitrogen pollution to river system',
        'unit': 'kg',
        'computation': lambda NOPENDEFF, NCONSEW, **kwargs: NOPENDEFF + NCONSEW
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
    'CRYPTOLOAD': {
        'type': 'variable',
        'name': 'Crypto emissions load per basin area',
        'unit': 'oocyst/km2',
        'computation': lambda CRYTPOEM, BASINAREAi, **kwargs: CRYTPOEM / BASINAREAi
    },
    'CRYTPOEM':{
        'type': 'variable',
        'name': 'Crypto pollution from sanitation sources',
        'unit': 'oocyst',
        'computation': lambda CRYPTOSEWSYS, CRYPTOURDDIRECT, CRYPTORURINDIRECT, CRYPTORURDIFF, **kwargs: CRYPTOSEWSYS + CRYPTOURDDIRECT + CRYPTORURINDIRECT + CRYPTORURDIFF
    },
    'CRYPTOSEWSYS':{
        'type': 'input',
        'name': 'Crypto pollution from connected to sewage system',
        'unit': 'oocyst'
    },
    'CRYPTOURDDIRECT':{
        'type': 'input',
        'name': 'Crypto pollution input from urban direct sources',
        'unit': 'oocyst'
    },
    'CRYPTORURINDIRECT': {
        'type': 'input',
        'name': 'Crypto pollution input from rural direct sources',
        'unit': 'oocyst',
    },
    'CRYPTORURDIFF':{
        'type': 'input',
        'name': 'Crypto pollution input from rural diffuse sources',
        'unit': 'oocyst'
    }
}

# models
WATERQUAL_model = GraphModel(WATERQUAL_nodes)



# Dictionnary for easier access in the interface
model_dictionnary = {'WATERQUAL_model': WATERQUAL_model}

model_properties = get_model_properties('models/water/WATERQUAL_properties.json')