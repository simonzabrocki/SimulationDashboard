__author__ = 'Hermen'
__status__ = 'Pending Validation'

"""
TO DO.
"""
from GM.graphmodels.graphmodel import GraphModel, concatenate_graph_specs
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
import plotly.graph_objects as go

# To check naming, confusing with demand/prod + total not total
kg_to_1000tonnes = 1e-6
day_per_year = 365
ktonnes_to_hg = 1e7


FPi_nodes = {'FLOi': {
                'type': 'input',
                'unit': '1000 tonnes',
                'name': 'Food losses per food group'
                },
             'FDKGi': {
                'type': 'input',
                'unit': 'kg/capita/day',
                'name': 'Kg food demand per day per food group'
                },
             'SSRi': {
                'type': 'input',
                'unit': '1',
                'name': 'Self-sufficiency ratio per food group',
                },
             'FDPi': {
                'type': 'variable',
                'unit': '1000 tonnes',
                'name': 'Total food production per food group',
                'computation': lambda FDKGi, Pop, FLOi, **kwargs: kg_to_1000tonnes * day_per_year * FDKGi.fillna(0) * Pop * 1e3 + FLOi.fillna(0)
                },
             'OFi': {
                'type': 'variable',
                'unit': '1000 tonnes',
                'name': 'Other food demand',
                'computation': lambda SDi, NFDi, PDi, RDi, SVi, **kwargs: SDi.fillna(0) + NFDi.fillna(0) + PDi.fillna(0) + RDi.fillna(0) + SVi.fillna(0)
                },
             'SDi': {
                'type': 'input',
                'unit': '1000 tonnes',
                'name': 'Seed demand per food group'
                },
             'NFDi': {
                'type': 'input',
                'unit': '1000 tonnes',
                'name': 'Non-food demand per food group'
                },
             'PDi': {
                'type': 'input',
                'unit': '1000 tonnes',
                'name': 'Processed demand per food group'
                },
             'RDi': {
                'type': 'input',
                'unit': '1000 tonnes',
                'name': 'Residual demand per food group'
                },
             'SVi': {
                'type': 'input',
                'unit': '1000 tonnes',
                'name': 'Stock variation per food group'
                },
             'FPi': {
                'type': 'output',
                'name': 'Food production per food group',
                'unit': '1000 tonnes',
                'computation': lambda SSRi, OFi, FDi, FDPi, **kwargs: (OFi.fillna(0) + FDi.fillna(0) + FDPi.fillna(0)) * SSRi.fillna(1)
                },
             'FDi': {
                'type': 'input',
                'unit': '1000 tonnes',
                'name': 'Feed demand per food group'
                },
             'Pop': {
                'type': 'input',
                'unit': '1000 persons',
                'name': 'Total population'
                }
        }

TCLDi_nodes = {'TCLDi': {
                  'type': 'output',
                  'name': 'Cropland demand',
                  'unit': 'ha',
                  'computation': lambda CYi, FPi, **kwargs: ktonnes_to_hg * FPi / CYi
                  },
               'CYi': {
                  'type': 'input',
                  'unit': 'hg/ha',
                  'name': 'Crop yields per crop type'
                  },
               'FPi': {
                  'type': 'input',
                  'name': 'Food production per food group',
                  'unit': '1000 tonnes'
                  },
               }

CL_nodes = {'TCLDi': {
               'type': 'input',
               'name': 'Cropland demand',
               'unit': 'ha',
               },
            'CL_corr_coef': {
               'type': 'input',
               'name': 'Correction coefficient',
               'unit': '1',
               },
            'CL_corr_intercept': {
               'type': 'input',
               'name': 'Correction intercept by country',
               'unit': '1000 ha',
               },
            'CL': {
               'type': 'output',
               'name': 'Cropland stock',
               'unit': '1000 ha',
               'computation':  lambda TCLDi, CL_corr_coef, **kwargs: TCLDi.groupby(level=['ISO', 'Year']).sum() * 1e-3 *CL_corr_coef #+ CL_corr_intercept # Strange to check !
            },
}

