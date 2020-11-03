import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
from utils import Header
import pandas as pd
import pathlib
import plotly.graph_objs as go
import dash_table


PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../data").resolve()

data = pd.read_csv(DATA_PATH.joinpath('GGGI/GGIs_2005_2020.csv'))

ISO_options = data[['ISO', 'Country']].drop_duplicates().values

cover = data[(data.Aggregation == 'Index') & (data.Year == 2020)].dropna().shape[0]
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


def Index_Heatmap(data):
    df = data[(data.Aggregation == 'Index') & (data.Year == 2020)]
    df = df.groupby(['Continent', 'Variable']).mean()[
        'Value'].reset_index().pivot(index='Continent', columns='Variable')
    fig = px.imshow(df['Value'],
                    color_continuous_scale=[(0, "#fc8d59"), (0.5, "#ffffbf"), (1, "#14ac9c")],
                    labels=dict(x="", y="", color="Value"),
                    range_color=[0, 100],
                    width=300,
                    height=300
                    )

    fig.update_layout(coloraxis_colorbar=dict(title="",
                                              thicknessmode="pixels", thickness=10,
                                              lenmode="pixels", len=100,
                                              dtick=50)
                      )
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})

    fig.update_layout(showlegend=False)
    fig.update(layout_coloraxis_showscale=False)
    return fig


def Index_trend(data):
    # df = data[(data.Aggregation == 'Index')].groupby('Year').mean().reset_index()
    # fig = px.line(df,
    #               x='Year',
    #               y='Value',
    #               labels={'Value': ''},
    #               height=300)
    # fig.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
    # fig.update_yaxes(visible=True, fixedrange=True)
    # fig.update_traces(mode='lines+markers', line_color="#14ac9c")

    df = data[(data.Aggregation == 'Index')].groupby(['Year', 'Continent']).mean().reset_index()
    fig = px.line(df,
                  x='Year',
                  y='Value',
                  facet_col='Continent',
                  facet_col_wrap=2,
                  labels = {
                     'Value': ''
                  },
                 height=600)
    fig.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
    fig.update_yaxes(visible=True)
    fig.update_xaxes(showticklabels=True, col=2, row=2)
    fig.update_traces(mode='lines', line_color='#14ac9c')
    return fig


def dimension_trend(data):
    # df = data[(data.Aggregation.isin(['Dimension']))].groupby(
    #     ["Variable_name", 'Variable', 'Year']).mean().reset_index()
    # df['Value'] = df['Value'].round(1)
    #
    # fig = px.line(df,
    #               x='Year',
    #               y='Value',
    #               labels={'Year': '', 'Value': ''},
    #               facet_col='Variable',
    #               facet_col_wrap=2,
    #               height=300,
    #               width=700,
    #               facet_col_spacing=0.04,
    #               hover_name='Variable_name',
    #               hover_data={'Variable': False, 'Year': False, 'Value': False})
    # fig.update_traces(mode='lines+markers', line_color="#14ac9c")
    # fig.update_yaxes(matches=None, showgrid=True, showticklabels=True)
    # fig.update_xaxes(showgrid=False)
    # fig.update_yaxes(showgrid=False)
    #
    # fig.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
    #
    # fig.update_layout(margin={"r": 25, "t": 25, "l": 25, "b": 25})
    df = data[(data.Aggregation.isin(['Dimension']))].groupby(
        ["Variable_name", 'Variable', 'Year', 'Continent']).mean().reset_index()
    df['Value'] = df['Value'].round(1)

    fig = px.line(df,
                  x='Year',
                  y='Value',
                  labels={'Year': '', 'Value': ''},
                  facet_col='Continent',
                  color='Variable_name',
                  facet_col_wrap=2,
                  width=700,
                  facet_col_spacing=0.04,
                  hover_name='Variable_name',
                  hover_data={'Variable': False,
                              'Year': False,
                              'Value': False,
                              'Continent': False,
                              'Variable_name': False},
                  height=600,
                  color_discrete_sequence=["#8fd1e7", "#9dcc93", "#f7be49", "#d9b5c9"],
                 )

    fig.update_yaxes(matches=None, showgrid=True, showticklabels=True)
    fig.update_xaxes(range=[2005, 2021])

    fig.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
    fig.update_xaxes(showticklabels=True, col=2, row=2)

    dots = px.scatter(df[df.Year == 2020],
                      x='Year',
                      y='Value',
                      labels={'Year': '', 'Value': ''},
                      facet_col='Continent',
                      color='Variable_name',
                      facet_col_wrap=2,
                      width=700,
                      facet_col_spacing=0.04,
                      hover_name='Variable_name',
                      hover_data={'Variable': False,
                                  'Year': False,
                                  'Value': False,
                                  'Continent':False,
                                  'Variable_name':False},
                      height=600,
                      color_discrete_sequence=["#8fd1e7", "#9dcc93", "#f7be49", "#d9b5c9"],
                      )
    dots.update_traces(marker=dict(size=10, opacity=1))
    dots.update_layout(showlegend=False)

    fig.add_traces(dots.data)
    fig.update_layout(legend=dict(
        yanchor="bottom",
        y=0.01,
        xanchor="right",
        x=1
    ))

    fig.update_layout(margin={"r": 25, "t": 25, "l": 25, "b": 25})
    return fig


