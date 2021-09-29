from ggmodel_dev.projection import *
from ggmodel_dev.models.landuse.BE2 import model_dictionnary


MODEL = model_dictionnary['BE2_model']

PROJECTION_DICT = {
    'FDi': lambda x: apply_itemized_ffill_projection(x, min_year=2018),
    'SSRi': lambda x: apply_itemized_ffill_projection(x, min_year=2018),
    'SVi': lambda x: apply_itemized_ffill_projection(x, min_year=2018),
    'RDi': lambda x: apply_itemized_ffill_projection(x, min_year=2018),
    'NFDi': lambda x: apply_itemized_ffill_projection(x, min_year=2018),
    'FEi': lambda x: apply_itemized_ffill_projection(x, min_year=2018),
    'FIi': lambda x: apply_itemized_ffill_projection(x, min_year=2018),
    'PDi': lambda x: apply_itemized_ffill_projection(x, min_year=2018),
    'FDi': lambda x: apply_itemized_ffill_projection(x, min_year=2018),
    'SDi': lambda x: apply_itemized_ffill_projection(x, min_year=2018),
    'TLA': lambda x: apply_ffill_projection(x, min_year=2018),
    'CL_baseline': lambda x: apply_ffill_projection(x, min_year=2018),
    'IL_baseline': lambda x: apply_ffill_projection(x, min_year=2018),
    'FL_baseline': lambda x: apply_ffill_projection(x, min_year=2018),
    'Pop': lambda x: apply_ffill_projection(x, min_year=2018),
    'CL_corr_coef': lambda x: apply_ffill_projection(x, min_year=2018),
 }


def run_scenario(data_dict, FDKGi_target=1, FLOi_target=1, CYi_target=1, R_rate=1):

    data_dict = data_dict.copy()

    projection_dict = {
        'CYi': lambda x: apply_itemized_percent_target_projection(x, CYi_target, min_year=2018),
        'FDKGi': lambda x: apply_itemized_percent_target_projection(x, FDKGi_target, min_year=2018),
        'FLOi': lambda x: apply_itemized_percent_target_projection(x, FLOi_target, min_year=2018),
        #'R_rate': lambda x: apply_constant_projection(x, R_rate)
        'R_rate': lambda x: apply_target_projection(x, R_rate, target_year=2050, min_year=2018)

    }

    data_dict = run_projection(projection_dict, data_dict)

    results = MODEL.run(data_dict)

    results['CL_baseline'] = pd.Series(results['CL'].loc[:, 2018].values[0], index=results['CL'].index) # to avoid discontinuty, to improve
    
    results = MODEL.run(results)

    return results


def run_all_scenarios(data_dict, args_dict_1, args_dict_2):
    scenarios_results = {}

    data_dict = run_projection(PROJECTION_DICT, data_dict)

    scenarios_results['BAU'] = run_scenario(data_dict)
    scenarios_results['scenario_one'] = run_scenario(data_dict, **args_dict_1)
    scenarios_results['scenario_two'] = run_scenario(data_dict, **args_dict_2)

    return scenarios_results