IL_FL_nodes = {'CL': {
                  'type': 'input',
                  'name': 'Cropland stock',
                  'unit': '1000 ha',
                  },
               'CL_baseline': {
                  'type': 'input',
                  'name': 'Cropland stock baseline',
                  'unit': '1000 ha',
                  },
               'delta_CL': {
                  'type': 'variable',
                  'name': 'Change in cropland',
                  'unit': '1000 ha',
                  'computation': lambda CL, CL_baseline, **kwargs: CL - CL_baseline
                  },
               'IL_baseline': {
                  'type': 'input',
                  'unit': '1000 ha',
                  'name': 'Inactive land baseline'
                  },
               'FL_baseline': {
                  'type': 'input',
                  'unit': '1000 ha',
                  'name': 'Forest land baseline'
                  },
               'IL': {
                  'type': 'output',
                  'name': 'Inactive land stock',
                  'unit': '1000 ha',
                  'computation': lambda delta_CL, IL_baseline, **kwargs: (IL_baseline - delta_CL).clip(lower=0) # to double check
                  },
               'FL': {
                  'type': 'output',
                  'name': 'Forest land stock',
                  'unit': '1000 ha',
                  'computation': lambda delta_CL, FL_baseline, IL_baseline, **kwargs: FL_baseline + (IL_baseline - delta_CL).clip(upper=0) # to double check
                  }
               }

BE2_nodes = {'TLA':{
               'type': 'input',
               'unit': '1000 ha',
               'name': 'Total land area'
               },
             'FL': {
               'type': 'input',
               'unit': '1000 ha',
               'name': 'Forest land stock'
               },
             'IL': {
               'type': 'input',
               'unit': '1000 ha',
               'name': 'Inactive land stock'
               },
             'R_rate': {
               'type': 'parameter',
               'unit': '%',
               'name': 'Rate of reforestation'
               },
             'FL_RF': {
               'type': 'variable',
               'name': 'Forest land stock after reforestation policy',
               'unit': '1000 ha',
               'computation': lambda FL, R_rate, IL, **kwargs: FL + 1e-2 * R_rate * IL
               },
             'BE2': {
               'type': 'output',
               'name': 'Share of forest area to total land area',
               'unit': '%',
               'computation': lambda FL_RF, TLA, **kwargs: 1e2 * FL_RF / TLA
               }
             }



FPi_model = GraphModel(FPi_nodes)
TCLDi_partial_model = GraphModel(TCLDi_nodes)
TCLDi_model = GraphModel(concatenate_graph_specs([TCLDi_nodes, FPi_nodes]))
IL_FL_model = GraphModel(IL_FL_nodes)
BE2_partial_model = GraphModel(concatenate_graph_specs([BE2_nodes, IL_FL_nodes]))
BE2_model = GraphModel(concatenate_graph_specs([BE2_nodes, IL_FL_nodes, CL_nodes, TCLDi_nodes, FPi_nodes]))

BE2_models = {
    'TCLDi_model': TCLDi_model,
    'TCLDi_partial_model': TCLDi_model,
    'FPi_model': FPi_model,
    'IL_FL_model': IL_FL_model,
    'BE2_partial_model': BE2_partial_model,
    'BE2_model': BE2_model
}


model_df = pd.read_csv('data/demo_data/BE2_data/BE2_df.csv').query('Year < 2019')
landuse = pd.read_csv('data/demo_data/BE2_data/landuse.csv')


def get_X_y_from_data(model, data_dict):
    '''TO CLEAN UP'''
    X = {key: data_dict[key] for key in model.inputs_() + model.parameters_()}
    y = {key: data_dict[key] for key in model.variables_(
    ) + model.outputs_() if key in data_dict}
    return X, y


def df_to_dict(df):
    X = {}
    for code in df.columns:
        X[code] = df[code]#.fillna(0)
    return X


def fill_missing_values(df):
    return df


def df_to_data_dict(df, itemized):
    data_dict = {}

    non_item_df = df[~df.Variable.isin(itemized)].pivot(
        index=['ISO', 'Year'], columns='Variable', values='Value')
    non_item_df = fill_missing_values(non_item_df)

    if itemized != []:
        item_df = df[df.Variable.isin(itemized)].pivot(
            index=['ISO', 'Year', 'Item'], columns='Variable', values='Value')
        data_dict.update(df_to_dict(item_df))

    data_dict.update(df_to_dict(non_item_df))

    return data_dict


itemized = [
    'FDKCi', 'FPi', 'FIi', 'SVi', 'FEi',
    'FDi', 'SDi', 'FLOi', 'PDi', 'RDi', 'Food', 'FDKGi', 'NFDi',
    'SSRi', 'KKRi', 'TCLDi', 'CYi'
]

