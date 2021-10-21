from ggmodel_dev.graphmodel import GraphModel, concatenate_graph_specs
from ggmodel_dev.utils import get_model_properties


GAS_nodes = {
    'GASCAPACITY': {
        'type': 'input',
        'name': 'Gas cumulative capacity',
        'unit':'GW',
    },
    'GASCAPFACTOR': {
        'type': 'input',
        'name': 'Gas capacity factor',
        'unit':'%'
    },
    'GASSUPPLY':{
        'type': 'input',
        'name': 'Gas supply',
        'unit':'GW'
    },
    'GASGENERATION':{
        'type': 'input',
        'name': 'Fuel required',
        'unit': 'TWh'
    },
    'GASEMISSIONSi':{
        'type': 'input',
        'name': 'C02, CH4, NO2 emissions',
        'unit': 'Mt CO2eq'
    },
    'GASLAND':{
        'type': 'input',
        'name': 'Gas land requirement',
        'unit': 'ha'
    }
}

COAL_nodes = {
    'COALCAPACITY':{
        'type': 'input',
        'name': 'Coal cumulative capacity',
        'unit':'GW',
    },
    'COALEMISSIONSi':{
        'type': 'input',
        'name': 'C02, CH4, NO2 emissions',
        'unit': 'Mt CO2eq'
    },
    'COALLAND':{
        'type': 'input',
        'name': 'Solar PV land requirement',
        'unit': 'ha'
    }
}

SOLAR_nodes = {
    'SOLARCAPACITY':{
        'type': 'input',
        'name': 'Solar cumulative capacity',
        'unit':'GW',
    },
    'SOLARCAPFACTOR': {
        'type': 'input',
        'name': 'Solar capacity factor',
        'unit':'%'
    },
    'SOLARSUPPLY':{
        'type': 'input',
        'name': 'Solar supply',
        'unit':'GW'
    },
    'SOLARGENERATION':{
        'type': 'input',
        'name': 'Solar generation',
        'unit': 'TWh'   
    },
    'SOLARLAND':{
        'type': 'input',
        'name': 'Solar PV land requirement',
        'unit': 'ha'
    }
}

SUPPLY_nodes = concatenate_graph_specs([SOLAR_nodes, COAL_nodes, GAS_nodes])

SUPPLY_model = GraphModel(SUPPLY_nodes)


# Dictionnary for easier access in the interface
model_dictionnary = {'SUPPLY_model': SUPPLY_model}

model_properties = get_model_properties('models/energy/SUPPLY_properties.json')