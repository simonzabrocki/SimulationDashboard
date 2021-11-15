import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import plotly.express as px

from utils import Header, dcc_config, is_btn_clicked
from app import app, data, missing_data, ISO_options, indicator_properties, INDEX_YEAR

import numpy as np
import pandas as pd
import os


def compute_group(data):
    '''To improve'''

    Income_region_group = data.groupby(
        ['Variable', 'Year', 'IncomeLevel', 'Region', 'Aggregation']).mean().reset_index()
    Income_region_group['ISO'] = 'AVG' + '_' + \
        Income_region_group["IncomeLevel"] + \
        '_' + Income_region_group["Region"]

    Income_group = data.groupby(['Variable', 'Year', 'IncomeLevel',
                                 'Aggregation']).mean().reset_index()
    Income_group['ISO'] = 'AVG' + '_' + Income_group["IncomeLevel"]

    Income_group['Continental_Rank'] = np.nan
    Income_group['Income_Rank'] = np.nan

    Region_group = data.groupby(['Variable', 'Year', 'Continent',
                                 'Aggregation']).mean().reset_index()
    Region_group['ISO'] = 'AVG' + '_' + Region_group["Continent"]
    Region_group['Continental_Rank'] = np.nan
    Region_group['Income_Rank'] = np.nan

    data = pd.concat([Income_region_group, Region_group, Income_group])

    return data


group_data = compute_group(data)


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
                            html.H5(
                                f"{Country}'s Green Growth Index is {Index}"),
                            html.Br([]),
                            html.P(
                                f"{Country} is a {Status} country located in {Continent}. Its Green Growth index is {Index}.",
                                style={"color": "#ffffff",
                                       'font-size': '15px'},
                                className="row",
                            ),
                            html.Button(f'Download {Country}\'s data', id='btn-country-data', n_clicks=0,
                                style={'font-size': 10,
                                        'color': '#ffffff',}),
                            dcc.Download(id="download-country-data"),
                            # html.Button(f'Download {Country}\'s report', id='btn-html-report', n_clicks=0,
                            #     style={'font-size': 10,
                            #             'color': '#ffffff',}),
                            # dcc.Download(id="download-html-report"),

                        ],
                        className="product",
                    )
                    ],
                    className="row",
                    )


def circular_plot(ISO):
    df = data[(data.ISO.isin([ISO])) & (data.Aggregation ==
                                        'Category') & (data.Year == INDEX_YEAR)].fillna(0)
    for dim in df.Dimension.unique():
        df = df.append({'Variable': f'{dim}', 'Value': 0,
                        'Dimension': dim}, ignore_index=True)

    index_df = data[(data.ISO.isin([ISO])) & (data.Variable == 'Index')
                    & (data.Year == INDEX_YEAR)].Value.unique()

    # degueux à revoir
    if index_df.shape[0] > 0:
        index = index_df[0]
    else:
        index = 'NA'

    fig = px.bar_polar(df,
                       theta='Variable',
                       r='Value',
                       range_r=[-30, 100],
                       color='Dimension',
                       hover_data={'Variable_name': True, 'Variable': False},
                       color_discrete_map={
                           "Social Inclusion": "#d9b5c9",
                           "Natural Capital Protection": "#f7be49",
                           "Efficient and Sustainable Resource Use": "#8fd1e7",
                           "Green Economic Opportunities": "#9dcc93",
                       },
                       labels={'Year': 'Year', 'Value': 'Score',
                               'Category': 'Dimension', 'Variable_name': 'Category'},
                       height=600,
                       )

    fig.update_traces(offset=-4 / 12)
    fig.update_polars(radialaxis=dict(gridcolor='white',
                                      dtick=20,
                                      gridwidth=3,
                                      ticks='',
                                      angle=0,
                                      tickangle=0,
                                      tickvals=[20, 40, 60, 80],
                                      showline=True,
                                      linewidth=0,
                                      side='clockwise',
                                      ),



                      angularaxis=dict(showgrid=False, rotation=90 - 1 * 360 / 20, ticks='',
                                       linewidth=1, linecolor='green',
                                       tickvals=[0, 1, 2, 3, 5, 6, 7, 8,
                                                 10, 11, 12, 13, 15, 16, 17, 18],
                                       ))

    fig.update_layout(annotations=[dict(
        text=f'{index}', x=0.5, y=0.5, font_size=20, showarrow=False, font_color='green'), ])

    fig.update_layout(legend=dict(
        orientation="h",
        yanchor="top",
        y=-0.05,
        xanchor="center",
        x=0,
        title='',
    ))
    return fig


