from ggmodel_dev.graphmodel import GraphModel
from ggmodel_dev.utils import get_model_properties
import numpy as np

NUTRIENT_nodes = {
    "AD": {
        "name": "Atmospheric N deposition",
        "type": "input",
        "unit": "tonnes N"
    },
    "BF": {
        "name": "Biological N fixation",
        "type": "input",
        "unit": "tonnes N"
    },
    "CL": {
        "name": "Cropland",
        "type": "input",
        "unit": "1000 ha"
    },
    "CNObaseline": {
        "name": "Total nitrogen content of crops in the baseline year",
        "type": "input",
        "unit": "tonnes N"
    },
    "CNYbaseline": {
        "name": "Crop nitrogen yields per unit of output",
        "type": "variable",
        "unit": "N/tonnes",
        "computation": lambda CNObaseline, FPi, **kwargs: CNObaseline * FPi.sum() * 1e3
    },
    "FPi": {
        "name": "Food production per food group",
        "type": "input",
        "unit": "1000 tonnes"
    },
    "FU": {
        "name": "Total fertilizer use",
        "type": "variable",
        "unit": "tonnes",
        "computation": lambda CL, FUrate, **kwargs: CL * FUrate
    },
    "FUBaseline": {
        "name": "Total fertilizer use in the baseline year",
        "type": "input",
        "unit": "tonnes"
    },
    "FUrate": {
        "name": "Cropland fertilizer application rate",
        "type": "variable",
        "unit": "kg/ha",
        "computation": lambda FUBaseline, TDCbaseline, **kwargs : FUBaseline / TDCbaseline
    },
    "F_subsidy": {
        "name": "Fertilizer subsidy",
        "type": "input",
        "unit": "Million $"
    },
    "IN_F": {
        "name": "Agricultural Use in nutrients",
        "type": "variable",
        "unit": "kg",
        "computation": lambda FU, **kwargs: 1, # Missing delta_C 
    },
    "MASi": {
        "name": "Vector manure applied to soil",
        "type": "input",
        "unit": "kg N"
    },
    "OUT_C": {
        "name": "Crop output",
        "type": "variable",
        "unit": "tonnes N",
        "computation": lambda FPi, CNYbaseline, **kwargs: (FPi * CNYbaseline) * 1e3
    },
    "P_fu": {
        "name": "Fertilizer price",
        "type": "input",
        "unit": "$/mt"
    },
    "SL1": {
        "name": "Nutrient balance",
        "type": "variable",
        "unit": "tonnes N",
        "computation": lambda MASi, IN_F, BF, AD, OUT_C, **kwargs: MASi.sum() * 1e-3 + IN_F + BF + AD - OUT_C
    },
    "TDCbaseline": {
        "name": "Total cropland area in the baseline year",
        "type": "input",
        "unit": "ha"
    },
    "deltaFU": {
        "name": "Change in fertilizer consumption",
        "type": "variable",
        "unit": "tonnes",
        "computation": lambda FU, epsilon_fertilizer, P_fu, F_subsidy, **kwargs: 1 /2 * ((-FU + np.sqrt(FU ** 2 - 4 * epsilon_fertilizer * P_fu * FI * F_subsidy) / P_fu))
    },
    "epsilon_fertilizer": {
        "name": "Price elasticity for fertilizer",
        "type": "input",
        "unit": "1"
    }
}


NUTRIENT_model = GraphModel(NUTRIENT_nodes)

model_dictionnary = {'NUTRIENT_model': NUTRIENT_model}

model_properties = get_model_properties('models/landuse/NUTRIENT_properties.json')