from ggmodel_dev.projection import *
from ggmodel_dev.models.water.EW import model_dictionnary

MODEL = model_dictionnary['EW_model']


PROJECTION_DICT = {
    'IGVA': lambda x: apply_Holt_projection(x),
    'SGVA': lambda x: apply_Holt_projection(x),
    'AGVA': lambda x: apply_Holt_projection(x),
    'GDPC': lambda x: apply_Holt_projection(x),
    'Pop': lambda x: apply_Holt_projection(x),
    'AIR': lambda x: apply_annual_rate_projection(x, rate=1.01),
    'CL': lambda x: apply_annual_rate_projection(x, rate=1.01),
    'Arice': lambda x: apply_annual_rate_projection(x, rate=1.01),
    'ETo': lambda x: apply_ffill_projection(x),
    'ETa': lambda x: apply_ffill_projection(x),
    'IRWR': lambda x: apply_ffill_projection(x),
    'ERWR': lambda x: apply_ffill_projection(x),
    'IWU': lambda x: apply_ffill_projection(x),
    'DW': lambda x: apply_ffill_projection(x),
    'TW': lambda x: apply_ffill_projection(x),
    'EFR': lambda x: apply_ffill_projection(x),
 }


def IRRTECH_projection(x, IRRTECH_sprinkler, IRRTECH_surface, IRRTECH_drip):
    series = reindex_series_itemized(x)

    series.loc[:, 2050, 'Sprinkler'] = IRRTECH_sprinkler / 100
    series.loc[:, 2050, 'Surface'] = IRRTECH_surface / 100
    series.loc[:, 2050, 'Drip'] = IRRTECH_drip / 100
    
    series = series.groupby(['Item']).apply(lambda x: x.interpolate()).groupby(['Item']).bfill()
    
    return series 

def run_scenario(data_dict, WP_rate=1.0, WRR_rate=1.00, IRRTECH_sprinkler=10, IRRTECH_surface=80, IRRTECH_drip=10):
    
    data_dict = data_dict.copy()
    
    
    scenario_projection_dict = {
        'WP': lambda x: apply_annual_rate_projection(x, WP_rate),
        #'WRR': lambda x: apply_annual_rate_projection(x, WRR_rate),
        'IRRTECHi': lambda x: IRRTECH_projection(x, IRRTECH_sprinkler, IRRTECH_surface, IRRTECH_drip),
    }
    
    data_dict = run_projection(scenario_projection_dict, data_dict)

    results = MODEL.run(data_dict)

    return results
    

def run_all_scenarios(data_dict, args_dict_1, args_dict_2):
    scenarios_results = {}

    data_dict = run_projection(PROJECTION_DICT, data_dict)

    scenarios_results['BAU'] = run_scenario(data_dict)
    scenarios_results['scenario_one'] = run_scenario(data_dict, **args_dict_1)
    scenarios_results['scenario_two'] = run_scenario(data_dict, **args_dict_2)

    return scenarios_results