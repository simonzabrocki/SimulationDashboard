from ggmodel_dev.projection import *
from ggmodel_dev.models.water.EW import model_dictionnary


projection_dict = {
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


def run_scenario(data_dict, WP_rate=1.05, WRR_rate=1.01):
    
    data_dict = data_dict.copy()

    scenario_projection_dict = {
        'WP': lambda x: apply_annual_rate_projection(x, WP_rate),
        'WRR': lambda x: apply_annual_rate_projection(x, WRR_rate),
    }
    
    data_dict = run_projection(scenario_projection_dict, data_dict)

    results = model_dictionnary['EW_model'].run(data_dict)

    return results
    
