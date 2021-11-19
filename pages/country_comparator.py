import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px

from utils import Header
from app import app, data, ISO_options, INDEX_YEAR


def HTML_text(ISO, className):
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
                        ],
                        className=className,
                    )
                    ],
                    className="row",
                    )


def circular_plot(ISO):
    # to put elsewhere


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
                       height=500,
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
        text=f'{index}', x=0.5, y=0.5, font_size=20, showarrow=False,
        font_color='green'), ])

    fig.update_layout(legend=dict(
        orientation="h",
        yanchor="top",
        y=-0.05,
        xanchor="center",
        x=0,
        title='',
    ))
    return fig


def time_series_Index(ISO_A, ISO_B):

    df = data[(data.ISO.isin([ISO_A, ISO_B])) & (
        data.Aggregation == 'Index')].fillna(0)
    df = df.round(2)

    fig = px.line(df,
                  x='Year',
                  y='Value',
                  color='ISO',
                  color_discrete_map={ISO_A: '#D8A488', ISO_B: '#86BBD8'},
                  height=500,
                  hover_data={'ISO': True, 'Year': True, 'Income_Rank': True,
                              },
                  hover_name='Year',
                  labels={
                          "Value": 'Score',
                          'ISO': 'ISO',
                          'Income_Rank': 'Rank in income group',
                          },
                  )
    fig.update_layout(hovermode="x")
    fig.update_layout(legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1
    ))

    dots = px.scatter(df[df.Year == INDEX_YEAR],
                      x='Year',
                      y='Value',
                      labels={'Year': 'Year', 'Value': 'Score'},
                      color='ISO',
                      hover_data={'Variable': False,
                                  'Year': False,
                                  'Value': False,
                                  'ISO': False},
                      color_discrete_map={ISO_A: '#D8A488', ISO_B: '#86BBD8'},

                      )

    dots.update_layout(showlegend=False, hovermode=False)

    dots.update_traces(marker=dict(size=10, opacity=1))
    for plot in dots.data:
        plot['showlegend'] = False

    fig.add_traces(dots.data)
    return fig


def dimension_trend(ISO_A, ISO_B):

    df = data[(data.Aggregation.isin(['Dimension']))
              & (data.ISO.isin([ISO_A, ISO_B]))]
    fig = px.line(df,
                  x='Year',
                  y='Value',
                  labels={'Year': 'Year', 'Value': 'Score',
                          'Variable_name': 'Dimension'},
                  facet_col='Variable_name',
                  color='ISO',
                  facet_col_wrap=2,
                  facet_col_spacing=0.04,
                  hover_data={'Variable': False,
                              'Year': False,
                              'Value': False,
                              'Continent': False,
                              'Variable_name': False},
                  height=700,
                  color_discrete_map={ISO_A: '#D8A488', ISO_B: '#86BBD8'},

                  )

    fig.update_yaxes(matches=None, showgrid=True, showticklabels=True)
    fig.update_xaxes(range=[2005, 2021])
    fig.update_traces(mode='lines', hovertemplate="%{y}",)

    dots = px.scatter(df[df.Year == INDEX_YEAR],
                      x='Year',
                      y='Value',
                      labels={'Year': 'Year', 'Value': 'Score'},
                      facet_col='Variable_name',
                      color='ISO',
                      facet_col_wrap=2,
                      facet_col_spacing=0.04,
                      hover_data={'Variable': False,
                                  'Year': False,
                                  'Value': False,
                                  'Continent': False,
                                  'Variable_name': False, 'ISO': False},
                      height=700,
                      color_discrete_map={ISO_A: '#D8A488', ISO_B: '#86BBD8'},
                      )

    dots.update_layout(showlegend=False, hovermode=False)

    dots.update_traces(marker=dict(size=10, opacity=1))
    for plot in dots.data:
        plot['showlegend'] = False

    fig.add_traces(dots.data)

    fig.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
    fig.update_xaxes(showticklabels=True, col=2, row=2)
    fig.update_layout(margin={"r": 25, "t": 25, "l": 25, "b": 25},
                      hovermode="x",
                      legend=dict(yanchor="bottom",
                                  y=0.01,
                                  xanchor="right",
                                  x=1
                                  )
                      )

    fig.update_layout(legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1
    ))

    return fig


layout = html.Div(
    [
        html.Div([Header(app, 'Country Comparison')]),

        html.Div(
            [
                html.Div([html.Div([dcc.Dropdown(id="ISO_select_A", options=[{'label': country, 'value': iso} for iso, country in ISO_options], value='LCA')],
                                   style={'width': '100%',
                                          'display': 'inline-block',
                                          'align-items': 'center',
                                          'justify-content': 'center',
                                          'font-size': '20px'}
                                   ),
                          html.Div(id='Description_A'),
                          dcc.Graph(id='circular_plot_A', config={
                                    'displayModeBar': False}),

                          ], className='pretty_container six columns'),

                html.Div([html.Div([dcc.Dropdown(id="ISO_select_B", options=[{'label': country, 'value': iso} for iso, country in ISO_options], value='VCT')],
                                   style={'width': '100%',
                                          'display': 'inline-block',
                                          'align-items': 'center',
                                          'justify-content': 'center',
                                          'font-size': '20px'}
                                   ),
                          html.Div(id='Description_B'),
                          dcc.Graph(id='circular_plot_B', config={
                                    'displayModeBar': False}),
                          ], className='pretty_container six columns'),

            ], className='pretty_container twelve columns'),

        html.Div(
            [
                html.H6(
                    "Index Trends",
                    className="subtitle padded",
                ),
                dcc.Graph(id='index_time_series_A_B', config={
                    'displayModeBar': False}),
                html.H6(
                    "Dimension Trends",
                    className="subtitle padded",
                ),
                dcc.Graph(id='dim_plot_A_B', config={
                    'displayModeBar': False}),
            ],
            className='pretty_container twelve columns')
        # page 1
    ],
    className="page",
)


@app.callback(
    dash.dependencies.Output('Description_A', 'children'),
    [dash.dependencies.Input('ISO_select_A', 'value')],
    suppress_callback_exceptions=True)
def update_HTML_A(ISO):
    return HTML_text(ISO, 'product_A')


@app.callback(
    dash.dependencies.Output('Description_B', 'children'),
    [dash.dependencies.Input('ISO_select_B', 'value')],
    suppress_callback_exceptions=True)
def update_HTML_B(ISO):
    return HTML_text(ISO, 'product_B')


@app.callback(
    dash.dependencies.Output('circular_plot_A', 'figure'),
    [dash.dependencies.Input('ISO_select_A', 'value')])
def update_circular_plots(ISO_A):
    return circular_plot(ISO_A)


@app.callback(
    dash.dependencies.Output('circular_plot_B', 'figure'),
    [dash.dependencies.Input('ISO_select_B', 'value')])
def update_circular_plots(ISO_B):
    return circular_plot(ISO_B)




@app.callback(
    dash.dependencies.Output('index_time_series_A_B', 'figure'),
    [dash.dependencies.Input('ISO_select_A', 'value'),
     dash.dependencies.Input('ISO_select_B', 'value')],
    suppress_callback_exceptions=True)
def update_ts(ISO_A, ISO_B):
    return time_series_Index(ISO_A, ISO_B)


@app.callback(
    dash.dependencies.Output('dim_plot_A_B', 'figure'),
    [dash.dependencies.Input('ISO_select_A', 'value'),
     dash.dependencies.Input('ISO_select_B', 'value')],
    suppress_callback_exceptions=True)
def update_dim(ISO_A, ISO_B):
    return dimension_trend(ISO_A, ISO_B)
