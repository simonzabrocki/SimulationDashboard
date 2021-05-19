__author__ = 'Hermen'
__status__ = 'Pending Validation'

"""
TO DO.
"""
from ggmodel_dev.graphmodel import GraphModel, concatenate_graph_specs
from ggmodel_dev.utils import get_model_properties

# Conversions
GWPN2O = 310
GWPCH4 = 21
N2ON_to_NO2 = 1.57
kg_to_Gg = 1e-6
ktonnes_to_hg = 1e-7
kg_to_1000tonnes = 1e-6
day_per_year = 365
ktonnes_to_hg = 1e7

# Nodes
FPi_nodes = {'FLOi': {'type': 'input',
                      'unit': '1000 tonnes',
                      'name': 'Food losses per food group'},
             'FDKGi': {'type': 'input',
                       'unit': 'kg/capita/day',
                       'name': 'Kg food demand per day per food group'},
             'SSRi': {'type': 'input',
                      'unit': '1',
                      'name': 'Self-sufficiency ratio per food group',
                      },
             'FDPi': {'type': 'variable',
                      'unit': '1000 tonnes',
                      'name': 'Total food production per food group',
                      'computation': lambda FDKGi, Pop, FLOi, **kwargs: kg_to_1000tonnes * day_per_year * FDKGi * Pop * 1e3 + FLOi
                      },
             'OFi': {'type': 'variable',
                     'unit': '1000 tonnes',
                     'name': 'Other food demand',
                     'computation': lambda SDi, NFDi, PDi, RDi, SVi, **kwargs: SDi + NFDi + PDi + RDi + SVi
                     },
             'SDi': {'type': 'input',
                     'unit': '1000 tonnes',
                     'name': 'Seed demand per food group'},
             'NFDi': {'type': 'input',
                      'unit': '1000 tonnes',
                      'name': 'Non-food demand per food group'},
             'PDi': {'type': 'input',
                     'unit': '1000 tonnes',
                     'name': 'Processed demand per food group'},
             'RDi': {'type': 'input',
                     'unit': '1000 tonnes',
                     'name': 'Residual demand per food group'},
             'SVi': {'type': 'input',
                     'unit': '1000 tonnes',
                     'name': 'Stock variation per food group'},
             'FPi': {'type': 'output',
                     'name': 'Food production per food group',
                     'unit': '1000 tonnes',
                     'computation': lambda SSRi, OFi, FDi, FDPi, **kwargs: (OFi + FDi + FDPi) * SSRi
                     },
             'FDi': {'type': 'input',
                     'unit': '1000 tonnes',
                     'name': 'Feed demand per food group'},
             'Pop': {'type': 'input', 'unit': 'capita', 'name': 'Population'}}

TAi_nodes = {'FPi': {'type': 'input',
                     'unit': '1000 tonnes',
                     'name': 'Food production per food group'},
             'AYi': {'type': 'input',
                     'unit': 'tonnes/head',
                     'name': 'Vector of animal yields'},
             'ANPi': {'type': 'variable',
                      'unit': 'head',
                      'name': 'Vector animals needed for production',
                      'computation': lambda FPi, AYi, **kwargs: 1e3 * FPi / AYi
                      },
             'PTTAi': {'type': 'parameter',
                       'unit': '1',
                       'name': 'vector production-to-total animals ratio',
                       },
             'TAi': {'type': 'output',
                     'unit': 'head',
                     'name': 'Total animal population',
                     'computation': lambda ANPi, PTTAi, **kwargs: PTTAi * ANPi.groupby(level=['ISO', 'Year', 'emi_item']).sum().rename_axis(index={"emi_item": 'Item'})
                     },
             }

TMi_nodes = {'TAi': {'type': 'input', 'unit': 'head', 'name': 'Total animal population'},
             'MYi': {'type': 'input', 'unit': 'kgN/head', 'name': 'Manure yields'},
             'TMi': {'type': 'output',
                     'unit': 'kgN',
                     'name': 'Total Manure (N content)',
                     'computation': lambda TAi, MYi, **kwargs: TAi * MYi
                     }
             }

