from ggmodel_dev.graphmodel import GraphModel
from ggmodel_dev.utils import get_model_properties


BIOMASS_nodes = {
    'C_fr': {'type': 'input',
              'unit': '1',
              'name': 'Carbon fraction of dry matter'},
    'G_w': {'type': 'input',
              'unit': 'tonnes dry matter/ha',
              'name': 'average annual above-ground biomass growth'},
    'Cg': {'type': 'variable',
              'name': 'Annual increase in carbon stocks duo to biomass growth',
              'unit': 'tonnes carbon',
              'computation': lambda G_w,FLi,C_fr, **kwargs: sum(FLi*G_w*C_fr)
              },  
    'FLi': {'type': 'input',
             'unit': 'ha',
             'name': 'Forest land by forest type'},
    'Hi': {'type': 'input',
              'unit': 'm3',
              'name': 'Annual industrial roundwood removals'},
    'BCEFr': {'type': 'input',
              'unit': 'm3',
              'name': 'Biomass conversion & expansion factor for biomass removal'},  
    'L_wood_removals': {'type': 'variable',
              'name': 'Carbon loss due to wood removals',
              'unit': 'tonnes carbon',
              'computation': lambda Hi,BCEFr,C_fr, **kwargs: sum(Hi*BCEFr*C_fr)
             },
    'L_fuelwood': {'type': 'variable',
              'name': 'Annual carbon loss in biomass of fuelwood removal',
              'unit': 'tonnes carbon',
              'computation': lambda FG_tree,BCEFr,C_fr,  **kwargs: sum(FG_tree*BCEFr*C_fr)
             },
    'FG_tree': {'type': 'parameter',
              'unit': 'm3',
              'name': 'Volume of fuel wood removal as tree parts'},
    'A_disturbance': {'type': 'parameter',
              'unit': 'ha',
              'name': 'Area affected by disturbances'},
    'B_w': {'type': 'input',
              'unit': 'tonnes/ha',
              'name': 'Average above-ground biomass of land areas affected by disturbances'},
    'L_disturbance': {'type': 'variable',
              'name': 'Annual carbon loss in biomass due to disturbances',
              'unit': 'tonnes carbon',
              'computation': lambda A_disturbance,B_w,C_fr, **kwargs: sum(A_disturbance*B_w*C_fr*1)
             },

    'C_losses': {'type': 'variable',
              'name': 'Annual decrease in carbon stocks due to biomass loss',
              'unit': 'tonnes carbon',
              'computation': lambda L_wood_removals,L_fuelwood,L_disturbance,  **kwargs: L_wood_removals+L_fuelwood+L_disturbance
             },

    'Change_biomass': {'type': 'variable',
              'name': 'Annual change in carbon stocks in biomass',
              'unit': 'tonnes carbon',
              'computation': lambda Cg, C_losses,  **kwargs: Cg - C_losses
             },
    'delta_BE3': {'type': 'variable',
              'name': 'Annual change in carbon stocks in biomass',
              'unit': 'tonnes carbon/ha',
              'computation': lambda Change_biomass,FLi,  **kwargs: Change_biomass/sum(FLi)
             },
    'BE3_baseline': {'type': 'input',
              'unit': 'tonnes carbon/ha',
              'name': 'Carbon content of above-ground biomass t-1'},  
    'BE3': {'type': 'output',
              'name': 'Above-ground biomass',
              'unit': 'tonnes carbon/ha',
              'computation': lambda BE3_baseline, delta_BE3,  **kwargs: BE3_baseline + delta_BE3
             },
}

BIOMASS_model = GraphModel(BIOMASS_nodes)

model_dictionnary = {'BIOMASS_model': BIOMASS_model}

model_properties = get_model_properties('models/landuse/BIOMASS_properties.json')