
import pkg_resources
import json
from collections import defaultdict
import pandas as pd
import os

def get_model_properties(path):
    stream = pkg_resources.resource_stream(__name__, f'{path}')

    with open(stream.name, 'r', encoding="utf8") as f: 
        model_properties = json.load(f)

    return model_properties


def flip_dict(data):
    flipped =  defaultdict(dict)
    for key, val in data.items():
        for subkey, subval in val.items():
            flipped[subkey][key] = subval
    return dict(flipped)


def results_to_df_dict(results, model):
    results = flip_dict(results)
    dfs = {}
    
    for var, res in results.items():
        if var in model.summary_df.index:
            if isinstance(res['BAU'], pd.core.series.Series):
                df = pd.concat([df.to_frame(name=s) for s,df in res.items()], axis=1)
            else: 
                df = pd.DataFrame.from_dict({s: v for s, v in res.items()}, orient='index').T
                
            new_level = [[n] for n in model.summary_df.loc[var].fillna('None').values]
            df.columns = pd.MultiIndex.from_product(new_level + [df.columns])
            df.columns= df.columns.set_names(['name', 'type', 'unit', 'computation', 'scenario'])
            dfs[var] = df
    return dfs


def results_to_excel(results, model, filepath):
    writer = pd.ExcelWriter(filepath, engine='xlsxwriter')

    dfs = results_to_df_dict(results, model)
    
    for var, df in dfs.items():
        df.to_excel(writer, sheet_name=var)
    writer.save()


def get_data_dict_from_folder(folder_name):
    files = os.listdir(folder_name)
    data_dict = {file.split('.')[0]: pd.read_csv(
        f'{folder_name}/{file}') for file in files}

    data_dict = {name: df.set_index([col for col in df.columns if col != name]).squeeze(
    ) for name, df in data_dict.items()}

    return data_dict


def get_data_dict_from_folder_parquet(folder_name):
    files = os.listdir(folder_name)
    data_dict = {file.split('.')[0]: pd.read_parquet(
        f'{folder_name}/{file}') for file in files}
    data_dict = {name: df[name] for name, df in data_dict.items()}
    return data_dict
