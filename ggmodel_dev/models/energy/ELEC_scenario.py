from ggmodel_dev.projection import *
from ggmodel_dev.models.energy.ELEC import model_dictionnary


def run_scenario(data_dict):

    data_dict = data_dict.copy()

    scenario_projection_dict = {
        'EFELECGHGi': lambda x: x,
        'ELECPRODi': lambda x: x,
        'WWFUELCOOLi': lambda x: x,
    }

    data_dict = run_projection(scenario_projection_dict, data_dict)

    results = model_dictionnary['ELEC_model'].run(data_dict)

    return results
