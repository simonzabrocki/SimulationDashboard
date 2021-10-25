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
    'GASHOURS':{
        'type': 'input',
        'name': 'Gas generation time',
        'unit': 'hours'
    },
    'GASEFFICIENCY':{
        'type': 'input',
        'name': 'Gas conversion efficiency',
        'unit':'1'
    },
    'GASFUEL':{
        'type': 'variable',
        'name': 'Fuel required for gas generation',
        'unit': 'TWh',
        'computation': lambda GASCAPACITY, GASCAPFACTOR, GASHOURS, GASEFFICIENCY, **kwargs: GASCAPACITY  * GASCAPFACTOR * GASHOURS / GASEFFICIENCY
    },
    'GASEMFACTORi':{
        'type': 'input',
        'name': 'Gas emission factors',
        'unit': 'Mt CO2eq / TWh'
    },
    'GASEMISSIONSi':{
        'type': 'variable',
        'name': 'C02, CH4, NO2 emissions',
        'unit': 'Mt CO2eq',
        'computation': lambda GASEMFACTORi, GASFUEL, **kwargs: GASEMFACTORi * GASFUEL
    }, 
    'GASLANDREQ':{
        'type': 'input',
        'name': 'land requirement per GW of gas plant',
        'unit': 'ha / GW'
    },
    'GASLAND':{
        'type': 'variable',
        'name': 'Gas land requirement',
        'unit': 'ha',
        'computation': lambda GASLANDREQ, GASFUEL, **kwargs: GASLANDREQ * GASFUEL
    }
}

COAL_nodes = {
    'COALCAPACITY':{
        'type': 'input',
        'name': 'Coal cumulative capacity',
        'unit':'GW',
    },
    'COALGENERATION':{
        'type': 'variable',
        'name': 'Coal generation',
        'unit': 'TWh',
        'computation': lambda COALCAPTGENERATION, COALUTILGENERATION, OWNUSEFRAC, **kwargs: COALCAPTGENERATION + COALUTILGENERATION * (1 - OWNUSEFRAC)
    },
    'OWNUSEFRAC':{
        'type': 'input',
        'name': 'Fraction of energy for own use',
        'unit': '1',
    },
    'COALEFF':{
        'type': 'input',
        'name': 'Coal thermal conversion efficiency',
        'unit': '1'
    },
    'COALFUEL':{
        'type': 'variable',
        'name': 'Fuel required for coal generation',
        'unit': 'TWh',
        'computation': lambda COALEFF, COALGENERATION, **kwargs: COALEFF * COALGENERATION
    },
    'COALEMISSIONSi':{
        'type': 'variable',
        'name': 'C02, CH4, NO2 emissions',
        'unit': 'Mt CO2eq',
        'computation': lambda COALFUEL, COALEMFACTORi, **kwargs: COALFUEL * COALEMFACTORi
    },
    'COALLANDREQ':{
        'type': 'input',
        'name': 'land requirement per GW of coal plant',
        'unit': 'ha / GW'
    },
    'COALEMFACTORi':{
        'type': 'input',
        'name': 'Gas emission factors',
        'unit': 'Mt CO2eq / TWh'
    },
    'COALLAND':{
        'type': 'variable',
        'name': 'Coal plant land requirement',
        'unit': 'ha',
        'computation': lambda COALCAPACITY, COALLANDREQ, **kwargs: COALCAPACITY * COALLANDREQ
    },
    'COALUTILCAPFACTOR':{
        'type': 'input',
        'name': 'Coal plant capacity factor utility',
        'unit': '1',
    },
    'COALCAPTCAPFACTOR':{
        'type': 'input',
        'name': 'Coal plant capacity factor captive',
        'unit': '1',
    },
    'COALHOURS':{
        'type': 'input',
        'name': 'Coal generation time',
        'unit': 'hours'
    },
    'COALUTILGENERATION':{
        'type': 'variable',
        'name': 'Coal generation for utilities',
        'unit': 'TWh',
        'computation': lambda COALHOURS, COALUTILCAPFACTOR, COALCAPACITY, **kwargs: COALHOURS * COALUTILCAPFACTOR * COALCAPACITY
    },
    'COALCAPTGENERATION':{
        'type': 'variable',
        'name': 'Coal generation for captive',
        'unit': 'TWh',
        'computation': lambda COALHOURS, COALCAPTCAPFACTOR, COALCAPACITY, **kwargs: COALHOURS * COALCAPTCAPFACTOR * COALCAPACITY
    },
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
    'SOLARHOURS':{
        'type': 'input',
        'name': 'Solar generation time',
        'unit':'hours'
    },
    'SOLARGENERATION':{
        'type': 'variable',
        'name': 'Solar generation',
        'unit': 'TWh',
        'computation': lambda SOLARHOURS, SOLARCAPFACTOR, SOLARCAPACITY, **kwargs: SOLARHOURS * SOLARCAPFACTOR * SOLARCAPACITY
    },
    'SOLARLANDREQ':{
        'type': 'input',
        'name': 'land requirement per GW of solar plant',
        'unit': 'ha / GW'
    },
    'SOLARLAND':{
        'type': 'variable',
        'name': 'Solar PV land requirement',
        'unit': 'ha',
        'computation': lambda SOLARGENERATION, SOLARLANDREQ, **kwargs: SOLARGENERATION * SOLARLANDREQ
    }
}

GraphModel(SOLAR_nodes).draw()
SUPPLY_nodes = concatenate_graph_specs([SOLAR_nodes, COAL_nodes, GAS_nodes])

SUPPLY_model = GraphModel(SUPPLY_nodes)


# Dictionnary for easier access in the interface
model_dictionnary = {'SUPPLY_model': SUPPLY_model}

model_properties = get_model_properties('models/energy/SUPPLY_properties.json')