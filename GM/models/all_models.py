from GM.models.Sarah.model_EW import EW_models
from GM.models.Sarah.model_material import material_models
from GM.models.Hermen.model_GE3 import GE3_models
from GM.models.Hermen.model_SL1_BE3 import BE3_SL1_models
from GM.models.Hermen.model_BE2 import BE2_models


all_models = {}

all_models['EW_models'] = EW_models
all_models['material_models'] = material_models
all_models['GE3_models'] = GE3_models
all_models['BE3_SL1_models'] = BE3_SL1_models
all_models['BE2_models'] = BE2_models