def polar(ISO):
    REF = 'AVG_' + "_".join(data[data.ISO == ISO][['Continent']
                                                  ].drop_duplicates().values[0].tolist())

    group_df = group_data[group_data.ISO.isin([ISO]) & (data.Aggregation ==
                                                        'Category') & (data.Year == INDEX_YEAR)]

    df = data[(data.ISO.isin([ISO, REF])) & (data.Aggregation ==
                                             'Category') & (data.Year == INDEX_YEAR)]  # .fillna(0)

    df = pd.concat([df, group_df])
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
    REF = 'AVG_' + "_".join(data[data.ISO == ISO][["Continent"]
                                                  ].drop_duplicates().values[0].tolist())

    group_df = group_data[group_data.ISO.isin([REF]) & (group_data.Aggregation ==
                                                        'Dimension') & (group_data.Year == INDEX_YEAR)]

    df = data[(data.ISO.isin([ISO, REF])) & (data.Aggregation ==
                                             'Dimension') & (data.Year == INDEX_YEAR)]  # .fillna(0)

    df = pd.concat([df, group_df])

    df = df.round(2)
    continent = df.Continent.values[0]

    fig = px.scatter(df[df.ISO == ISO],
                     y="Value",
                     x="Variable",
                     color='Variable',
                     color_discrete_map={
                         ISO: '#14ac9c',
                         "SI": "#d9b5c9",
                         "NCP": "#f7be49",
                         "ESRU": "#8fd1e7",
                         "GEO": "#9dcc93",
    },
        hover_name='Variable_name',
        hover_data={
        'ISO': False,
        'Variable': False,
        'Continental_Rank': True,
        'Income_Rank': False
    },
        labels={
        "Value": 'Score',
        'Variable': '',
        'ISO': '',
        'Continental_Rank': f'Rank in {continent}',
    }

    )

    fig.add_trace(go.Scatter(x=df[df.ISO == REF]['Variable'],
                             y=df[df.ISO == REF]['Value'],
                             name=REF,
                             mode='markers',
                             marker=dict(color='darkgrey', size=1),
                             hoverinfo='skip')
                  )

    fig.update_traces(marker=dict(size=20, opacity=0.8))
    fig.update_yaxes(showgrid=False, range=[0, 100], tickvals=[20, 40, 60, 80])
    fig.update_layout(margin={"r": 20, "t": 20, "l": 20, "b": 20},
                      showlegend=True)

    fig.update_layout(legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1
    ))

    # there must be a better way
    conversion = {
        "ESRU": 'Efficient and Sustainable Resource Use',
        "GEO": 'Green Economic Opportunities',
        "NCP": 'Natural Capital Protection',
        'SI': "Social Inclusion",
        REF: REF,
    }

    fig.for_each_trace(lambda t: t.update(name=conversion[t.name]))

    return fig


def loliplot_2(ISO):
    REF = 'AVG_' + "_".join(data[data.ISO == ISO][["Continent"]
                                                  ].drop_duplicates().values[0].tolist())

    df = data[(data.ISO.isin([ISO, REF])) & (data.Aggregation ==
                                             'Category') & (data.Year == INDEX_YEAR)]  # .fillna(0)

    group_df = group_data[group_data.ISO.isin([REF]) & (group_data.Aggregation ==
                                                        'Category') & (group_data.Year == INDEX_YEAR)]

    df = pd.concat([df, group_df])

    df = df.round(2)
    continent = df.Continent.values[0]

    fig = px.bar(df[df.ISO == ISO],
                 y="Value",
                 x="Variable",
                 color='Dimension',
                 color_discrete_map={
        ISO: '#14ac9c',
        "Efficient and Sustainable Resource Use": "#8fd1e7",
        "Green Economic Opportunities": "#9dcc93",
        "Natural Capital Protection": "#f7be49",
        "Social Inclusion": "#d9b5c9",
    },
        hover_name='Variable_name',
        hover_data={'ISO': False,
                    'Variable': False,
                    'Continental_Rank': True,
                    'Income_Rank': False},

        labels={"Value": 'Score',
                'Variable': '',
                'ISO': '',
                'Continental_Rank': f'Rank in {continent}',
                },

    )
    fig.update_traces(opacity=0.7)

    fig.add_trace(go.Scatter(x=df[df.ISO == REF]['Variable'],
                             y=df[df.ISO == REF]['Value'],
                             name=REF,
                             mode='markers',
                             marker=dict(color='darkgrey',
                                         size=10, symbol='square'),
                             hoverinfo='skip'))

    fig.update_yaxes(showgrid=False, range=[0, 100], tickvals=[20, 40, 60, 80])
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
    REF_1 = 'AVG_' + "_".join(data[data.ISO == ISO][["IncomeLevel"]
                                                    ].drop_duplicates().values[0].tolist())
    REF_2 = 'AVG_' + "_".join(data[data.ISO == ISO][["Continent"]
                                                    ].drop_duplicates().values[0].tolist())

    df = data[(data.ISO.isin([ISO, REF_1, REF_2])) &
              (data.Aggregation == 'Index')].fillna(0)

    group_df = group_data[group_data.ISO.isin([REF_1, REF_2]) & (
        group_data.Aggregation == 'Index')].fillna(0)

    df = pd.concat([df, group_df])

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
                      height=500,
                      hover_data={'ISO': False, 'Year': False,
                                  'Continental_Rank': True,
                                  'Income_Rank': True},
                      hover_name='Year',
                      labels={"Value": 'Score',
                              'ISO': '',
                              'Continental_Rank': f'Rank in {continent}',
                              'Income_Rank': 'Rank in income group',
                              },
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



