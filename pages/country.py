import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go

from utils import Header, make_dash_table
import pandas as pd
import pathlib

PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../data").resolve()

data = pd.read_csv(DATA_PATH.joinpath('GGGI/GGIs_2015_2020.csv'))

ISO_options = data[['ISO', 'Country']].drop_duplicates().values


def create_layout(app):
    # Page layouts
    return html.Div(
        [
            html.Div([Header(app)]),
            # page 1
            html.Div(
                [
                    #ISO sel
                    html.Div([dcc.Dropdown(id="ISO_select", options=[{'label': country, 'value': iso} for iso, country in ISO_options], value='FRA')],
                             style={'width': '100%',
                                    'display': 'inline-block',
                                    'align-items': 'center',
                                    'justify-content': 'center'}
                             ),
                    html.Div(id='Description'),

                    # ROW 1
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.H6(["Dimensions"], className="subtitle padded"),
                                    dcc.Graph(id='Dim_ISO'),
                                ],
                                className="six columns",
                            ),
                            html.Div(
                                [
                                    html.H6(["Categories"], className="subtitle padded"),
                                    dcc.Graph(id='Perf_ISO'),
                                ],
                                className="six columns",
                            ),
                        ],
                        className="row",
                    ),
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.H6(
                                        "Index over time",
                                        className="subtitle padded",
                                    ),
                                    dcc.Graph(id='index_time_series')

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
                                        "Dimensions over time",
                                        className="subtitle padded",
                                    ),
                                    dcc.Graph(id='dim_time_series'),


                                ],
                                className="twelve columns",
                            )
                        ],
                        className="row",
                    ),
                ],

                className="sub_page",
            ),
        ],
        className="page",
    )
