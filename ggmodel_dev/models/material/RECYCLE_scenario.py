from ggmodel_dev.projection import *
from ggmodel_dev.models.material.RECYCLE import model_dictionnary

projection_dict = {
    'DMCi': lambda x: x,
    'LDi_mu': lambda x: x,
    'LDi_std':lambda x: x,
    'year': lambda x: x,
 }


def run_scenario(data_dict, RRi=0.1):
    
    data_dict = data_dict.copy()
    data_dict['RRi'] = RRi

    # scenario_projection_dict = {}
    
    # data_dict = run_projection(scenario_projection_dict, data_dict)

    results = model_dictionnary['RECYCLE_model'].run_recursive(data_dict,
                                  rec_vars=[('RMSi', 'RMSi_t_minus_1')],
                                  initials=[1e6],
                                  t0=1970,
                                      tmax=2017,
                  templates=[pd.Series(data=np.nan, index=data_dict['DMCi'].index)])

    return results
    
