
import pkg_resources
import json

def get_model_properties(path):
    stream = pkg_resources.resource_stream(__name__, f'{path}')

    with open(stream.name, 'r', encoding="utf8") as f: 
        model_properties = json.load(f)

    return model_properties