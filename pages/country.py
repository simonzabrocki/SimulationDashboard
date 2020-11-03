import dash_core_components as dcc
import dash_html_components as html
from utils import Header


def create_layout(app, data):
    ISO_options = data.dropna(subset=['Country'])[['ISO', 'Country']].drop_duplicates().values
    # Page layouts
    return html.Div(
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
                                    html.H6(["2020 Dimensions"], className="subtitle padded"),
                                    dcc.Graph(id='Dim_ISO',
                                              config={'displayModeBar': False}),
                                ],
                                className="six columns",
                            ),
                            html.Div(
                                [
                                    html.H6(["2020 Indicators"], className="subtitle padded"),
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
