from ggmodel_dev.projection import *
from ggmodel_dev.models.landuse.BE2 import model_dictionnary

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
    'CL_corr_coef': lambda x: apply_ffill_projection(x),
 }


def run_scenario(data_dict, FDKGi_target=1, FLOi_target=1, CYi_target=1, R_rate=1):

    data_dict = data_dict.copy()

    projection_dict = {
        'CYi': lambda x: apply_itemized_percent_target_projection(x, CYi_target),
        'FDKGi': lambda x: apply_itemized_percent_target_projection(x, FDKGi_target),
        'FLOi': lambda x: apply_itemized_percent_target_projection(x, FLOi_target),
        'R_rate': lambda x: apply_constant_projection(x, R_rate)
    }

    data_dict = run_projection(projection_dict, data_dict)

    results = model_dictionnary['BE2_model'].run(data_dict)

    results['CL_baseline'] = pd.Series(results['CL'].loc[:, 2018].values[0], index=results['CL'].index) # to avoid discontinuty, to improve
    
    results = model_dictionnary['BE2_model'].run(results)

    return results