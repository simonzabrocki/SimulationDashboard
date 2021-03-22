import pandas as pd
from GM.graphmodels.graphmodel import GraphModel, concatenate_graph_specs
from statsmodels.tsa.api import Holt
import os
import numpy as np


def get_X_y_from_data(model, data_dict):
    '''TO CLEAN UP'''
    X = {key: data_dict[key] for key in model.inputs_() + model.parameters_()}
    y = {key: data_dict[key] for key in model.variables_(
    ) + model.outputs_() if key in data_dict}
    return X, y


def df_to_dict(df):
    X = {}
    for code in df.columns:
        X[code] = df[code].fillna(0)
    return X


def fill_missing_values(df):
    return df.groupby(level='ISO').fillna(method='ffill')\
             .groupby(level='ISO').fillna(method='bfill')


def df_to_data_dict(df, itemized):
    data_dict = {}

    non_item_df = df[~df.Variable.isin(itemized)].pivot(
        index=['ISO', 'Year'], columns='Variable', values='Value')
    non_item_df = fill_missing_values(non_item_df)
    item_df = df[df.Variable.isin(itemized)].pivot(
        index=['ISO', 'Year', 'Item'], columns='Variable', values='Value')

    data_dict.update(df_to_dict(non_item_df))
    data_dict.update(df_to_dict(item_df))

    return data_dict


def expand_series_non_itemized(df):
    multi_index = pd.MultiIndex.from_product([df.index.get_level_values(
        'ISO').unique(), np.arange(1980, 2051)], names=['ISO', 'Year'])
    return df.reindex(multi_index, method='ffill')


def expand_series_itemized(df):
    multi_index = pd.MultiIndex.from_product([df.index.get_level_values('ISO').unique(), np.arange(
        1980, 2051), df.index.get_level_values('Item').unique()], names=['ISO', 'Year', 'Item'])
    return df.reindex(multi_index)


def expand_data_dict(data_dict):
    data_dict_expanded = {}

    for key, item in data_dict.items():
        if key not in ['Kc', 'ICA']:
            data_dict_expanded[key] = expand_series_non_itemized(item)

    data_dict_expanded['Kc'] = data_dict['Kc']
    data_dict_expanded['ICA'] = data_dict['Kc']

    return data_dict_expanded


def apply_scenario_WP(WP, rate):
    WP = WP.copy()
    for i in range(2020, 2051):
        WP.loc[:, i] = (WP.loc[:, 2019] * rate ** (i - 2019)).values
    return WP


def apply_projection_GVA(GVA):
    GVA = GVA.copy()
    for ISO in GVA.index.get_level_values('ISO').unique():
        fit = Holt(GVA.loc[ISO, 2000:2020].values).fit(smoothing_level=0.3)
        GVA.loc[ISO, 2020:2050] = fit.forecast(31)

    return GVA


def apply_projection_AIR(AIR, rate=1.05):
    AIR = AIR.copy()
    for i in range(2020, 2051):
        AIR.loc[:, i] = (AIR.loc[:, 2019] * rate ** (i - 2019)).values
    return AIR


def apply_scenario_WRR(WR, rate=0.9):
    WR = WR.copy()
    for i in range(2020, 2051):
        WR.loc[:, i] = (WR.loc[:, 2019] * rate ** (i - 2019)).values
    return WR


def apply_projection(data_dict_expanded):
    data_dict_expanded['IGVA'] = apply_projection_GVA(
        data_dict_expanded['IGVA'])
    data_dict_expanded['AGVA'] = apply_projection_GVA(
        data_dict_expanded['AGVA'])
    data_dict_expanded['SGVA'] = apply_projection_GVA(
        data_dict_expanded['SGVA'])
    data_dict_expanded['GDPC'] = apply_projection_GVA(
        data_dict_expanded['GDPC'])
    data_dict_expanded['AIR'] = apply_projection_AIR(
        data_dict_expanded['AIR'], rate=1.01)
    data_dict_expanded['CL'] = apply_projection_AIR(
        data_dict_expanded['CL'], rate=1.01)

    return data_dict_expanded


MWU_df = pd.read_csv('data/demo_data/MWU_df.csv')

# Conversions
height_rice = 0.2  # meter height of rice
ha_to_m2 = 1e4  # * 1e3
mm_to_m = 1  # 1e-3 TO CHECK
mmyear_to_m3year = 1  # from mm/year to m3/year as 1mm = 10m3/ha \n",