def missing_bar_plot(ISO):
    cats = ['EE', 'EW', 'SL', 'ME',
            'EQ', 'GE', 'BE', 'CV',
            'AB', 'GB', 'SE', 'SP',
            'GV', 'GT', 'GJ', 'GN']
    

    plot_df = (
        missing_data.loc[ISO].reset_index().merge(indicator_properties[['Category', "Dimension"]].drop_duplicates(), on='Category')
                    .merge(data[['Variable_name', 'Variable']].drop_duplicates(), left_on='Category', right_on='Variable')
    )
    plot_df_bis = plot_df.copy().assign(Dimension='Missing')
    plot_df_bis['Data availability (%)'] = (100 - plot_df_bis['Data availability (%)']).round(2)

    plot_df = pd.concat([plot_df, plot_df_bis])
    fig = px.bar(plot_df,
             y='Category',
             x='Data availability (%)',
             color='Dimension',
             barmode='stack',
             orientation='h',
            text='Data availability (%)',
             hover_data={'Variable_name': True, 'Dimension': False, 'Data availability (%)': False},
            labels={'Variable_name': 'Category'},
            color_discrete_map={
                           "Social Inclusion": "#d9b5c9",
                           "Natural Capital Protection": "#f7be49",
                           "Efficient and Sustainable Resource Use": "#8fd1e7",
                           "Green Economic Opportunities": "#9dcc93",
                           "Missing": '#D3D3D3'
                       },
                ).update_layout(height=1000,
                                plot_bgcolor='rgba(0, 0, 0, 0)',
                                legend=dict(
        yanchor="top",
        y=-0.05,
        xanchor="center",
        x=0,
        title=''
        
    ),
    ).update_traces(texttemplate='%{text:.2s}%', textposition='inside', textfont=dict(
        family="sans serif",
        size=18,
        color="white"
    )).update_yaxes(title="").update_xaxes(showticklabels=False)

    return fig




def Indicator_lolipop(ISO):
    df = data[(data.Aggregation == 'Indicator_normed') & (data.Year == 2019) & (data.ISO == ISO)].drop(columns=['Category', 'Dimension']).merge(indicator_properties, left_on='Variable', right_on='Indicator')

    df = df.round(2).sort_values(by=['Dimension', 'Variable'], ascending=False)
    fig = px.scatter(df,
                     y='Variable',
                     x='Value',
                     color='Dimension',
                     facet_col='Dimension',
                     facet_col_spacing=0.05,
                     hover_data={'Value': True, 'Variable': False, "display_name": True},
                     labels={'Variable': 'Indicator', 'Value': 'Score'},
                     color_discrete_map={
                         "Social Inclusion": "#d9b5c9",
                         "Natural Capital Protection": "#f7be49",
                         "Efficient and Sustainable Resource Use": "#8fd1e7",
                         "Green Economic Opportunities": "#9dcc93",
                     },
                     height=600,
                     )
    fig.update_xaxes(showgrid=True, range=[0, 110], tickvals=[
                     20, 40, 60, 80, 100], visible=True, title='')
    fig.update_yaxes(showgrid=False, range=[-1, 12], matches=None, showticklabels=True)

    fig.update_traces(marker=dict(size=12, opacity=0.8))
    fig.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))

    bars = px.bar(df,
                  y='Variable',
                  x='Value',
                  facet_col='Dimension',
                  facet_col_spacing=0.05,
                  hover_data={'Value': True},
                  labels={'Variable': 'Indicator', 'Value': ''},
                  orientation='h',
                  opacity=0.6,
                  height=600,
                  )

    bars.update_traces(marker_color='lightgrey',
                       width=0.1,
                       marker_line_width=0.1, opacity=0.8)

    fig.add_traces(bars.data)

    fig.update_layout(legend=dict(
        orientation="h",
        yanchor="top",
        y=-0.1,
        xanchor="right",
        x=1,
        title=''
    ))
    return fig


