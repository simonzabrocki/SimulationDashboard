__author__ = 'Hermen'
__status__ = 'Pending Validation'

"""
TO DO.
"""
from GM.graphmodels.graphmodel import GraphModel, concatenate_graph_specs
import pandas as pd


FDTi_nodes = {'TCDi': {'type': 'variable',
                       'unit': 'kcal/day',
                       'name': 'Total calorie demand per food group',
                       'computation': lambda P, FDKCi, FWi, FWCRi, **kwargs: P * (FDKCi + FWi - FWCRi) * 1e3
                       },
              'FWCRi': {'type': 'parameter',
                        'unit': 'kcal/cap/day',
                        'name': 'Waste reduction policy consumption per food group'},
              'FWPPi': {'type': 'parameter',
                        'unit': '%',
                        'name': 'Waste reduction policy production per food group'},
              'FWi': {'type': 'variable',
                      'unit': 'kcal/cap/day',
                      'name': 'Food waste per food group',
                      'computation': lambda FWPi_baseline, FWPPi, **kwargs: FWPi_baseline * FWPPi * 1e-2 / 365
                      },
              'FWPi_baseline': {'type': 'variable',
                                'unit': 'kcal/cap/day',
                                'name': 'Food waste baseline per food group',
                                'computation': lambda FLOi, KKRi, P, **kwargs: FLOi * KKRi / P * 1e-3
                                },
              'FLOi': {'type': 'input',
                       'unit': '1000 tonnes',
                       'name': 'Food losses per food group'},
              'KKRi': {'type': 'variable',
                       'name': 'kcal/1000 tonnes ratio per food group',
                       'unit': 'kcal/1000 tonnes',
                       'computation': lambda FDKCi, FDKGi, **kwargs: FDKCi / (FDKGi * 1e-6)
                       },
              'FDKGi': {'type': 'input',
                        'unit': 'kg/capita/day',
                        'name': 'Kg food demand per year per food group'},
              'FDKCi': {'type': 'input',
                        'unit': 'kcal/capita/day',
                        'name': 'kcal food demand per day per food group'},
              'P': {'type': 'input', 'unit': 'capita', 'name': 'Total population'},
              'SSRi': {'type': 'variable',
                       'unit': '1',
                       'name': 'Self-sufficiency ratio per food group',
                       'computation': lambda FPi, FEi, FIi, **kwargs: FPi / (FPi - FEi + FIi)
                       },
              'FPi': {'type': 'input',
                      'unit': '1000 tonnes',
                      'name': 'Food production per food group'},
              'FEi': {'type': 'input',
                      'unit': '1000 tonnes',
                      'name': 'Food exports per food group'},
              'FIi': {'type': 'input',
                      'unit': '1000 tonnes',
                      'name': 'Food imports per food group'},
              'FDPi': {'type': 'variable',
                       'unit': '1000 tonnes',
                       'name': 'Total domestic food production per food group',
                       'computation': lambda TCDi, SSRi, KKRi, **kwargs: TCDi * SSRi / KKRi * 365
                       },
              'FDi': {'type': 'input',
                      'unit': '1000 tonnes',
                      'name': 'Feed demand per group'},
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
              'FDTi': {'type': 'output',
                       'name': 'Total food demand per food group',
                       'unit': '1000 tonnes',
                       'computation': lambda SSRi, OFi, FDi, FDPi, **kwargs: SSRi * (OFi + FDi) + FDPi
                       }
              }

chCL_nodes = {'FDTi': {'type': 'input',
                       'name': 'Total food demand per food group',
                       'unit': '1000 tonnes'},
              'CYi': {'type': 'input',
                      'unit': 'hg/ha',
                      'name': 'Crop yields per crop type'},
              'TCLD_baseline': {'type': 'input',
                                'unit': 'ha',
                                'name': 'Total crop land demand (baseline)'},
              'CD_corr': {'type': 'parameter',
                          'unit': '1',
                          'name': 'Correction parameter crop demand'},
              'crop_group': {'type': 'parameter',
                             'unit': '1',
                             'name': 'crop group'},
              'TCLD': {'type': 'variable',
                       'name': 'Total cropland demand',
                       'unit': 'ha',
                       'computation': lambda FDTi, CYi, CD_corr, crop_group, **kwargs: (FDTi.loc[(slice(None), slice(None), crop_group)] / CYi).groupby(level=['Area', 'Year']).sum() * CD_corr * 1e7
                       },
              'chCL': {'type': 'output',
                       'name': 'Change in cropland',
                       'unit': '1000 ha',
                       'computation': lambda TCLD, TCLD_baseline, **kwargs: (TCLD - TCLD_baseline) * 1e-5
                       }
              }


