# from ggmodel_dev.projection import *
# from ggmodel_dev.models.landuse.GE3 import model_dictionnary

# projection_dict = {
#     'Pop': lambda x: x,
#     'OEi': lambda x: x,
#     'EF_EEi': lambda x: x,
#     'TAi': lambda x: x,
#     'IN_F': lambda x: x,
#     'MYi': lambda x: x,
#     'EF_ASi': lambda x: x,
#     'EF_Ti': lambda x: x,
#     'EF_CH4Ti': lambda x: x,
#     'EF_Li': lambda x: x,
#     'EF_F': lambda x: x,        
# }


# def run_scenario(data_dict, MM_Ti=1/3, MM_ASi=1/3, MM_LPi=1/3):
    
#     data_dict = data_dict.copy()
    
#     data_dict['MM_Ti'] = MM_Ti
#     data_dict['MM_ASi'] = MM_ASi
#     data_dict['MM_LPi'] = MM_LPi
    
#     results = model_dictionnary['GE3_model'].run(data_dict)
    
#     return results

from ggmodel_dev.projection import *
from ggmodel_dev.models.landuse.GE3 import model_dictionnary

projection_dict = {
    'Pop': lambda x: x,
    'OEi': lambda x: x,
    'EF_EEi': lambda x: x,
    'TAi': lambda x: x,
    'IN_F': lambda x: x,
    'MYi': lambda x: x,
    'EF_ASi': lambda x: x,
    'EF_Ti': lambda x: x,
    'EF_CH4Ti': lambda x: x,
    'EF_Li': lambda x: x,
    'EF_F': lambda x: x,        
}


def run_scenario(data_dict,
                 MM_Ti=1/3,
                 MM_ASi=1/3,
                 MM_LPi=1/3,
                 TAi_pct_Asses=1,
                 TAi_pct_Cattle_dairy=1,
                 TAi_pct_Cattle_non_dairy=1,
                 TAi_pct_Chickens_broilers=1,
                 TAi_pct_Chickens_layers=1,
                 TAi_pct_Ducks=1,
                 TAi_pct_Goats=1,
                 TAi_pct_Horses=1,
                 TAi_pct_Mules=1,
                 TAi_pct_Sheep=1,
                 TAi_pct_Swine_breeding=1,
                 TAi_pct_Swine_market=1,
                 TAi_pct_Turkeys=1
                 ):
    
    data_dict = data_dict.copy()
    
    
    # data_dict['MM_Ti'] = MM_Ti
    # data_dict['MM_ASi'] = MM_ASi
    # data_dict['MM_LPi'] = MM_LPi
    data_dict['MM_Ti'] = pd.Series(data=MM_Ti, index=data_dict['MM_Ti'].index)
    data_dict['MM_ASi'] = pd.Series(data=MM_ASi, index=data_dict['MM_Ti'].index)
    data_dict['MM_LPi'] = pd.Series(data=MM_LPi, index=data_dict['MM_Ti'].index)
    
    TAi_pct_target = pd.Series(index=['Asses', 'Cattle, dairy','Cattle, non-dairy',
                                  'Chickens, broilers', 'Chickens, layers', 'Ducks', 'Goats',
                                  'Horses', 'Mules', 'Sheep', 'Swine, breeding', 'Swine, market',
                                  'Turkeys'],
                           data=[TAi_pct_Asses, TAi_pct_Cattle_dairy,
                                 TAi_pct_Cattle_non_dairy, TAi_pct_Chickens_broilers,
                                 TAi_pct_Chickens_layers, TAi_pct_Ducks,TAi_pct_Goats,
                                 TAi_pct_Horses, TAi_pct_Mules ,TAi_pct_Sheep, TAi_pct_Swine_breeding,
                                 TAi_pct_Swine_market, TAi_pct_Turkeys
                               
                           ], name='TAi_pct_target')
    
    TAi_pct_target.index.name = 'Item'
    
    tmp = pd.merge(data_dict['TAi'].reset_index(), TAi_pct_target.reset_index(),on='Item')
    tmp['TAi'] = tmp['TAi'] * tmp['TAi_pct_target']

    data_dict['TAi'] = tmp.set_index(['ISO', 'Year', 'Item'])['TAi']
    
    results = model_dictionnary['GE3_model'].run(data_dict)
    
    return results