def heatmap_plot(ISO):
    REF_1 = 'AVG_' + "_".join(data[data.ISO == ISO][["IncomeLevel"]
                                                    ].drop_duplicates().values[0].tolist())
    REF_2 = 'AVG_' + "_".join(data[data.ISO == ISO][["Continent"]
                                                    ].drop_duplicates().values[0].tolist())

    df = data[(data.ISO.isin([ISO, REF_1, REF_2])) &
              (data.Aggregation == 'Category') & (data.Year == INDEX_YEAR)].fillna(0)

    group_df = group_data[group_data.ISO.isin([REF_1, REF_2]) & (
        group_data.Aggregation == 'Category') & (group_data.Year == INDEX_YEAR)].fillna(0)

    df = pd.concat([df, group_df, df[['Variable']].assign(ISO=' ', Value=np.nan)])

    df = df.round(2)
    
    df = df.pivot(index=['ISO'], columns=['Variable'], values='Value').loc[[ISO, ' ',REF_1, REF_2]]
    cats = ['AB', 'GB', 'SE', 'SP',
            'EQ', 'GE', 'BE', 'CV',
            'EE', 'EW', 'SL', 'ME',
            'GV', 'GT', 'GJ', 'GN']

    fig = px.imshow(df[cats],
          zmin=0, zmax=100,
          color_continuous_scale=[(0, "#f14326"),
                                  (0.25, "#fc8d59"),
                                  (0.5, "#ffffbf"),
                                  (1, "#14ac9c")],
    )

    fig.update_yaxes(showgrid=False)
    fig.update_xaxes(showgrid=False)
    return fig


layout = html.Div(
    [
        html.Div([Header(app, 'Country Profile')]),
        # page 1
        html.Div(
            [
                html.Div(
                    [
                        html.Div([dcc.Dropdown(id="ISO_select",
                                               options=[{'label': country, 'value': iso}
                                                        for iso, country in ISO_options],
                                               value='FRA')],
                                 style={'width': '100%',
                                        'display': 'inline-block',
                                        'align-items': 'center',
                                        'justify-content': 'center',
                                        'font-size': '20px'}
                                 ),
                        html.Div(id='Description'),
                        html.H6(
                            "Distances to Targets",
                            className="subtitle padded",
                        ),
                        dcc.Graph(id='circular_plot',
                                  config=dcc_config('distance_to_target')),
                        html.H6(
                            "Data availability",
                            className="subtitle padded",
                        ),
                        dcc.Graph(id='missing_data_plot',
                                  config=dcc_config('data_availability')),
                    ],
                    className='pretty_container four columns'),
                html.Div(
                    [

                        html.H6(
                            "Index trend",
                            className="subtitle padded",
                        ),
                        dcc.Graph(id='index_time_series',
                                  config=dcc_config('index_trend'),
                                  ),
                        html.Div(
                            [
                                html.Div(
                                    [
                                        html.H6([f"{INDEX_YEAR} Dimensions"],
                                                className="subtitle padded"),
                                        dcc.Graph(id='Dim_ISO',
                                                  config=dcc_config('dimensions')),
                                    ],
                                    className="six columns",
                                ),
                                html.Div(
                                    [
                                        html.H6([f"{INDEX_YEAR} Categories"],
                                                className="subtitle padded"),
                                        dcc.Graph(id='Perf_ISO',
                                                  config=dcc_config('categories')),
                                    ],
                                    className="six columns",
                                ),
                                html.Div(
                                    [
                                        html.H6([f"{INDEX_YEAR} Heatmap"],
                                                className="subtitle padded"),
                                        dcc.Graph(id='heatmap_ISO',
                                                  config=dcc_config('indicators')),

                                    ],
                                    className="twelve columns",
                                ),
                                html.Div(
                                    [
                                        html.H6([f"{INDEX_YEAR} Indicators"],
                                                className="subtitle padded"),
                                        dcc.Graph(id='indic_ISO',
                                                  config=dcc_config('indicators')),

                                    ],
                                    className="twelve columns",
                                ),
                            ],
                            className="row",
                        ),
                    ],
                    className='pretty_container eight columns')
            ],

            className="row",
        ),
    ],
    className="page",
)


