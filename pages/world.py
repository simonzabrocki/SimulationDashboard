import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import plotly.figure_factory as ff
import plotly.express as px

from utils import Header, make_dash_table
import pandas as pd
import pathlib

PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../data").resolve()

data = pd.read_csv(DATA_PATH.joinpath('GGGI/GGIs_2015_2020.csv'))

ISO_options = data[['ISO', 'Country']].drop_duplicates().values

cover = data[(data.Aggregation == 'Index') & (data.Year == 2020)].dropna().shape[0]


def Index_Heatmap():

    df = data[(data.Aggregation == 'Index') & (data.Year == 2020)]
    df = df.groupby(['Continent', 'Variable']).mean()['Value'].reset_index().pivot(index='Continent', columns='Variable')

    fig = px.imshow(df['Value'],
              color_continuous_scale=[(0, "#fc8d59"), (0.5, "#ffffbf"), (1, "#14ac9c")],
              labels=dict(x="", y="", color="Value"),
              range_color=[0, 100],
              width=300,
              height=300)


    fig.update_layout(coloraxis_colorbar=dict(title="",
                                                  thicknessmode="pixels", thickness=10,
                                                  lenmode="pixels", len=100,
                                                  dtick=50
                                                  ))
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})

    fig.update_layout(showlegend=False)
    fig.update(layout_coloraxis_showscale=False)
    return fig


def Index_trend():
    df = data[(data.Aggregation == 'Index')].groupby('Year').mean().reset_index()
    fig = px.line(df,
                  x='Year',
                  y='Value',
                  labels = {
                     'Value': ''
                  },
                 height=300)
    fig.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
    fig.update_yaxes(visible=True, fixedrange=True)
    fig.update_traces(mode='lines+markers', line_color="#14ac9c")
    return fig

def dimension_trend():

    df = data[(data.Aggregation.isin(['Dimension'])) & (data.Year.isin([2015, 2020]))].groupby(['Variable', 'Year']).mean().reset_index()
    df['Value'] = df['Value'].round(1)
    df['Year'] = df['Year'].astype(int).astype(str)
    fig = px.scatter(df, x="Value",
                     y="Variable",
                     color='Year',
                     labels={"Variable": 'Dimension'},
                     color_discrete_map={'2020': '#14ac9c', '2015': 'darkgrey'},
    )
    fig.update_traces(marker=dict(size=25, opacity=0.6))
    fig.update_xaxes(showgrid=False, range=[0,100])

    return fig

def Heatmap():
    df = data[(data.Aggregation.isin(['Index', 'Dimension'])) & (data.Year == 2020)]
    df = df.groupby(['Continent', 'Variable']).mean()['Value'].reset_index().pivot(index='Continent', columns='Variable')
    df_plot = df['Value']
    df_plot[''] = None
    fig = px.imshow(df_plot[['Index', '','ESRU', 'GEO', 'NCP', 'SI']],
              color_continuous_scale=[(0, "#fc8d59"), (0.5, "#ffffbf"), (1, "#14ac9c")],
              labels=dict(x="", y="", color="Value"),
              range_color=[0, 100],
              width=500
    )

    fig.update_layout(coloraxis_colorbar=dict(title="",
                                                  thicknessmode="pixels", thickness=10,
                                                  lenmode="pixels", len=200,
                                                  dtick=20
                                                  ))
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    fig.layout.plot_bgcolor = '#fff'
    return fig


def create_layout(app):
    # Page layouts
    return html.Div(
        [
            html.Div([Header(app)]),
            # page 1
            html.Div(
                [
                    #ISO sel
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
                                        "Index Trend",
                                        className="subtitle padded",
                                    ),
                                    dcc.Graph(figure=Index_trend(),
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
                                        "Dimension Trends",
                                        className="subtitle padded",
                                    ),
                                    dcc.Graph(figure=dimension_trend(),
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
                                        "Index and Dimension by Continent",
                                        className="subtitle padded",
                                    ),
                                    dcc.Graph(figure=Heatmap(),
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
