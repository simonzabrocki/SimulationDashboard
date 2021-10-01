from ggmodel_dev.projection import *
from ggmodel_dev.models.material.RECYCLE import model_dictionnary

MODEL = model_dictionnary['RECYCLE_model']


PROJECTION_DICT = {
    'DMCi': lambda x: x,
    'LDi_mu': lambda x: x,
    'LDi_std':lambda x: x,
    'year': lambda x: x,
 }



def run_recursive(X, t0, tmax):
    X = X.copy()
    X['SBMi'] = model_dictionnary['SBMi_model'].run(X)
    X['RMSi_t_minus_1'] = pd.Series(data=0, index=X['DMCi'].index)
    
    RMSi = pd.Series(data=np.nan, index=X['DMCi'].index)
    OUTFLOWi = pd.Series(data=np.nan, index=X['DMCi'].index)
    MSi = pd.Series(data=np.nan, index=X['DMCi'].index)
    WASTEi = pd.Series(data=np.nan, index=X['DMCi'].index)
    
    for year in range(t0 + 1, tmax):
        X['year'] = year
        res = model_dictionnary['MUE_model'].run(X)
        X['RMSi_t_minus_1'].loc[:, :, year] = res['RMSi']
        
        RMSi.loc[:, :, year-1] = res['RMSi']
        OUTFLOWi.loc[:, :, year-1] = res['OUTFLOWi']
        MSi.loc[:, :, year-1] = res['MSi']
        WASTEi.loc[:, :, year-1] = res['WASTEi']
        
    res['RMSi'] = RMSi
    res['OUTFLOWi'] = OUTFLOWi
    res['MSi'] = MSi
    res['WASTEi'] = WASTEi

    return res



def run_scenario(data_dict, RRi=0.1, MLOSSi=0, PLOSSi=0):
    
    data_dict = data_dict.copy()
    data_dict['RRi'] = RRi


    MLOSSi = pd.Series(index=['Biomass', 'Fossil fuels', 'Metal ores', 'Non-metallic minerals'], data=[1, 1, 0.1255, 0.04])
    PLOSSi = pd.Series(index=['Biomass', 'Fossil fuels', 'Metal ores', 'Non-metallic minerals'], data=[1, 1, 0.6925, 0.35])
    MLOSSi.index.name = 'Item'
    PLOSSi.index.name = 'Item'

    data_dict['PLOSSi'] = PLOSSi
    data_dict['MLOSSi'] = MLOSSi 

    results = run_recursive(data_dict, t0=1970, tmax=2017)
    return results
    

def run_all_scenarios(data_dict, args_dict_1, args_dict_2):
    scenarios_results = {}


    # TO BE PUT IN DB !!!!!
    LDi_mu = pd.Series(index=['Biomass', 'Fossil fuels', 'Metal ores', 'Non-metallic minerals'], data=[0, 0, 26, 50])
    LDi_std = pd.Series(index=['Biomass', 'Fossil fuels', 'Metal ores', 'Non-metallic minerals'], data=[1e-10, 1e-10, 8, 16.6])
    data_dict['LDi_mu'] = LDi_mu
    data_dict['LDi_std'] = LDi_std


    #data_dict = run_projection(PROJECTION_DICT, data_dict)

    scenarios_results['BAU'] = run_scenario(data_dict, RRi=0.1)
    scenarios_results['scenario_one'] = run_scenario(data_dict, **args_dict_1)
    scenarios_results['scenario_two'] = run_scenario(data_dict, **args_dict_2)

    return scenarios_results
