from ggmodel_dev.graphmodel import GraphModel
from ggmodel_dev.utils import get_model_properties


crop_group = ['Cereals - Excluding Beer', 'Starchy Roots', 'Sugar Crops', 'Sugar & Sweeteners', 'Pulses',
              'Treenuts', 'Oilcrops', 'Vegetable Oils', 'Vegetables', 'Fruits - Excluding Wine',
              'Stimulants', 'Spices']
m3_to_tonnes = 1  # to check


SL1_nodes = {'FDTi': {'type': 'input',
                      'unit': '1000 tonnes',
                      'name': 'Total food demand per food group'
                      },
             'CNYi': {'type': 'input',
                      'unit': 'N/tonnes',
                      'name': 'Crop nitrogen yield per unit of output'
                      },
             'OUT_C': {'type': 'variable',
                       'unit': 'tonnesN',
                       'name': 'Crop output',
                       'computation': lambda FDTi, CNYi, **kwargs: FDTi.loc[crop_group] * CNYi * 1e3
                       },
             'BF': {'type': 'input', 'unit': 'tonnesN', 'name': 'Biological N fixation'
                    },
             'AD': {'type': 'input', 'unit': 'tonnesN', 'name': 'Atmospheric N deposition'},
             'IN_F': {'type': 'input', 'unit': 'kg', 'name': 'Agricultural Use in nutrients'},
             'MASi': {'type': 'input',
                      'unit': 'kgN',
                      'name': 'Vector manure applied to soil'},
             'SL1': {'type': 'output',
                     'unit': 'tonnes N',
                     'name': 'Nutrient balance',
                     'computation': lambda MASi, IN_F, BF, AD, OUT_C, **kwargs: MASi * 1e-3 + IN_F + BF + AD - OUT_C
                     }
             }


# BE3_nodes = {'NFI': {'type': 'input',
#                      'unit': 'm3/ha',
#                      'name': 'Net natural forest increment rate'},
#              'CSF': {'type': 'parameter',
#                      'unit': 'm3/ha',
#                      'name': 'Climate smart forestry practices'},
#              'FBI': {'type': 'variable',
#                      'unit': 'm3/ha',
#                      'name': 'Forest biomass increment',
#                      'computation': lambda CSF, NFI, **kwargs: CSF + NFI
#                      },
#              'HR': {'type': 'input', 'unit': '%', 'name': 'Harvest rate'},
#              'BE3': {'type': 'output',
#                      'unit': 'tonnes/ha',
#                      'name': 'net change forest biomass',
#                      'computation': lambda FBI, HR, **kwargs: FBI * (1 - HR * 1e-2) * m3_to_tonnes
#                      },
#              }

BE3_nodes = {
# New node set to 0.47 - Table 4.3 https://www.ipcc-nggip.iges.or.jp/public/2006gl/pdf/4_Volume4/V4_04_Ch4_Forest_Land.pdf
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


BE3_model = GraphModel(BE3_nodes)
SL1_model = GraphModel(SL1_nodes)


model_dictionnary = {
    'BE3_model': BE3_model,
    'SL1_model': SL1_model
}

model_properties = get_model_properties('models/landuse/SL1_BE3_properties.json')