M_xi_nodes = {'TMi': {'type': 'input',
                              'unit': 'kgN',
                              'name': 'Total Manure (N content)'},
              'MM_ASi': {'type': 'input',
                         'unit': '1',
                         'name': '% Manure applied to soils'},
              'MM_LPi': {'type': 'input',
                         'unit': '1',
                         'name': '% Manure left on pasture'},
              'MM_Ti': {'type': 'input',
                        'unit': '1',
                        'name': '% Manure treated'},
              'M_Ti': {'type': 'output',
                       'unit': 'kgN',
                       'name': 'Manure treated (N content)',
                       'computation': lambda MM_Ti, TMi, **kwargs: MM_Ti * TMi

                       },
              'M_LPi': {'type': 'output',
                        'unit': 'kg',
                        'name': 'Manure left on pasture (N content)',
                        'computation': lambda MM_LPi, TMi, **kwargs: MM_LPi * TMi

                        },
              'M_ASi': {'type': 'output',
                        'unit': 'kgN',
                        'name': 'Manure applied to soils (N content)',
                        'computation': lambda MM_ASi, TMi, **kwargs: MM_ASi * TMi

                        }
              }

TMP_CO2eq_nodes = {'M_LPi': {'type': 'input',
                             'unit': 'kg',
                             'name': 'Manure left on pasture (N content)'},
                   'EF_Li': {'type': 'parameter',
                             'unit': 'kg N2O-N/kg N',
                             'name': 'Implied emission factor for N2O (Manure on pasture)'
                             },
                   'TMP_CO2eq': {'type': 'output',
                                 'unit': 'gigagrams (CO2eq)',
                                 'name': 'Emissions (CO2eq) (Manure on pasture)',
                                 'computation': lambda M_LPi, EF_Li, **kwargs: kg_to_Gg * N2ON_to_NO2 * GWPN2O * (M_LPi * EF_Li)
                                 }
                   }

TMT_CO2eq_nodes = {'M_Ti': {'type': 'input',
                            'unit': 'kgN',
                            'name': 'Manure treated (N content)',
                            },
                   'EF_Ti': {'type': 'parameter',
                             'unit': 'kg N2O-N/kg N',
                             'name': 'Implied emission factor for N2O (Manure management)'},
                   'EF_CH4Ti': {'type': 'parameter',
                                'unit': 'kg/head',
                                'name': 'Implied emission factor for CH4 (Manure management)'},
                   'TAi': {'type': 'input',
                           'unit': 'head',
                           'name': 'Total animal population'},
                   'E_Ti': {'type': 'variable',
                            'unit': 'gigagrams',
                            'name': 'Emissions (N2O) (Manure management)',
                            'computation': lambda EF_Ti, M_Ti, **kwargs: N2ON_to_NO2 * kg_to_Gg * (EF_Ti * M_Ti)
                            },
                   'E_TCH4i': {'type': 'variable',
                               'unit': 'gigagrams',
                               'name': 'Emissions (CH4) (Manure management)',
                               'computation': lambda EF_CH4Ti, TAi, **kwargs: kg_to_Gg * (EF_CH4Ti * TAi)
                               },
                   'TMT_CO2eq': {'type': 'output',
                                 'unit': 'gigagrams (CO2eq)',
                                 'name': 'Emissions (CO2eq) (Manure management)',
                                 'computation': lambda E_Ti, E_TCH4i, **kwargs: E_Ti * GWPN2O + E_TCH4i * GWPCH4
                                 }}

TMA_CO2eq_nodes = {'M_ASi': {'type': 'input',
                             'unit': 'kgN',
                             'name': 'Manure applied to soils (N content)',
                             },
                   'EF_ASi': {'type': 'parameter',
                              'unit': 'kg N2O-N/kg N',
                              'name': 'Implied emission factor for N2O (Manure applied)'},
                   'TMA_CO2eq': {'type': 'output',
                                 'unit': 'gigagrams (CO2eq)',
                                 'name': 'Emissions (CO2eq) (Manure applied)',
                                 'computation': lambda EF_ASi, M_ASi, **kwargs: GWPN2O * N2ON_to_NO2 * kg_to_Gg * (EF_ASi * M_ASi)
                                 }
                   }

TEE_CO2eq_nodes = {'EF_EEi': {'type': 'input',
                              'unit': 'kg CH4 / head',
                              'name': 'Implied emission factor for CH4 (Enteric)'},
                   'TAi': {'type': 'input',
                           'unit': 'head',
                           'name': 'Total animal population'},
                   'TEE_CO2eq': {'type': 'output',
                                 'unit': 'gigagrams (CO2eq)',
                                 'name': 'Emissions (CO2eq) (Enteric)',
                                 'computation': lambda TAi, EF_EEi, **kwargs: kg_to_Gg * GWPCH4 * (TAi * EF_EEi)
                                 }
                   }

