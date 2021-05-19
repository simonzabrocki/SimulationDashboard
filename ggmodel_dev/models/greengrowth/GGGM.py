from ggmodel_dev.graphmodel import merge_models
from ggmodel_dev.utils import get_model_properties
from ggmodel_dev.models.landuse import BE2, SL1_BE3, GE3
from ggmodel_dev.models.water import EW

def flatten_dictionary(dictionary):
    
    flat_dictionary = {}
    
    for dict_name, dict in dictionary.items():
        flat_dictionary.update({k: v for k, v in dict.items()})
        
    return flat_dictionary

def merge_model_dictionary():
    '''To improve'''
    model_dictionary = {}
    model_dictionary['BE2'] = BE2.model_dictionnary
    model_dictionary['SL1_BE3'] = SL1_BE3.model_dictionnary
    model_dictionary['GE3'] = GE3.model_dictionnary
    model_dictionary['EW'] = EW.model_dictionnary

    return flatten_dictionary(model_dictionary)


def merge_model_properties():
    '''To improve'''
    model_properties = {}
    model_properties['BE2'] = BE2.model_properties
    model_properties['SL1_BE3'] = SL1_BE3.model_properties
    model_properties['GE3'] = GE3.model_properties
    model_properties['EW'] = EW.model_properties

    return flatten_dictionary(model_properties)

all_model_dictionary = merge_model_dictionary()
all_model_properties = merge_model_properties()

GreenGrowthModel = merge_models([model for _, model in all_model_dictionary.items()])

model_dictionnary = {'GGGM_model': GreenGrowthModel}

model_properties = get_model_properties('models/greengrowth/GGGM_properties.json')

all_model_dictionary.update(model_dictionnary)
all_model_properties.update(model_properties)