def Heatmap(data):

    df = data[(data.Aggregation == 'Dimension') & (data.Year == 2020)]
    df = df.groupby(['Continent', 'Variable', 'Variable_name']).mean()[
        'Value'].reset_index().pivot(index='Continent', columns='Variable_name')

    fig = go.Figure(data=go.Heatmap(z=df['Value'].T,
                                    x=df.index,
                                    zmin=0,
                                    zmax=100,
                                    y=df['Variable'].columns,
                                    colorscale=[(0.0, "#fc8d59"),
                                                (0.6, "#ffffbf"),
                                                (1, "#14ac9c")]
                                    )
                    )

    return fig


def cat_heatmap(data):
    df = data[(data.Aggregation == 'Category') & (data.Year == 2020)]
    df = df.dropna().groupby(['Variable', 'Continent', 'Variable_name']).mean().reset_index()
    df = df.round(2)
    cats = ['EE', 'EW', 'SL', 'ME',
            'EQ', 'GE', 'BE', 'CV',
            'AB', 'GB', 'SE', 'SP',
            'GV', 'GT', 'GJ', 'GN']
    df = df.set_index('Variable').T[cats].T.reset_index()

    fig = px.scatter(df,
                     y='Variable',
                     x='Value',
                     facet_col='Continent',
                     facet_col_spacing=0.05,
                     hover_name='Variable_name',
                     hover_data={'Value': True, 'Continent': False},
                     labels={'Variable': '', 'Value': ''},
                     )
    fig.update_xaxes(showgrid=False, range=[0, 100])
    fig.update_traces(marker=dict(size=12, opacity=0.8, color='#14ac9c'))
    fig.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))

    bars = px.bar(df,
                  y='Variable',
                  x='Value',
                  facet_col='Continent',
                  facet_col_spacing=0.05,
                  hover_name='Variable_name',
                  hover_data={'Value': True, 'Continent': False},
                  labels={'Variable': '', 'Value': ''},
                  orientation='h',
                  opacity=0.6,
                  )
    bars.update_traces(marker_color='#14ac9c',
                       width=0.1,
                       marker_line_width=0.1, opacity=0.8)
    fig.add_traces(bars.data)

    fig.update_layout(margin={"r": 20, "t": 20, "l": 20, "b": 20})

    return fig


def Table(data):
    df = data[(data.Year == 2020) & (data.Aggregation.isin(['Dimension']))].groupby(['Variable_name', 'Continent']).mean()
    df = df.reset_index().pivot(index=['Continent'], columns='Variable_name', values='Value')
    df.columns.name = None
    df = df.round(2).reset_index()
    table = dash_table.DataTable(id='table',
                                 columns=[{"name": i, "id": i} for i in df.columns],
                                 data=df.to_dict('records'),
                                 style_as_list_view=True,
                                 style_header={'backgroundColor': 'white',
                                               'fontWeight': 'bold',
                                               'text_align': 'left',
                                               'font_size': '12px',
                                               'border': '1px solid rgb(0, 0, 0, 0.1)',
                                               },
                                 style_cell={'font_family': 'roboto',
                                             'font_size': '12px',
                                             'text_align': 'left',
                                             'border': '0px solid rgb(0, 0, 0, 0.1)',
                                             'opacity': '0.7',
                                             },
                                 style_data_conditional=[{'if': {'row_index': 'odd'},
                                                          'backgroundColor': 'rgb(0, 0, 0, 0.1)',
                                                          }]
                                 )
    return table


def create_layout(app):
    # Page layouts
    return html.Div(
        [
            html.Div([Header(app)]),
            # page 1
            html.Div(
                [
                    # ISO sel
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.H5(f"{cover} countries covered"),
                                    html.Br([]),
                                    html.P(
                                        "",
                                        style={"color": "#ffffff", 'font-size': '13px'},
                                        className="row",
                                    ),
                                ],
                                className="product",
                            )
                        ],
                        className="row",
                    ),
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.H6(
                                        "Index Regional Trend",
                                        className="subtitle padded",
                                    ),
                                    dcc.Graph(figure=Index_trend(data),
                                              config={'displayModeBar': False}),

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
                                    html.H6(
                                        "Dimension World Trends",
                                        className="subtitle padded",
                                    ),
                                    dcc.Graph(figure=dimension_trend(data),
                                              config={'displayModeBar': False}),

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
                                    html.H6(
                                        "Dimensions by Continent",
                                        className="subtitle padded",
                                    ),
                                    Table(data),


                                ],
                                className="twelve columns",
                            ),
                        ],
                        className="row",
                    ),
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.H6(
                                        "Categories by Continent",
                                        className="subtitle padded",
                                    ),
                                    dcc.Graph(figure=cat_heatmap(data),
                                              config={'displayModeBar': False}),

                                ],
                                className="twelve columns",
                            ),
                        ],
                        className="row",
                    ),
                    # ROW 1
                ],

                className="sub_page",
            ),
        ],
        className="page",
    )
