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


def run_scenario(data_dict, MM_Ti=1/3, MM_ASi=1/3, MM_LPi=1/3):
    
    data_dict = data_dict.copy()
    
    data_dict['MM_Ti'] = MM_Ti
    data_dict['MM_ASi'] = MM_ASi
    data_dict['MM_LPi'] = MM_LPi
    
    results = model_dictionnary['GE3_model'].run(data_dict)
    
    return results