@app.callback(
    dash.dependencies.Output('Description', 'children'),
    [dash.dependencies.Input('ISO_select', 'value')],
    suppress_callback_exceptions=True)
def update_HTML(ISO):
    return HTML_text(ISO)


@app.callback(
    dash.dependencies.Output('circular_plot', 'config'),
    dash.dependencies.Output('circular_plot', 'figure'),
    [dash.dependencies.Input('ISO_select', 'value')])
def update_circular_plot(ISO):
    return dcc_config(f'distance_to_target_{ISO}'), circular_plot(ISO)


@app.callback(
    dash.dependencies.Output('missing_data_plot', 'config'),
    dash.dependencies.Output('missing_data_plot', 'figure'),
    [dash.dependencies.Input('ISO_select', 'value')])
def update_missing_plot(ISO):
    return dcc_config(f'data_availability_{ISO}'), missing_bar_plot(ISO)


@app.callback(
    dash.dependencies.Output('indic_ISO', 'config'),
    dash.dependencies.Output('indic_ISO', 'figure'),
    [dash.dependencies.Input('ISO_select', 'value')])
def update_gauge_plot(ISO):
    return dcc_config(f'indicators_{ISO}'), Indicator_lolipop(ISO)

@app.callback(
    dash.dependencies.Output('index_time_series', 'config'),
    dash.dependencies.Output('index_time_series', 'figure'),
    [dash.dependencies.Input('ISO_select', 'value')])
def update_ts_ind(ISO):
    return dcc_config(f'index_trend_{ISO}'), time_series_Index(ISO)


@app.callback(
    dash.dependencies.Output('Dim_ISO', 'config'),
    dash.dependencies.Output('Dim_ISO', 'figure'),
    [dash.dependencies.Input('ISO_select', 'value')])
def update_loliplot(ISO):
    return dcc_config(f'dimensions_{ISO}'), loliplot(ISO)



@app.callback(
    dash.dependencies.Output('heatmap_ISO', 'config'),
    dash.dependencies.Output('heatmap_ISO', 'figure'),
    [dash.dependencies.Input('ISO_select', 'value')])
def update_loliplot(ISO):
    return dcc_config(f'heatmap_{ISO}'), heatmap_plot(ISO)


@app.callback(
    dash.dependencies.Output('Perf_ISO', 'config'),
    dash.dependencies.Output('Perf_ISO', 'figure'),
    [dash.dependencies.Input('ISO_select', 'value')])
def update_polar(ISO):
    return dcc_config(f'categories_{ISO}'), loliplot_2(ISO)


@app.callback(
    dash.dependencies.Output("download-country-data", "data"),
    [
        dash.dependencies.Input('ISO_select', 'value'),
        dash.dependencies.Input("btn-country-data", "n_clicks"),
    ],
    prevent_initial_call=True,
)
def downdload_table(ISO, n_clicks):
    if is_btn_clicked('btn-country-data'):
        df  = data.query("ISO == @ISO")[['ISO', 'Variable', 'Aggregation', 'Year', 'Value']]

        return dcc.send_data_frame(df.set_index("ISO").to_csv, f"{ISO}_data.csv")

    else:  # https://community.plotly.com/t/how-to-leave-callback-output-unchanged/7276/8
        raise dash.exceptions.PreventUpdate



@app.callback(
    dash.dependencies.Output("download-html-report", "data"),
    [
        dash.dependencies.Input('ISO_select', 'value'),
        dash.dependencies.Input("btn-html-report", "n_clicks"),
    ],
    prevent_initial_call=True,
)
def downdload_table(ISO, n_clicks):
    if is_btn_clicked('btn-html-report'):
        df  = data.query("ISO == @ISO")[['ISO', 'Variable', 'Aggregation', 'Year', 'Value']]
        os.system(f"python jupyter_ISO_report.py report.ipynb --iso {ISO}")

        return  dcc.send_file("./outputs/reports/report.html")

    else:  # https://community.plotly.com/t/how-to-leave-callback-output-unchanged/7276/8
        raise dash.exceptions.PreventUpdate