from ggmodel_dev.graphmodel import GraphModel, concatenate_graph_specs
from ggmodel_dev.utils import get_model_properties

AGRI_nodes = {
    'NTRACTORS':{
        'type': 'input',
        'name': 'Number of tractors',
        'unit':'1',
    },
    'FUELTRACTORS':{
        'type': 'input',
        'name': 'Diesel demand for 1 tractor',
        'unit': 'litres / hour'
    },
    'USETRACTOR':{
        'type': 'input',
        'name': 'Number of hours of use of a tractor',
        'unit': 'hour'
    },
    'FUELTRACTOR':{
        'type': 'variable',
        'name': 'Diesel required for tractors',
        'unit': 'bcm',
        'computation': lambda USETRACTOR, FUELTRACTORS, NTRACTORS, **kwargs: USETRACTOR * FUELTRACTORS * NTRACTORS
    },
    'TRACTOREMFACTORi':{
        'type': 'input',
        'name': 'Tractor emissions factors',
        'unit':'Mt CO2eq / bcm'
    },
    'EMISSIONTRACTORi':{
        'type': 'variable',
        'name': 'C02, CH4, NO2 emissions',
        'unit': 'Mt CO2eq',
        'computation': lambda TRACTOREMFACTORi, FUELTRACTOR, **kwargs: FUELTRACTOR * TRACTOREMFACTORi
    }
}


RESIDENTIAL_nodes = {
    'NHOUSEHOLD':{
        'type': 'input',
        'name': 'Number of household by rural/urban',
        'unit':'households',
    },
    'HOURUSAGE':{
        'type': 'input',
        'name': 'Weighted hours of usage',
        'unit': 'hours',
    },
    'HOUSEHOLDUSAGEi':{
        'type': 'input',
        'name': 'Percentage of households using appliances by appliances and rural/urban',
        'unit': '%'
    },
    'NAPPLIANCE':{
        'type': 'input',
        'name': 'Number of appliancces by appliance', 
        'unit': 'count'
    },
    'APPEFFICENCYi':{
        'type': 'input',
        'name': 'Weighted average efficiency by appliance by appliance',
        'unit': '%'
    },
    'APPDEMANDi':{
        'type': 'variable',
        'name': 'Energy demand by appliance',
        'unit': 'TWh',
        'computation': lambda HOURUSAGE, APPCONSUMPi, NAPPLIANCE, **kwargs: HOURUSAGE * APPCONSUMPi * NAPPLIANCE
    },
    'APPCONSUMPi':{
        'type': 'input',
        'name': 'Average comsumption by appliance',
        'unit': 'W'
    }
}


DEMANDE_nodes = concatenate_graph_specs([AGRI_nodes, RESIDENTIAL_nodes])

DEMAND_model = GraphModel(DEMANDE_nodes)


# Dictionnary for easier access in the interface
model_dictionnary = {'DEMAND_model': DEMAND_model}

model_properties = get_model_properties('models/energy/DEMAND_properties.json')