IWW_nodes = {'Kc': {'type': 'parameter', 'unit': '1', 'name': 'Crop Factor'},
             'ICA': {'type': 'input', 'unit': '1000 ha', 'name': 'Cropland area actually irrigated'},
             'CI': {'type': 'variable',
                    'unit': '1',
                    'name': 'Cropping Intensity',
                    'computation': lambda ICA, AIR, **kwargs: ICA / AIR
                    },
             'ETo': {'type': 'input', 'unit': 'mm/year', 'name': 'Evapotranspiration'},
             'ETc': {'type': 'variable',
                     'name': 'Potential Crop Evaporation Vector',
                     'unit': 'mm/year',
                     'computation': lambda Kc, CI, ETo, **kwargs: (Kc * CI * ETo).groupby(level=['ISO']).sum()
                     },
             'ETa': {'type': 'input',
                     'unit': 'mm/year',
                     'name': 'Actual Evapotranspiration'},
             'ICU': {'type': 'variable',
                     'name': 'Irrigation Consumptive',
                     'unit': 'mm/year',
                     # bug to fix
                     'computation': lambda ETc, ETa, **kwargs: abs(ETc - ETa)
                     },
             'AIR': {'type': 'parameter',
                     'unit': '1000 ha',
                     'name': 'Agriculture area actually irrigated'},
             'Arice': {'type': 'parameter',
                       'unit': '1000 ha',
                       'name': 'Area of Rice Paddy Irrigation'},
             'WRR': {'type': 'parameter', 'name': 'Water Requirement Ratio', 'unit': '1'},
             'IWR': {'type': 'variable',
                     'name': ' Irrigation Water Requirement',
                     'unit': '1e9 m3/year',
                     'computation': lambda ICU, AIR, Arice, **kwargs: 1e-9 * ha_to_m2 * mmyear_to_m3year * ((ICU * AIR) + Arice * height_rice)
                     },
             'IWW': {'type': 'variable',
                     'name': ' Irrigation Water Withdrawal',
                     'unit': '1e9 m3/year',
                     'computation': lambda IWR, WRR, **kwargs: IWR / WRR * 1e2
                     },
             'AWU': {'type': 'variable', 'unit': '1e9 m3/year',
                     'name': 'Agricultural Water Withdrawal',
                     'computation': lambda IWW, **kwargs: IWW
                     },
             }


def model_MWU(GDPC, WP, Pop):
    '''Find alternative to hard coding,
    also find way to link the regression data to those coefficient to improve reproducability
    '''

    return np.exp(-0.9522 - 0.3174 * np.log(WP) + 0.5918827 * np.log(GDPC) + 0.9859812 * np.log(Pop)) * 1e-9


MWU_nodes = {'WP': {'type': 'input', 'name': 'Water Price', 'unit': '$/15m3'},
             'GDPC': {'type': 'parameter', 'name': 'GDP per capita', 'unit': '$'},
             'Pop': {'type': 'parameter', 'name': 'Population', 'unit': 'capita'},
             'MWU': {'type': 'variable',
                     'name': 'Municipal Water Withdrawal',
                     'unit': '1e9 m3/year',
                     'computation': lambda GDPC, WP, Pop, **kwargs: model_MWU(GDPC, WP, Pop)
                     }
             }
EW1_nodes = {'IWU': {'type': 'parameter',
                     'name': 'Industrial Water Withdrawal',
                     'unit': '1e9 m3/year'},
             'ICA': {'type': 'input',
                     'unit': '1000 ha',
                     'name': 'Cropland area actually irrigated'},
             'MWU': {'type': 'input',
                     'name': 'Municipal Water Withdrawal',
                     'unit': '1e9 m3/year'},
             'AWU': {'type': 'input',
                     'name': 'Agricultural Water Withdrawal',
                     'unit': '1e9 m3/year'},
             'TWW': {'type': 'variable',
                     'name': 'Total Water Withdrawal',
                     'unit': '1e9 m3/year',
                     'computation': lambda AWU, IWU, MWU, **kwargs: AWU + IWU + MWU
                     },
             'AGVA': {'type': 'input',
                      'name': 'Agricultural Gross Value Added',
                      'unit': '$',
                      },

             'CL': {'type': 'parameter',
                    'unit': '1000 ha',
                    'name': 'Cropland'},
             'PAIR': {'type': 'variable',
                      'name': 'Proportion of Irrigated Cropland',
                      'unit': '1',
                      'computation': lambda ICA, CL, **kwargs: ICA.groupby(level=['ISO']).sum() / CL
                      },
             'Cr': {'type': 'variable',
                    'name': 'Corrective coefficient',
                    'unit': '1',
                    'computation': lambda PAIR, **kwargs: 1 / (1 + (PAIR / (1 - PAIR) * 0.375))
                    },

             'IGVA': {'type': 'parameter',
                      'name': 'Industrial Gross Value Added',
                      'unit': '$'},

             'SGVA': {'type': 'parameter',
                      'name': 'Service Sector Gross Value Added',
                      'unit': '$'},
             'EW1': {'type': 'output',
                     'name': 'Water Use Efficiency',
                     'unit': '$/(m3/year)',
                     'computation': lambda TWW, AGVA, IGVA, SGVA, Cr, **kwargs: (AGVA * (1 - Cr) + IGVA + SGVA) / (TWW * 1e9)
                     },
             }

