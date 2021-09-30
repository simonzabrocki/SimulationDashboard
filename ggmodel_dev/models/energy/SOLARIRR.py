from ggmodel_dev.graphmodel import GraphModel, concatenate_graph_specs
from ggmodel_dev.utils import get_model_properties

rho_water = 997
g = 9.81

SOLARIRR_nodes = {
   'IWR': {'type': 'input',
                     'name': ' Irrigation Water Requirement',
                     'unit': '1e9 m3/year',
                     },
    'SOLARPUMPNRJ':{
        'type': 'variable',
        'unit': 'kWh/year',
        'name': 'Energy required for solar pumping',
        'computation': lambda IWR, WATERDEPTH, PUMPEFF, SOLARPANELEFF, **kwargs: (1e9 * IWR * rho_water * g * WATERDEPTH) / (3.6e6 * SOLARPANELEFF * PUMPEFF)
    },
    'SOLARPUMPPOW':{
        'type': 'variable',
        'unit': 'kW/year',
        'name': 'Solar power required for pumping',
        'computation': lambda SOLARPUMPNRJ, SUNDUR, **kwargs: SOLARPUMPNRJ / SUNDUR
    },
    'SOLARSURF':{
        'type': 'variable',
        'unit': 'm2',
        'name': 'Solar Panel surface',
        'computation': lambda SOLARPUMPNRJ, SOLARIRRAD, **kwargs: SOLARPUMPNRJ / SOLARIRRAD  
    },
    'WATERDEPTH':{
        'type': 'input',
        'unit': 'm',
        'name': 'Water depth level'
    },
    'SOLARIRRAD':{
        'type': 'input',
        'unit': 'kWh/m2/year',
        'name': 'Yearly solar irradiation'
    },
    'SUNDUR':{
        'type': 'input',
        'unit': 'h / year',
        'name': 'Sunshine duration'
    },
    'PUMPEFF':{
        'type': 'input',
        'unit': '1',
        'name': 'Pump efficiency'
    },
    'SOLARPANELEFF':{
        'type': 'input',
        'unit': '1',
        'name': 'Solar panel efficiency'
    }
}

SOLARIRR_model = GraphModel(SOLARIRR_nodes)

# Dictionnary for easier access in the interface
model_dictionnary = {'SOLARIRR_model': SOLARIRR_model}

model_properties = get_model_properties('models/energy/SOLARIRR_properties.json')
