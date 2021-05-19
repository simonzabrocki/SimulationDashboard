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
                     'unit': 'tonnesN',
                     'name': 'Nutrient balance',
                     'computation': lambda MASi, IN_F, BF, AD, OUT_C, **kwargs: MASi * 1e-3 + IN_F + BF + AD - OUT_C
                     }
             }


BE3_nodes = {'NFI': {'type': 'input',
                     'unit': 'm3/ha',
                     'name': 'Net natural forest increment rate'},
             'CSF': {'type': 'parameter',
                     'unit': 'm3/ha',
                     'name': 'Climate smart forestry practices'},
             'FBI': {'type': 'variable',
                     'unit': 'm3/ha',
                     'name': 'Forest biomass increment',
                     'computation': lambda CSF, NFI, **kwargs: CSF + NFI
                     },
             'HR': {'type': 'input', 'unit': '%', 'name': 'Harvest rate'},
             'BE3': {'type': 'output',
                     'unit': 'tonnes/ha',
                     'name': 'net change forest biomass',
                     'computation': lambda FBI, HR, **kwargs: FBI * (1 - HR * 1e-2) * m3_to_tonnes
                     },
             }


BE3_model = GraphModel(BE3_nodes)
SL1_model = GraphModel(SL1_nodes)


model_dictionnary = {
    'BE3_model': BE3_model,
    'SL1_model': SL1_model
}

model_properties = get_model_properties('models/landuse/SL1_BE3_properties.json')
