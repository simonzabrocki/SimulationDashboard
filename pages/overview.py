import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import plotly.express as px

from utils import Header, make_dash_table

import pandas as pd
import dash_table
import pathlib

# get relative data folder
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../data").resolve()


df_fund_facts = pd.read_csv(DATA_PATH.joinpath("df_fund_facts.csv"))
df_price_perf = pd.read_csv(DATA_PATH.joinpath("df_price_perf.csv"))

data = pd.read_csv(DATA_PATH.joinpath('GGGI/GGIs_2015_2020.csv'))


# Map to put in sep scripts later
map_df = data[(data.Year == 2020) & (data.Aggregation == 'Index')]

fig_map = px.choropleth(map_df,
                        locations="ISO",
                        color="Value",
                        hover_name="Country",
                        color_continuous_scale=px.colors.diverging.RdYlGn,
                        labels={'Value': 'Index'},
                        range_color=[0, 100],
                        )
fig_map.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0},
                      geo=dict(showframe=False,
                               showcoastlines=False,
                               ),
                      )

fig_map.update_layout(coloraxis_colorbar=dict(title="",
                                              thicknessmode="pixels", thickness=20,
                                              lenmode="pixels", len=200,
                                              dtick=20
                                              ))

# table

table_df = data[(data.Year == 2020) & (data.Aggregation.isin(['Index', 'Dimension']))].pivot(index=['Country'], columns='Variable', values='Value')[['Index', 'ESRU', 'NCP', 'SI', 'GEO']]
table_df = table_df.reset_index()
table = dash_table.DataTable(id='table',
                             columns=[{"name": i, "id": i} for i in table_df.columns],
                             data=table_df.to_dict('records'),
                             sort_action="native",
                             page_action="native",
                             page_current=0,
                             page_size=20,
                             style_as_list_view=True,
                             style_header={'backgroundColor': 'white',
                                           'fontWeight': 'bold',
                                           },
                             style_cell={'font_family': 'roboto',
                                         'font_size': '12px',
                                         'text_align': 'right'},
                             style_data_conditional=[{'if': {'row_index': 'odd'},
                                                      'backgroundColor': 'lightgrey'}]
                            )


def create_layout(app):
    # Page layouts
    return html.Div(
        [
            html.Div([Header(app)]),
            # page 1
            html.Div(
                [
                    # Row 3
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.H5("Summary"),
                                    html.Br([]),
                                    html.P(
                                        "\
                                    Green Growth Index measures country performance in achieving sustainability targets including \
                                    Sustainable Development Goals, Paris Climate Agreement, and Aichi Biodiversity Targets \
                                    for four green growth dimensions: efficient and sustainable resource use,\
                                    natural capital protection, green economic opportunities and social inclusion.",
                                        style={"color": "#ffffff"},
                                        className="row",
                                    ),
                                ],
                                className="product",
                            )
                        ],
                        className="row",
                    ),
                    # MAP
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.H6(
                                        "Green Growth Index Map 2020",
                                        className="subtitle padded",
                                    ),
                                    dcc.Graph(figure=fig_map)
                                ],
                                className="twelve columns",
                            )
                        ],
                        className="row",
                    ),
                    # Table
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.H6(
                                        "Green Growth Index Table 2020",
                                        className="subtitle padded",
                                    ),
                                    table,
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