def FL(chCL, FL_t_minus_1, IL_t_minus_1):
    '''To check'''
    df = pd.concat([chCL, FL_t_minus_1, IL_t_minus_1], axis=1).dropna()
    df.columns = ['chCL', 'FL_t_minus_1', 'IL_t_minus_1']
    df['FL'] = df['FL_t_minus_1']

    df[(df.chCL > 0) & (df.IL_t_minus_1 - df.chCL) < 0]['FL'] += df['IL_t_minus_1'] - df['chCL']

    return df['FL']


def IL(chCL, IL_t_minus_1):
    '''To check'''
    df = pd.concat([chCL, IL_t_minus_1], axis=1).dropna()
    df.columns = ['chCL', 'IL_t_minus_1']
    df['IL'] = df['IL_t_minus_1'] - df['chCL']
    df[(df.chCL > 0) & (df.IL_t_minus_1 - df.chCL) < 0] = 0
    return df['IL']


CH_IL_FL_nodes = {'chCL': {'type': 'input', 'name': 'Change in cropland', 'unit': '1000 ha'},
                  'CL_t_minus_1': {'type': 'input', 'unit': '1000 ha', 'name': 'Cropland t-1'},
                  'IL_t_minus_1': {'type': 'input',
                                   'unit': '1000 ha',
                                   'name': 'Inactive land t-1'},
                  'FL_t_minus_1': {'type': 'input',
                                   'unit': '1000 ha',
                                   'name': 'Forest land t-1'},
                  'CL_t': {'type': 'output',
                           'name': 'Cropland stock',
                           'unit': '1000 ha',
                           'computation': lambda chCL, CL_t_minus_1, **kwargs: chCL + CL_t_minus_1
                           },
                  'IL_t': {'type': 'output',
                           'name': 'Inactive land stock',
                           'unit': '1000 ha',
                           'computation': lambda chCL, IL_t_minus_1, **kwargs: IL(chCL, IL_t_minus_1)
                           },
                  'FL_t': {'type': 'output',
                           'name': 'Forest land stock',
                           'unit': '1000 ha',
                           'computation': lambda chCL, FL_t_minus_1, IL_t, **kwargs: FL(chCL, FL_t_minus_1, IL_t)
                           }
                  }

BE2_nodes = {'TLA': {'type': 'input', 'unit': '1000 ha', 'name': 'Total land area'},
             'FL_t': {'type': 'input', 'unit': '1000 ha', 'name': 'Forest land stock'},
             'IL_t': {'type': 'input', 'unit': '1000 ha', 'name': 'Inactive land stock'},
             'R_rate': {'type': 'parameter', 'unit': '%', 'name': 'Rate of reforestation'},
             'RF_land': {'type': 'variable',
                         'name': 'Reforestation of land',
                         'unit': '1000 ha',
                         'computation': lambda R_rate, IL_t, **kwargs: R_rate * 1e-2 * IL_t
                         },
             'FL_RF': {'type': 'variable',
                       'name': 'Forest land stock after reforestation policy',
                       'unit': '1000 ha',
                       'computation': lambda FL_t, RF_land, **kwargs: FL_t + RF_land
                       },
             'IL_RF': {'type': 'variable',
                       'name': 'Inactive land stock after reforestation policy',
                       'unit': '1000 ha',
                       'computation': lambda IL_t, RF_land, **kwargs: IL_t - RF_land
                       },
             'BE2': {'type': 'output',
                     'name': 'Share of forest area to total land area',
                     'unit': '%',
                     'computation': lambda FL_RF, TLA, **kwargs: 1e2 * FL_RF / TLA
                     }
             }

nodes = concatenate_graph_specs([chCL_nodes, FDTi_nodes, CH_IL_FL_nodes, BE2_nodes])

FDTi_model = GraphModel(FDTi_nodes)
CH_IL_FL_model = GraphModel(CH_IL_FL_nodes)
chCL_model = GraphModel(chCL_nodes)

BE2_model = GraphModel(nodes)

BE2_models = {'FDTi_model': FDTi_model,
              'CH_IL_FL_model': CH_IL_FL_model,
              'chCL_model': chCL_model,
              'BE2_model': BE2_model}
