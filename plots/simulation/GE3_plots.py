from sklearn.preprocessing import LabelEncoder
import plotly.graph_objects as go
import pandas as pd


def emission_data_dict_to_df(data_dict):

    data_dict = data_dict.copy()

    data = pd.concat([v.to_frame(name='Value').assign(Variable=k)
                      for k, v in data_dict.items()], axis=0).reset_index().dropna()

    data = pd.concat([data, data.groupby('Variable').sum().reset_index().rename(
        columns={"Variable": 'Item'}).assign(Variable='Non-CO2 agricultural emissions')])

    return data


def encode_source_target(df, source='Item', target='Variable'):

    le = LabelEncoder()

    encoded = le.fit_transform(
        df[[source, target]].values.flatten()).reshape(-1, 2)

    return encoded, le.classes_


def sankeyplot(df, source, target, valueformat='.00f', valuesuffix=' Gg(CO2eq)'):

    data = df.copy()

    encoded_s_t, classe_names = encode_source_target(data, source, target)

    data[['Source', 'Target']] = encoded_s_t

    fig = go.Figure(data=[go.Sankey(
        valueformat=valueformat,
        valuesuffix=valuesuffix,
        node=dict(
            pad=15,
            thickness=20,
            line=dict(color="black", width=0.5),
            label=classe_names,
        ),
        link=dict(
            target=data['Target'],
            source=data['Source'],
            value=data['Value']
        ))])

    return fig