data_dict = df_to_data_dict(model_df, itemized)


data_dict.update(df_to_data_dict(landuse, itemized=[]))

data_dict['CL_baseline'] = data_dict['CL']
data_dict['IL_baseline'] = data_dict['IL']
data_dict['FL_baseline'] = data_dict['FL']
data_dict['R_rate'] = pd.Series(data=0, index=data_dict['CL_baseline'].index)




def expand_series_non_itemized(df):
    multi_index = pd.MultiIndex.from_product([df.index.get_level_values(
        'ISO').unique(), np.arange(2018, 2051)], names=['ISO', 'Year'])
    return df.reindex(multi_index)


def expand_series_itemized(df):
    multi_index = pd.MultiIndex.from_product([df.index.get_level_values('ISO').unique(), np.arange(
        2018, 2051), df.index.get_level_values('Item').unique()], names=['ISO', 'Year', 'Item'])
    return df.reindex(multi_index)


def apply_percent_target_projection(series, percent_target=0):
    series = series.copy()
    series = expand_series_non_itemized(series)
    series.loc[:, 2050, :] = percent_target * series.loc[:, 2018, :].values
    return series.interpolate()


def apply_target_projection(series, target=0):
    series = series.copy()
    series = expand_series_non_itemized(series)
    series.loc[:, 2050, :] = target
    return series.interpolate()


def apply_itemized_percent_target_projection(series, percent_target=0):
    '''To improve: Apply item wise projection'''
    series = series.copy()
    series = expand_series_itemized(series)
    series.loc[:, 2050, :] = percent_target * series.loc[:, 2018, :].values

    return series.groupby(level=['ISO', 'Item']).apply(lambda group: group.interpolate())


def apply_annual_rate_projection(series, rate=1):
    series = series.copy()
    series = expand_series_non_itemized(series)

    year = series.loc[:, 2019:].index.get_level_values(level='Year').values

    series.loc[:, 2019:] = series.loc[:, 2018].values * rate ** (year - 2019)

    return series


def apply_constant_projection(series, constant=0):
    series = series.copy()
    series = expand_series_non_itemized(series)
    series.loc[:, 2018:] = constant

    return series


def apply_itemized_ffill_projection(series):
    series = series.copy()
    series = expand_series_itemized(series)

    return series.groupby(['ISO', 'Item']).fillna(method='ffill')


def apply_ffill_projection(series):
    series = series.copy()
    series = expand_series_non_itemized(series)

    return series.groupby(['ISO']).fillna(method='ffill')


def run_BE2_scenario(data_dict, FDKGi_target=1, FLOi_target=1, CYi_target=1, R_rate=0):

    data_dict = data_dict.copy()

    projection_dict = {
        'CYi': lambda x: apply_itemized_percent_target_projection(x, CYi_target),
        'FDKGi': lambda x: apply_itemized_percent_target_projection(x, FDKGi_target),
        'FLOi': lambda x: apply_itemized_percent_target_projection(x, FLOi_target),
        'R_rate': lambda x: apply_target_projection(x, R_rate)
    }

    for variable, function in projection_dict.items():
        data_dict[variable] = function(data_dict[variable])

    results = BE2_models['BE2_model'].run(data_dict)
    
    # Correct the CL_baseline (find a better way to do it)
    
    results['CL_baseline'] = pd.Series(results['CL'].loc[:, 2018].values[0], index=results['CL'].index)
    
    
    corrected_results = BE2_models['BE2_partial_model'].run(results)
    #return results
    
    return corrected_results


def run_BE2_projection(data_dict):
    data_dict = data_dict.copy()

    projection_dict = {
        'FDi': lambda x: apply_itemized_ffill_projection(x),
        'SSRi': lambda x: apply_itemized_ffill_projection(x),
        'SVi': lambda x: apply_itemized_ffill_projection(x),
        'RDi': lambda x: apply_itemized_ffill_projection(x),
        'NFDi': lambda x: apply_itemized_ffill_projection(x),
        'FEi': lambda x: apply_itemized_ffill_projection(x),
        'FIi': lambda x: apply_itemized_ffill_projection(x),
        'PDi': lambda x: apply_itemized_ffill_projection(x),
        'FDi': lambda x: apply_itemized_ffill_projection(x),
        'SDi': lambda x: apply_itemized_ffill_projection(x),
        'TLA': lambda x: apply_ffill_projection(x),
        'CL_baseline': lambda x: apply_ffill_projection(x),
        'IL_baseline': lambda x: apply_ffill_projection(x),
        'FL_baseline': lambda x: apply_ffill_projection(x),
        'Pop': lambda x: apply_ffill_projection(x),
    }

    for variable, function in projection_dict.items():
        data_dict[variable] = function(data_dict[variable])

    return data_dict


