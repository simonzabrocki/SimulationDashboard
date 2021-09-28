from statsmodels.tsa.api import ExponentialSmoothing, SimpleExpSmoothing, Holt
import pandas as pd
import numpy as np


def reindex_series_non_itemized(df, min_year=2000, max_year=2050):
    multi_index = pd.MultiIndex.from_product([df.index.get_level_values(
        'ISO').unique(), np.arange(min_year, max_year+1)], names=['ISO', 'Year'])
    return df.reindex(multi_index)


def reindex_series_itemized(df, min_year=2000, max_year=2050):
    multi_index = pd.MultiIndex.from_product([df.index.get_level_values('ISO').unique(), np.arange(
        min_year, max_year+1), df.index.get_level_values('Item').unique()], names=['ISO', 'Year', 'Item'])
    return df.reindex(multi_index)


def apply_percent_target_projection(series, percent_target=0, min_year=2000, baseline_year=2018, target_year=2050):
    series = series.copy()
    series = reindex_series_non_itemized(series, min_year=min_year, max_year=target_year)
    series.loc[:, target_year, :] = percent_target * \
        series.loc[:, baseline_year, :].values
    return series.interpolate()


def apply_target_projection(series, target=0, min_year=2000, baseline_year=2018, target_year=2050, final_year=2050):
    series = series.copy()
    series = reindex_series_non_itemized(series, min_year=min_year, max_year=final_year)
    series.loc[:, target_year:final_year+1, :] = target
    return series.interpolate()



def apply_itemized_percent_target_projection(series, percent_target=0, min_year=2000, baseline_year=2018, target_year=2050):
    '''To improve: Apply item wise projection'''
    series = series.copy()
    series = reindex_series_itemized(series, min_year=min_year, max_year=target_year)

    series.loc[:, baseline_year+1:, :] = np.nan # remove points after baseline year to have consistent projection
    series.loc[:, target_year, :] = percent_target * \
        series.loc[:, baseline_year, :].values

    return series.groupby(level=['ISO', 'Item']).apply(lambda x: x.interpolate())


def apply_annual_rate_projection(series, rate=1, min_year=2000, baseline_year=2018, target_year=2050):
    series = series.copy()
    series = reindex_series_non_itemized(series, min_year=min_year, max_year=target_year)

    year = series.loc[:, baseline_year:].index.get_level_values(
        level='Year').values

    series.loc[:, baseline_year:] = series.loc[:,
                                               baseline_year].values * rate ** (year - baseline_year)

    return series


def apply_constant_projection(series, constant=0, min_year=2000, baseline_year=2018, target_year=2050):
    series = series.copy()
    series = reindex_series_non_itemized(series, min_year=min_year, max_year=target_year)
    series.loc[:, baseline_year:] = constant

    return series


def apply_itemized_ffill_projection(series,min_year=2000, target_year=2050):
    '''To improve: Apply item wise projection'''
    series = series.copy()
    series = reindex_series_itemized(series, min_year=min_year, max_year=target_year)

    return series.groupby(['ISO', 'Item']).fillna(method='ffill')


def apply_ffill_projection(series, min_year=2000, target_year=2050):
    series = series.copy()
    series = reindex_series_non_itemized(series, min_year=min_year, max_year=target_year)

    return series.groupby(['ISO']).fillna(method='ffill')


def apply_Holt_projection(series, min_year=2000, baseline_year=2018, target_year=2050, smoothing_level=0.3):
    '''Improve choice of smoothing methods'''
    series = series.copy()
    series = reindex_series_non_itemized(series, min_year=min_year, max_year=target_year)

    for ISO in series.index.get_level_values('ISO').unique():
        fit = Holt(series.loc[ISO, :baseline_year].values).fit(
            smoothing_level=smoothing_level)
        series.loc[ISO, baseline_year:target_year +
                   1] = fit.forecast(target_year - baseline_year + 1)

    return series


def run_projection(projection_dict, data_dict):
    data_dict = data_dict.copy()

    for variable, function in projection_dict.items():
        data_dict[variable] = function(data_dict[variable])

    return data_dict


def run_scenario_list(scenario_function,
                      list_of_scenarios,
                      projection_dictionnary,
                      data_dict,
                      ):
    
    proj_data_dict = run_projection(projection_dictionnary, data_dict.copy())

    results = {}
    
    for i, args in enumerate(list_of_scenarios):
        results[f'scenario_{i}'] = scenario_function(proj_data_dict, **args)
        
    return results