# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from dash.dependencies import Input, Output
import plotly.express as px
from pages import (
    overview,
    newsReviews,
    country,
    world
)
import pandas as pd
import numpy as np

app = dash.Dash(
    __name__, meta_tags=[{"name": "viewport", "content": "width=device-width"}]
)
app.title = 'GreenGrowthReport'

server = app.server

# Describe the layout/ UI of the app
app.layout = html.Div(
    [dcc.Location(id="url", refresh=False), html.Div(id="page-content")]
)


# Update page
@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def display_page(pathname):
    if pathname == "/SimulationDashBoard/world-outlouk":
        return world.create_layout(app)
    elif pathname == "/SimulationDashBoard/by-country":
        return country.create_layout(app)
    elif pathname == "/SimulationDashBoard/simulation":
        return newsReviews.create_layout(app)
    else:
        return overview.create_layout(app)


#####
# TO PUT SOMEWHERE ESLE
data = pd.read_csv('data/GGGI/GGIs_2005_2020.csv')
ISO_options = data[['ISO', 'Country']].drop_duplicates().values

data['Continental_Rank'] = data.groupby(["Year", "Continent", "Variable"])["Value"].rank(method='dense', ascending=False)
data['Income_Rank'] = data.groupby(["Year", "IncomeLevel", "Variable"])["Value"].rank(method='dense', ascending=False)


Income_region_group = data.groupby(['Variable', 'Year', 'IncomeLevel', 'Region', 'Aggregation']).mean().reset_index()
Income_region_group['ISO'] = 'AVG' + '_' + Income_region_group["IncomeLevel"] + '_' + Income_region_group["Region"]

Income_group = data.groupby(['Variable', 'Year', 'IncomeLevel', 'Aggregation']).mean().reset_index()
Income_group['ISO'] = 'AVG' + '_' + Income_group["IncomeLevel"]
Income_group['Continental_Rank'] = np.nan
Income_group['Income_Rank'] = np.nan


Region_group = data.groupby(['Variable', 'Year', 'Continent', 'Aggregation']).mean().reset_index()
Region_group['ISO'] = 'AVG' + '_' + Region_group["Continent"]
Region_group['Continental_Rank'] = np.nan
Region_group['Income_Rank'] = np.nan

data = pd.concat([data, Income_region_group, Region_group, Income_group])

variable_names = {
    'ESRU': 'Efficient and sustainable resource use',
    'NCP': 'Natural capital protection',
    'GEO': 'Green economic opportunities',
    'SI': 'Social inclusion',
    'EE': 'Efficient and and sustainable energy',
    'EW': 'Efficient and sustainable water use',
    'SL': 'Sustainable land use',
    'ME': 'Material use efficiency',
    'EQ': 'Environmental quality',
    'GE': 'Greenhouse gas emissions reductions',
    'BE': 'Biodiversity and ecosystem protection',
    'CV': 'Cultural and social value',
    'GV': 'Green investment',
    'GT': 'Green trade',
    'GJ': 'Green employment',
    'GN': 'Green innovation',
    'AB': 'Access to basic services and resources',
    'GB': 'Gender balance',
    'SE': 'Social equity',
    'SP': 'Social protection'
}

var_names = pd.DataFrame.from_dict(variable_names, orient='index')
var_names.columns = ['Variable_name']
data = data.set_index('Variable')
data['Variable_name'] = var_names
data = data.reset_index()
######


def HTML_text(ISO):
    data_plot = data[(data.ISO.isin([ISO]))]

    if data_plot[data_plot.Aggregation == 'Index'].shape[0] > 0:
        data_plot = data_plot[data_plot.Aggregation == 'Index']
        Country = data_plot['Country'].values[0]
        Index = data_plot['Value'].values[-1]
        Continent = data_plot['Continent'].values[0]
        Status = data_plot['IncomeLevel'].values[0]
    else:
        Country = data_plot.Country.unique()[0]
        Continent = data_plot['Continent'].values[0]
        Status = data_plot['IncomeLevel'].values[0]
        Index = 'Not available'

    return html.Div([
                    html.Div(
                        [
                            html.H5(f"{Country}'s Green Growth Index is {Index}"),
                            html.Br([]),
                            html.P(
                                f"{Country} is a {Status} country located in {Continent}. Its Green Growth index is {Index}.",
                                style={"color": "#ffffff", 'font-size': '15px'},
                                className="row",
                            ),
                        ],
                        className="product",
                    )
                    ],
                    className="row",
                    )


def polar(ISO):
    REF = 'AVG_' + "_".join(data[data.ISO == ISO][['Continent']].drop_duplicates().values[0].tolist())

    df = data[(data.ISO.isin([ISO, REF])) & (data.Aggregation == 'Category') & (data.Year == 2020)].fillna(0)
    continent = df.Continent.values[0]
    inc_level = df.IncomeLevel.values[0]

    df = df.round(2)
    fig = go.Figure()
    cats = ['EE', 'EW', 'SL', 'ME',
            'EQ', 'GE', 'BE', 'CV',
            'AB', 'GB', 'SE', 'SP',
            'GV', 'GT', 'GJ', 'GN']
    df = df.set_index('Variable').T[cats].T.reset_index()

    fig = px.line_polar(df, r="Value", theta="Variable", color="ISO", line_close=True,
                        color_discrete_map={ISO: '#14ac9c', REF: 'darkgrey'},
                        hover_name='Variable_name',
                        hover_data={'ISO': False, 'Variable': False,
                                    'Continental_Rank': True,
                                    'Income_Rank': False},
                        labels={"Value": 'Score',
                                'ISO': '',
                                'Continental_Rank': f'Rank in {continent}',
                                })

    fig.update_traces(fill='toself')
    fig.update_traces(mode="markers+lines", marker=dict(opacity=0.7, size=10))
    fig.update_layout(margin={"r": 20, "t": 20, "l": 20, "b": 20},
                      showlegend=True)
    fig.update_layout(legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1
    ))
    return fig