EW2_nodes = {
    'IRWR': {'type': 'input',
                     'name': 'Internal Renewable Water Resources',
                     'unit': 'm3/year'},
    'ERWR': {'type': 'input',
             'unit': 'm3/year',
             'name': 'External Renewable Water Resources'},
    'TRF': {'type': 'variable',
            'name': 'Total Renewable Freshwater',
            'unit': 'm3/year',
            'computation': lambda IRWR, ERWR, **kwargs: IRWR + ERWR
            },
    'DW': {'type': 'parameter', 'unit': 'm3/year', 'name': 'Desalination Water'},
    'TW': {'type': 'parameter', 'unit': 'm3/year', 'name': 'Treated Wastewater'},
    'TNCW': {'type': 'variable',
             'name': 'Total Non Conventional Water',
             'unit': 'm3/year',
             'computation': lambda DW, TW, **kwargs: DW + TW
             },
    'TFA': {'type': 'variable',
            'name': 'Total Freshwater Available',
            'unit': 'm3/year',
            'computation': lambda TRF, TNCW, **kwargs: TRF + TNCW
            },
    'TWW': {'type': 'input', 'unit': '1e9 m3/year', 'name': 'Total Water Withdrawal'},
    'EFR': {'type': 'parameter',
            'unit': 'm3/year',
            'name': 'Environmental Flow Requirement'},
    'EW2': {'type': 'output',
            'name': 'Share of Freshwater Withdrawal to Freshwater Availability',
            'unit': '%',
            'computation': lambda TWW, TFA, EFR, **kwargs: TWW / (TFA - EFR) * 1e2
            },
    'Natural EW2': {'type': 'output',
                    'name': 'Share of Freshwater Withdrawal to Freshwater Availability',
                    'unit': '%',
                    'computation': lambda TWW, TRF, EFR, **kwargs: TWW / (TRF - EFR) * 1e2
                    }
}

EW_model = GraphModel(concatenate_graph_specs(
    [IWW_nodes, MWU_nodes, EW1_nodes, EW2_nodes]))


# data_dict = df_to_data_dict(MWU_df, ['ICA', 'Kc'])
# data_dict_expanded = expand_data_dict(data_dict)
# data_dict_expanded = apply_projection(data_dict_expanded)

data_dict_expanded = {key.split('.')[0]: pd.read_csv(f"data/demo_data/projection_data/{key.split('.')[0]}.csv", index_col=[
    'ISO', 'Year']).iloc[:, 0] for key in os.listdir('data/demo_data/projection_data')}

data_dict_expanded['ICA'] = pd.read_csv(
    'data/demo_data/projection_data/ICA.csv', index_col=['ISO', 'Year', 'Item']).iloc[:, 0]
data_dict_expanded['Kc'] = pd.read_csv(
    'data/demo_data/projection_data/Kc.csv', index_col=['ISO', 'Year', 'Item']).iloc[:, 0]


def scenario_BAU(data_dict_expanded=data_dict_expanded):

    data_dict_expanded = data_dict_expanded.copy()
    X, y = get_X_y_from_data(EW_model, data_dict_expanded)
    res = EW_model.run(X)

    return res


def scenario_1(data_dict_expanded=data_dict_expanded):

    data_dict_expanded = data_dict_expanded.copy()
    data_dict_expanded['WP'] = apply_scenario_WP(
        data_dict_expanded['WP'], rate=1.1)
    data_dict_expanded['WRR'] = apply_scenario_WRR(
        data_dict_expanded['WRR'], rate=1)

    X, y = get_X_y_from_data(EW_model, data_dict_expanded)
    return EW_model.run(X)


def scenario_2(data_dict_expanded=data_dict_expanded):

    data_dict_expanded = data_dict_expanded.copy()
    data_dict_expanded['WP'] = apply_scenario_WP(
        data_dict_expanded['WP'], rate=1.05)
    data_dict_expanded['WRR'] = apply_scenario_WRR(
        data_dict_expanded['WRR'], rate=1)

    X, y = get_X_y_from_data(EW_model, data_dict_expanded)
    return EW_model.run(X)


def scenario(data_dict_expanded=data_dict_expanded, WP_rate=1, WRR_rate=1):
    data_dict_expanded = data_dict_expanded.copy()
    data_dict_expanded['WP'] = apply_scenario_WP(
        data_dict_expanded['WP'], rate=WP_rate)
    data_dict_expanded['WRR'] = apply_scenario_WRR(
        data_dict_expanded['WRR'], rate=WRR_rate)

    X, y = get_X_y_from_data(EW_model, data_dict_expanded)
    return EW_model.run(X)


res_1 = scenario()
res_2 = scenario(WP_rate=1.05, WRR_rate=1)
res_3 = scenario(WP_rate=1.1, WRR_rate=0.999)
