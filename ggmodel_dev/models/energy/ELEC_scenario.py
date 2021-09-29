from ggmodel_dev.projection import *
from ggmodel_dev.models.energy.ELEC import model_dictionnary


MODEL = model_dictionnary['ELEC_model']


def run_scenario(data_dict):

    data_dict = data_dict.copy()

    scenario_projection_dict = {
        'EFELECGHGi': lambda x: x,
        'ELECPRODi': lambda x: x,
        'WWFUELCOOLi': lambda x: x,
    }

    data_dict = run_projection(scenario_projection_dict, data_dict)

    results = MODEL.run(data_dict)

    return results

def run_all_scenarios(data_dict, args_dict_1, args_dict_2):
    scenarios_results = {}

    scenarios_results['BAU'] = run_scenario(data_dict=data_dict, **args_dict_1, **args_dict_2)

    return scenarios_results