# GE3

__author__ = 'Hermen'
__status__ = 'Pending Validation'

"""
TO DO.
"""

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
             'Pop': {'type': 'input', 'unit': '1000 persons', 'name': 'Total population'}}

TAi_nodes = {'FPi': {'type': 'input',
                     'unit': 'tonnes',
                     'name': 'Production'},
             'AYi': {'type': 'input',
                     'unit': 'tonnes/head',
                     'name': 'Vector of animal yields'},
             'ANPi': {'type': 'variable',
                      'unit': 'head',
                      'name': 'Vector animals needed for production',
                      'computation': lambda FPi, AYi, **kwargs: FPi / AYi
                      },
             'PTTAi': {'type': 'parameter',
                       'unit': '1',
                       'name': 'vector production-to-total animals ratio',
                       },
             'TAi': {'type': 'output',
                     'unit': 'head',
                     'name': 'Vector total animal population',
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

GE3_nodes = {'Pop': {'type': 'input', 'unit': '1000 persons', 'name': 'Total population'},
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

GE3_models = {'TMi_model': TMi_model,
              # 'TAi_model': TAi_model,
              'M_xi_model': M_xi_model,
              'TMP_CO2eq_model': TMP_CO2eq_model,
              'TMT_CO2eq_model': TMT_CO2eq_model,
              'TMA_CO2eq_model': TMA_CO2eq_model,
              'TEE_CO2eq_model': TEE_CO2eq_model,
              'FE_CO2eq_model': FE_CO2eq_model,
              'GE3_partial_model': GE3_partial_model,
              'GE3_model': GE3_model
              }


def run_GE3_scenario(data_dict, MM_Ti=1/2, MM_ASi=1):

    data_dict = data_dict.copy()

    data_dict['MM_Ti'] = MM_Ti
    data_dict['MM_ASi'] = MM_ASi
    data_dict['MM_LPi'] = 1 - MM_Ti

    results = GE3_models['GE3_model'].run(data_dict)

    return results


GE3_model_df = pd.read_csv('data/demo_data/GE3_data/GE3_df.csv')

itemized = ['TAi', 'EF_EEi', 'EECH4', 'TEE_CO2eq', 'M_ASi',
            'EF_ASi', 'E_ASi', 'TMA_CO2eq', 'M_Ti', 'EF_CH4Ti',
            'EF_Ti', 'E_TCH4i', 'E_Ti', 'TMT_CO2eq', 'M_LPi', 'EF_Li', 'E_Li',
            'TMP_CO2eq', 'TMi', 'MM_ASi', 'MM_LPi', 'MM_Ti', 'MYi', ]


GE3_data_dict = df_to_data_dict(GE3_model_df, itemized)


def format_data_dict_sankey(data_dict):
    data_dict = data_dict.copy()

    # grab data and format
    data = pd.concat([v.to_frame(name='Value').assign(Variable=k)
                      for k, v in data_dict.items()], axis=0).reset_index().dropna()

    data = pd.concat([data, data.groupby('Variable').sum().reset_index().rename(
        columns={"Variable": 'Item'}).assign(Variable='Non-CO2 agricultural emissions')])

    # add encoding for Sanky
    le = LabelEncoder()
    encoded = le.fit_transform(
        data[['Item', 'Variable']].values.flatten()).reshape(-1, 2)

    data[['Source', 'Target']] = encoded

    return data, le.classes_


def plot_sanky_GE3(data, classes):
    '''To improve, should write a more general wrapper for Sankey'''

    fig = go.Figure(data=[go.Sankey(
        node=dict(
            pad=15,
            thickness=20,
            line=dict(color="black", width=0.5),
            label=classes,
            #color = "blue"
        ),
        link=dict(
            target=data['Target'],
            source=data['Source'],
            value=data['Value']
        ))])

    fig.update_layout(
        title_text=f"Agricultural Animal Emissions", font_size=10)
    return fig
