import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px

import pandas as pd
import dash_table
import pathlib
from utils import Header

# get relative data folder
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../data").resolve()
data = pd.read_csv(DATA_PATH.joinpath('GGGI/GGIs_2015_2020.csv'))
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


def Map(data):
    map_df = data[(data.Year == 2020) & (data.Aggregation == 'Index')]
    fig_map = px.choropleth(map_df,
                            locations="ISO",
                            color="Value",
                            hover_name="Country",
                            color_continuous_scale=[(0, "#fc8d59"), (0.6, "#ffffbf"), (1, "#14ac9c")],
                            labels={'Value': 'Index'},
                            range_color=[0, 100],
                            )
    fig_map.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0},
                          geo=dict(showframe=False,
                                   showcoastlines=False,
                                   ),
                          )
    fig_map.update_traces(marker_line_width=0.3, marker_line_color='white')

    fig_map.update_layout(coloraxis_colorbar=dict(title="",
                                                  thicknessmode="pixels", thickness=20,
                                                  lenmode="pixels", len=200,
                                                  dtick=50
                                                  ))
    return fig_map


def Table(data):
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
                                               'text_align': 'left',
                                               'font_size': '13px',
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
                                        style={"color": "#ffffff", 'font-size': '13px'},
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
                                    dcc.Graph(figure=Map(data))
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
                                    Table(data),
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