def loliplot(ISO):
    REF = 'AVG_' + "_".join(data[data.ISO == ISO][["Continent"]].drop_duplicates().values[0].tolist())
    df = data[(data.ISO.isin([ISO, REF])) & (data.Aggregation == 'Dimension') & (data.Year == 2020)].fillna(0)
    df = df.round(2)
    continent = df.Continent.values[0]
    inc_level = df.IncomeLevel.values[0]
    fig = px.scatter(df, y="Value",
                     x="Variable",
                     color='ISO',
                     color_discrete_map={ISO: '#14ac9c', REF: 'darkgrey'},
                     hover_name='Variable_name',
                     hover_data={'ISO': False,
                                 'Variable': False,
                                 'Continental_Rank': True,
                                 'Income_Rank': False},
                     labels={"Value": 'Score',
                             'Variable': '',
                             'ISO': '',
                             'Continental_Rank': f'Rank in {continent}',
                             }
                     )
    fig.update_traces(marker=dict(size=25, opacity=0.6))
    fig.update_yaxes(showgrid=False, range=[0, 100])
    fig.update_layout(margin={"r": 20, "t": 20, "l": 20, "b": 20},
                      showlegend=True)
    fig.update_layout(legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1
    ))
    return fig


def time_series_Index(ISO):
    REF = 'AVG_' + "_".join(data[data.ISO == ISO][["IncomeLevel", 'Region']].drop_duplicates().values[0].tolist())
    REF_1 = 'AVG_' + "_".join(data[data.ISO == ISO][["IncomeLevel"]].drop_duplicates().values[0].tolist())
    REF_2 = 'AVG_' + "_".join(data[data.ISO == ISO][["Continent"]].drop_duplicates().values[0].tolist())

    df = data[(data.ISO.isin([ISO, REF_1, REF_2])) & (data.Aggregation == 'Index')].fillna(0)
    df = df.round(2)
    continent = df.Continent.values[0]
    inc_level = df.IncomeLevel.values[0]

    fig = px.line(df,
                  x='Year',
                  y='Value',
                  color='ISO',
                  line_dash='ISO',
                  color_discrete_map={ISO: '#14ac9c',
                                      REF_1: 'darkgrey',
                                      REF_2: 'darkgrey'},
                  height=300,
                  hover_data={'ISO': False, 'Year': False,
                              'Continental_Rank': True,
                              'Income_Rank': True},
                  hover_name='Year',
                  labels={"Value": 'Score',
                          'ISO': '',
                          'Continental_Rank': f'Rank in {continent}',
                          'Income_Rank': f'Rank in income group',
                          }
                  )
    fig.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
    fig.update_yaxes(visible=True, fixedrange=True)
    fig.update_traces(mode='lines+markers')
    fig.update_layout(legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1
    ))
    #fig.update_layout(hovermode="x unified")

    return fig


def time_series_Rank(ISO):

    df = data[(data.ISO.isin([ISO])) & (data.Aggregation == 'Index')]
    continent = df.Continent.values[0]

    n_continent = data[data.Continent == continent]['ISO'].unique().shape[0]
    fig = px.line(df,
                  x='Year',
                  y='Continental_Rank',
                  color='ISO',
                  line_dash='ISO',
                  color_discrete_map={ISO: '#14ac9c'},
                  height=300,
                  hover_data={'ISO': False, 'Year': False},
                  labels={"Continental_Rank": f'Rank in {continent}'})
    fig.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
    fig.update_yaxes(visible=True,
                     fixedrange=True,
                     range=[n_continent, 0])
    fig.update_traces(mode='lines+markers')
    fig.update_layout(legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1
    ))
    fig.update_layout(hovermode="x unified")

    return fig


@app.callback(
    dash.dependencies.Output('Description', 'children'),
    [dash.dependencies.Input('ISO_select', 'value')],
    suppress_callback_exceptions=True)
def update_HTML(ISO):
    return HTML_text(ISO)


@app.callback(
    dash.dependencies.Output('Perf_ISO', 'figure'),
    [dash.dependencies.Input('ISO_select', 'value')])
def update_polar(ISO):
    return polar(ISO)


@app.callback(
    dash.dependencies.Output('Dim_ISO', 'figure'),
    [dash.dependencies.Input('ISO_select', 'value')])
def update_loliplot(ISO):
    return loliplot(ISO)


@app.callback(
    dash.dependencies.Output('index_time_series', 'figure'),
    [dash.dependencies.Input('ISO_select', 'value')])
def update_ts_ind(ISO):
    return time_series_Index(ISO)


# @app.callback(
#     dash.dependencies.Output('rank_time_series', 'figure'),
#     [dash.dependencies.Input('ISO_select', 'value')])
# def update_ts_rank(ISO):
#     return time_series_Rank(ISO)


if __name__ == "__main__":
    app.run_server(debug=True, host='localhost',
                   dev_tools_ui=False,
                   dev_tools_props_check=False
                   )
