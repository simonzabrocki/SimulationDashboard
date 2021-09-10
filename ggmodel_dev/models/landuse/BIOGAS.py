from ggmodel_dev.graphmodel import GraphModel
from ggmodel_dev.utils import get_model_properties


BIOGAS_nodes = {
    "BioCropMixi": {
        "name": "Allocation of crops for biodiesel production",
        "type": "input",
        "unit": "1"
    },
    "BioDiesLandi": {
        "name": "Total land for biodiesel crops",
        "type": "variable",
        "unit": "ha",
        "computation": lambda CropBioDiesSupplyi, CropBioDiesYi, **kwargs: CropBioDiesSupplyi / CropBioDiesYi
    },
    "BioDieselDemand": {
        "name": "Total demand for biodiesel",
        "type": "input",
        "unit": "TJ"
    },
    "BioDieselResiduei": {
        "name": "Residues for biodiesel  (i.e. animal fats)",
        "type": "input",
        "unit": "kg"
    },
    "BioDieselYi": {
        "name": "Biodiesel yields",
        "type": "input",
        "unit": "L/kg residue"
    },
    "BioEthConversionMJ": {
        "name": "Conversion factor bioethanol",
        "type": "input",
        "unit": "L/TJ"
    },
    "BioEthDemand": {
        "name": "Total demand for bioethanol",
        "type": "input",
        "unit": "TJ"
    },
    "BioEthLandi": {
        "name": "Total land for bioethanol crops",
        "type": "variable",
        "unit": "ha",
        "computation": lambda CropBioEthSupply, CropBioEthYi, **kwargs: CropBioEthSupply / CropBioEthYi
    },
    "BiogasConversionMJ": {
        "name": "Conversion factor biogas",
        "type": "input",
        "unit": "m3/MJ"
    },
    "BiogasYi": {
        "name": "Methane yields from manure",
        "type": "input",
        "unit": "m3/kg VS"
    },
    "BodyMassi": {
        "name": "Average adult body mass of animal",
        "type": "input",
        "unit": "kg"
    },
    "CLBIO": {
        "name": "Total land demand for biofuels",
        "type": "output",
        "unit": "ha",
        "computation": lambda BioEthLandi, BioDiesLandi, **kwargs: BioEthLandi.sum() + BioDiesLandi.sum()
    },
    "CropBioDiesSupplyi": {
        "name": "Total demand for biodiesel from dedicated crops",
        "type": "variable",
        "unit": "TJ",
        "computation": lambda BioDieselDemand, RBioDiesSupplyi, BioCropMixi, **kwargs: BioCropMixi * (BioDieselDemand - RBioDiesSupplyi)
    },
    "CropBioDiesYi": {
        "name": "Biodiesel yields from crops",
        "type": "input",
        "unit": "TJ/km2"
    },
    "CropBioEthSupply": {
        "name": "Total demand for bioethanol from dedicated crops",
        "type": "variable",
        "unit": "TJ",
        "computation": lambda BioEthDemand, RBioEthSupply, EthCropMixi, **kwargs: EthCropMixi * (BioEthDemand - RBioEthSupply)
    },
    "CropBioEthYi": {
        "name": "Bioethanol yields from crops",
        "type": "input",
        "unit": "TJ/km2"
    },
    "EthCropMixi": {
        "name": "Allocation of crops for bioethanol production",
        "type": "input",
        "unit": "1"
    },
    "EthYi": {
        "name": "Bioethanol yields",
        "type": "input",
        "unit": "L/kg dm biomass"
    },
    "MBiogasTJ": {
        "name": "Total biogas production from manure",
        "type": "variable",
        "unit": "TJ",
        "computation": lambda Mbiogasi, BiogasConversionMJ, **kwargs: (Mbiogasi * BiogasConversionMJ).sum()
    },
    "MMASi": {
        "name": "% of total manure applied to soils",
        "type": "input",
        "unit": "%"
    },
    "MMLPi": {
        "name": "Fraction of manure left on pasture",
        "type": "input",
        "unit": "%"
    },
    "ManureKGi": {
        "name": "Total manure production in kg",
        "type": "variable",
        "unit": "kg",
        "computation": lambda TAi, BodyMassi, MprodDAYi, **kwargs: 1
    },
    "ManureVSi": {
        "name": "total manure production in kg volatile solids",
        "type": "variable",
        "unit": "kg",
        "computation": lambda TAi, BodyMassi, VSprodDAYi, **kwargs: TAi * BodyMassi * VSprodDAYi * 365 * 1e-6
    },
    "Mbioenergyi": {
        "name": "Manure available for bioenergy",
        "type": "variable",
        "unit": "kg VS",
        "computation": lambda ManureVSi, MMLPi, MMASi, **kwargs: ManureVSi * (1 - MMLPi) * MMASi
    },
    "Mbiogasi": {
        "name": "Total biogas production from manure",
        "type": "variable",
        "unit": "m3",
        'computation': lambda Mbioenergyi, BiogasYi, **kwargs: Mbioenergyi * BiogasYi
    },
    "MprodDAYi": {
        "name": "Manure production per day",
        "type": "input",
        "unit": "kg / day per 1000 kg body mass"
    },
    "RBioDiesSupplyi": {
        "name": "Biodiesel from residue streams",
        "type": "variable",
        "unit": "L",
        "computation": lambda BioDieselResiduei, BioDieselYi, **kwargs: BioDieselResiduei * BioDieselYi
    },
    "RBioEthSupply": {
        "name": "Total bioethanol from residue crops",
        "type": "variable",
        "unit": "TJ",
        "computation": lambda RBioEthi, BioEthConversionMJ, **kwargs: (RBioEthi * BioEthConversionMJ).sum()
    },
    "RBioEthi": {
        "name": "Bioethanol from residue crops",
        "type": "variable",
        "unit": "L",
        "computation": lambda ResiduesRemovedi, EthYi, **kwargs: ResiduesRemovedi * EthYi
    },
    "ResiduesRemovedi": {
        "name": "Residues removed from cropland",
        "type": "input",
        "unit": "kg dm"
    },
    "TAi": {
        "name": "Total animal population",
        "type": "input",
        "unit": "head"
    },
    "VSprodDAYi": {
        "name": "Manure production per day in Volatile solids",
        "type": "input",
        "unit": "kg VS / day per 1000 kg body mass"
    }
}

BIOGAS_model = GraphModel(BIOGAS_nodes)

model_dictionnary = {'BIOGAS_model': BIOGAS_model}

model_properties = get_model_properties('models/landuse/BIOGAS_properties.json')