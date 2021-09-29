from ggmodel_dev.projection import *
from ggmodel_dev.models.transport.VEHC import model_dictionnary

MODEL = model_dictionnary['VEHC_model']

def run_scenario(data_dict, MAX_sat=1000, GDPC_rate=1.05):

    data_dict = data_dict.copy()

    data_dict['MAX_sat'] = pd.Series(
        data=data_dict['MAX_sat'].values[0], index=data_dict['GDPC'].index, name='MAX_sat')

    scenario_projection_dict = {
        'MAX_sat': lambda x: apply_target_projection(x, MAX_sat),
        'GDPC': lambda x: apply_annual_rate_projection(x, GDPC_rate),
    }

    data_dict = run_projection(scenario_projection_dict, data_dict)

    results = MODEL.run(data_dict)

    return results

def run_all_scenarios(data_dict, args_dict_1, args_dict_2):
    scenarios_results = {}

    scenarios_results['BAU'] = run_scenario(data_dict, MAX_sat=data_dict['MAX_sat'], GDPC_rate=1.02)
    scenarios_results['scenario_one'] = run_scenario(data_dict, **args_dict_1)
    scenarios_results['scenario_two'] = run_scenario(data_dict, **args_dict_2)

    return scenarios_results
