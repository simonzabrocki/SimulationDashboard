import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import plotly.express as px

from utils import Header
from app import app, data, ISO_options

import numpy as np
import pandas as pd
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

    df = data[(data.ISO.isin([ISO, REF])) & (data.Aggregation == 'Category') & (data.Year == 2019)]#.fillna(0)
    continent = df.Continent.values[0]

    df = df.round(2)
    fig = go.Figure()

    cats = ['EE', 'EW', 'SL', 'ME',
            'EQ', 'GE', 'BE', 'CV',
            'AB', 'GB', 'SE', 'SP',
            'GV', 'GT', 'GJ', 'GN']

    df = df.set_index('Variable').T[cats].T.reset_index()

    fig = px.line_polar(df[df.ISO == ISO],
                        r="Value", theta="Variable", color="ISO", line_close=True,
                        color_discrete_map={ISO: '#14ac9c', REF: 'darkgrey'},
                        hover_name='Variable_name',
                        hover_data={'ISO': False, 'Variable': False,
                                    'Continental_Rank': True,
                                    'Income_Rank': False},
                        labels={"Value": 'Score',
                                'ISO': '',
                                'Continental_Rank': f'Rank in {continent}',
                                })

    fig.update_traces(mode="markers", marker=dict(opacity=0.7, size=10))

    # fig.update_traces(fill='toself')

    fig.add_trace(go.Scatterpolar(r=df[df.ISO == REF]['Value'],
                                  theta=df[df.ISO == REF]['Variable'],
                                  name=REF,
                                  mode='markers',
                                  marker=dict(color='darkgrey', size=10),
                                  hoverinfo='skip')
                  )

    fig.update_traces(fill='toself')
    fig.update_traces(mode="markers", marker=dict(opacity=0.7, size=10))

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
    df = data[(data.ISO.isin([ISO, REF])) & (data.Aggregation == 'Dimension') & (data.Year == 2019)]#.fillna(0)
    df = df.round(2)
    continent = df.Continent.values[0]

    fig = px.scatter(df[df.ISO == ISO],
                     x="Value",
                     y="Variable",
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

    fig.add_trace(go.Scatter(y=df[df.ISO == REF]['Variable'],
                             x=df[df.ISO == REF]['Value'],
                             name=REF,
                             mode='markers',
                             marker=dict(color='darkgrey', size=1),
                             hoverinfo='skip'))

    fig.update_traces(marker=dict(size=15, opacity=0.6))
    fig.update_xaxes(showgrid=False, range=[0, 100])
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


def loliplot_2(ISO):
    REF = 'AVG_' + "_".join(data[data.ISO == ISO][["Continent"]].drop_duplicates().values[0].tolist())
    df = data[(data.ISO.isin([ISO, REF])) & (data.Aggregation == 'Category') & (data.Year == 2019)]#.fillna(0)
    df = df.round(2)
    continent = df.Continent.values[0]


    cats = ['EE', 'EW', 'SL', 'ME',
            'EQ', 'GE', 'BE', 'CV',
            'AB', 'GB', 'SE', 'SP',
            'GV', 'GT', 'GJ', 'GN']

    df = df.set_index('Variable').T[cats].T.reset_index()
    fig = px.scatter(df[df.ISO == ISO],
                     x="Value",
                     y="Variable",
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

    fig.add_trace(go.Scatter(y=df[df.ISO == REF]['Variable'],
                             x=df[df.ISO == REF]['Value'],
                             name=REF,
                             mode='markers',
                             marker=dict(color='darkgrey', size=1),
                             hoverinfo='skip'))

    fig.update_traces(marker=dict(size=10, opacity=0.6))
    fig.update_xaxes(showgrid=False, range=[0, 100])
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
    REF_1 = 'AVG_' + "_".join(data[data.ISO == ISO][["IncomeLevel"]].drop_duplicates().values[0].tolist())
    REF_2 = 'AVG_' + "_".join(data[data.ISO == ISO][["Continent"]].drop_duplicates().values[0].tolist())

    df = data[(data.ISO.isin([ISO, REF_1, REF_2])) & (data.Aggregation == 'Index')].fillna(0)
    df = df.round(2)
    continent = df.Continent.values[0]

    if df[df.ISO == ISO].shape[0] == 0:
        fig = px.line(df[df.ISO == ISO],
                      x='Year',
                      y='Value')
    else:
        fig = px.line(df[df.ISO == ISO],
                      x='Year',
                      y='Value',
                      color='ISO',
                      color_discrete_map={ISO: '#14ac9c'},
                      height=300,
                      hover_data={'ISO': False, 'Year': False,
                                  'Continental_Rank': True,
                                  'Income_Rank': True},
                      hover_name='Year',
                      labels={"Value": 'Score',
                              'ISO': '',
                              'Continental_Rank': f'Rank in {continent}',
                              'Income_Rank': 'Rank in income group',
                              }
                      )
    fig.update_traces(mode='lines+markers')

    fig.add_trace(go.Scatter(x=df[df.ISO == REF_1]['Year'],
                             y=df[df.ISO == REF_1]['Value'],
                             name=REF_1,
                             mode='lines',
                             line=dict(color='darkgrey', width=2, dash='dash'),
                             hoverinfo='skip'))

    fig.add_trace(go.Scatter(x=df[df.ISO == REF_2]['Year'],
                             y=df[df.ISO == REF_2]['Value'],
                             name=REF_2,
                             mode='lines',
                             line=dict(color='darkgrey', width=2, dash='dot'),
                             hoverinfo='skip'))
    fig.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
    fig.update_yaxes(visible=True, fixedrange=True)
    fig.update_layout(legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1
    ))
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
    #return polar(ISO)
    return loliplot_2(ISO)

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


layout = html.Div(
    [
        html.Div([Header(app)]),
        # page 1
        html.Div(
            [
                html.Div([dcc.Dropdown(id="ISO_select", options=[{'label': country, 'value': iso} for iso, country in ISO_options], value='FRA')],
                         style={'width': '100%',
                                'display': 'inline-block',
                                'align-items': 'center',
                                'justify-content': 'center',
                                'font-size': '20px'}
                         ),
                html.Div(id='Description'),
                html.Div(
                    [
                        html.Div(
                            [
                                html.H6(
                                    "Index trend",
                                    className="subtitle padded",
                                ),
                                dcc.Graph(id='index_time_series',
                                          config={'displayModeBar': False}
                                          )
                            ],
                            className="twelve columns",
                        )
                    ],
                    className="row",
                ),
                html.Div(
                    [
                        html.Div(
                            [
                                html.H6(["2019 Dimensions"], className="subtitle padded"),
                                dcc.Graph(id='Dim_ISO',
                                          config={'displayModeBar': False}),
                            ],
                            className="six columns",
                        ),
                        html.Div(
                            [
                                html.H6(["2019 Indicators"], className="subtitle padded"),
                                dcc.Graph(id='Perf_ISO',
                                          config={'displayModeBar': False}),
                            ],
                            className="six columns",
                        ),
                    ],
                    className="row",
                ),
            ],

            className="sub_page",
        ),
    ],
    className="page",
)