FE_CO2eq_nodes = {
    'IN_F': {'type': 'input',
             'unit': 'kg',
             'name': 'Agricultural Use in nutrients',
             },
    'EF_F': {'type': 'parameter',
             'unit': 'kg N2O-N/kg N',
             'name': 'Implied emission factor for N2O (Synthetic fertilizers)'},
    'FE_CO2eq': {'type': 'output',
                 'unit': 'gigagrams (CO2eq)',
                 'name': 'Emissions (CO2eq) (Synthetic fertilizers)',
                 'computation': lambda EF_F, IN_F, **kwargs: GWPN2O * N2ON_to_NO2 * kg_to_Gg * (EF_F * IN_F)
                 }
}

GE3_nodes = {'Pop': {'type': 'input', 'unit': 'capita', 'name': 'Population'},
             'TEE_CO2eq': {'type': 'input',
                           'unit': 'gigagrams (CO2eq)',
                           'name': 'Emissions (CO2eq) (Enteric)'},
             'TMT_CO2eq': {'type': 'input',
                           'unit': 'gigagrams (CO2eq)',
                           'name': 'Emissions (CO2eq) (Manure management)'},
             'TMA_CO2eq': {'type': 'input',
                           'unit': 'gigagrams (CO2eq)',
                           'name': 'Emissions (CO2eq) (Manure applied)'},
             'TMP_CO2eq': {'type': 'input',
                           'unit': 'gigagrams (CO2eq)',
                           'name': 'Emissions (CO2eq) (Manure on pasture)'},
             'FE_CO2eq': {'type': 'input',
                          'unit': 'gigagrams (CO2eq)',
                          'name': 'Emissions (CO2eq) (Synthetic fertilizers)'},
             'OEi': {'type': 'input',
                     'unit': 'gigagrams (CO2eq)',
                     'name': 'Vector of other emissions'},
             'GE3': {'type': 'output',
                     'unit': 'gigagrams (CO2eq) / capita',
                     'name': 'Ratio of non-CO2 emissions in agriculture to population',
                     'computation': lambda OEi, TEE_CO2eq, TMT_CO2eq, TMP_CO2eq, TMA_CO2eq, FE_CO2eq, Pop, **kwargs: (OEi + (TEE_CO2eq + TMT_CO2eq + TMP_CO2eq + TMA_CO2eq + FE_CO2eq).groupby(level=['ISO', 'Year']).sum()) / (Pop * 1e3)}}


nodes = concatenate_graph_specs(
    [GE3_nodes, TEE_CO2eq_nodes, TMA_CO2eq_nodes, TMT_CO2eq_nodes, TMP_CO2eq_nodes, FE_CO2eq_nodes, M_xi_nodes, TMi_nodes])

# models
FPi_nodes = GraphModel(FPi_nodes)
TAi_model = GraphModel(TAi_nodes)
TMi_model = GraphModel(TMi_nodes)
M_xi_model = GraphModel(M_xi_nodes)
TMP_CO2eq_model = GraphModel(TMP_CO2eq_nodes)
TMT_CO2eq_model = GraphModel(TMT_CO2eq_nodes)
TMA_CO2eq_model = GraphModel(TMA_CO2eq_nodes)
TEE_CO2eq_model = GraphModel(TEE_CO2eq_nodes)
FE_CO2eq_model = GraphModel(FE_CO2eq_nodes)
GE3_partial_model = GraphModel(GE3_nodes)

GE3_model = GraphModel(nodes)

model_dictionnary = {'TMi_model': TMi_model,
                     'TAi_model': TAi_model,
                     'M_xi_model': M_xi_model,
                     'TMP_CO2eq_model': TMP_CO2eq_model,
                     'TMT_CO2eq_model': TMT_CO2eq_model,
                     'TMA_CO2eq_model': TMA_CO2eq_model,
                     'TEE_CO2eq_model': TEE_CO2eq_model,
                     'FE_CO2eq_model': FE_CO2eq_model,
                     'GE3_partial_model': GE3_partial_model,
                     'GE3_model': GE3_model
                     }

model_properties = get_model_properties('models/landuse/GE3_properties.json')
