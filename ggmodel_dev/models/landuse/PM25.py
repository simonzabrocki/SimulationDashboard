from ggmodel_dev.graphmodel import GraphModel
from ggmodel_dev.utils import get_model_properties

PM25_nodes = {
    "AEUi": {
        "name": "Total agricultural energy use per type",
        "type": "input",
        "unit": "TWH"
    },
    "BMB": {
        "name": "Total biomass burned",
        "type": "input",
        "unit": "kg dm"
    },
    "ECR_PM25eq": {
        "name": "PM25 emissions from burning crop residues",
        "type": "variable",
        "unit": "tonnes",
        "computation": lambda BMB, EFCRBI_pm25, **kwargs: BMB * EFCRBI_pm25
    },
    "EFCRBI_pm25": {
        "name": "Emission factors burning crop residues",
        "type": "input",
        "unit": "kg/mg waste"
    },
    "EFPM25Ai": {
        "name": "Emission factor PM2.5 from live animals",
        "type": "input",
        "unit": "kg/heads"
    },
    "EFPM25Ci": {
        "name": "Emission factors PM2.5 from crops",
        "type": "input",
        "unit": "kg/ha"
    },
    "EFPM25Ei": {
        "name": "Emission factors PM2.5 agricultural fuel consumption",
        "type": "input",
        "unit": "g/tonne fuel"
    },
    "PM25": {
        "name": "Total agricultural PM25 emissions",
        "type": "variable",
        "unit": "tonnes",
        "computation": lambda PM25A, PM25C, PM25E, ECR_PM25eq, **kwargs: PM25A + PM25C + PM25E + ECR_PM25eq
    },
    "PM25A": {
        "name": "PM25 emissions from live animals",
        "type": "variable",
        "unit": "tonnes",
        "computation": lambda TAi, EFPM25Ai, **kwargs: (TAi * EFPM25Ai).sum() 
    },
    "PM25C": {
        "name": "PM25 emissions from crops",
        "type": "variable",
        "unit": "tonnes",
        "computation": lambda TCLDi, EFPM25Ci, **kwargs: (TCLDi * EFPM25Ci).sum()
    },
    "PM25E": {
        "name": "PM25 emissions from agricultural energy use",
        "type": "variable",
        "unit": "tonnes",
        "computation": lambda AEUi, EFPM25Ei, **kwargs: (AEUi * EFPM25Ei).sum()         
    },
    "TAi": {
        "name": "Total animal population",
        "type": "input",
        "unit": "head"
    },
    "TCLDi": {
        "name": "Cropland demand",
        "type": "input",
        "unit": "ha"
    }
}

PM25_model = GraphModel(PM25_nodes)

model_dictionnary = {"PM25_model": PM25_model}

model_properties = get_model_properties('models/landuse/PM25_properties.json')