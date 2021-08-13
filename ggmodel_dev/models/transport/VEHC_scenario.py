from ggmodel_dev.projection import *
from ggmodel_dev.models.transport.VEHC import model_dictionnary


def run_scenario(data_dict, MAX_sat=1000, GDPC_rate=1.05):

    data_dict = data_dict.copy()

    data_dict['MAX_sat'] = pd.Series(
        data=data_dict['MAX_sat'].values[0], index=data_dict['GDPC'].index, name='MAX_sat')

    scenario_projection_dict = {
        'MAX_sat': lambda x: apply_target_projection(x, MAX_sat),
        'GDPC': lambda x: apply_annual_rate_projection(x, GDPC_rate),
    }

    data_dict = run_projection(scenario_projection_dict, data_dict)

    results = model_dictionnary['VEHC_model'].run(data_dict)

    return results
