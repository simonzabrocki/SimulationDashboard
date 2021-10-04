import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import dash_table
from utils import Header
from app import app, data, INDEX_YEAR


def map_dcc_config(file_name):
    return {'toImageButtonOptions': {'format': 'png',
                                     'filename': f'{file_name}.png',
                                     'scale': 2,
                                     },
            'displaylogo': False,
            'modeBarButtonsToRemove': ['select2d', 'lasso2d',
                                       'toggleSpikelines', 'autoScale2d']}


def Map(data):
    map_df = data[(data.Aggregation == 'Index')].sort_values(by='Year')
    map_df['Year'] = map_df['Year'].astype(int)
    fig_map = px.choropleth(map_df,
                            locations="ISO",
                            color="Value",
                            hover_name="Country",
                            hover_data={"ISO": False},
                            color_continuous_scale=[(0, "#f14326"),
                                                    (0.25, "#fc8d59"),
                                                    (0.5, "#ffffbf"),
                                                    (1, "#14ac9c")],
                            labels={'Value': 'Index'},
                            range_color=[0, 100],
                            animation_frame="Year",
                            height=800,
                            )

    fig_map.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0},
                          geo=dict(showframe=False,
                                   resolution=50,
                                   showcoastlines=False,
                                   ),
                          )

    fig_map.update_traces(marker_line_width=0.3, marker_line_color='white')

    fig_map.update_layout(coloraxis_colorbar=dict(title="Score",
                                                  thicknessmode="pixels", thickness=10,
                                                  lenmode="pixels", len=200,
                                                  dtick=20
                                                  ))

    # fig_map.update_layout(sliders=[dict(active=14)])

    curr_val = {"font": {"size": 20, 'family': 'roboto'},
                "prefix": "Year: ",
                "visible": True,
                "xanchor": "center",
                }
    fig_map.layout['sliders'][0]['currentvalue'] = curr_val
    return fig_map


def Table(data):
    table_df = data[(data.Year == INDEX_YEAR) & (data.Aggregation.isin(['Index', 'Dimension']))].pivot(
        index=['Country', 'Continent', 'UNregion'], columns='Variable', values='Value')[['Index', 'ESRU', 'NCP', 'SI', 'GEO']]
    table_df = table_df.reset_index().rename(columns={"UNregion": 'Subregion'})

    header_name = {'Index': 'Index',
                   'ESRU': 'Efficient and sustainable resource use',
                   'NCP': 'Natural capital protection',
                   'SI': 'Social inclusion',
                   'GEO': 'Green economic opportunities'
                   }

    table = dash_table.DataTable(id='table',
                                 columns=[{"name": i, "id": i}
                                          for i in table_df.columns],
                                 data=table_df.to_dict('records'),
                                 sort_action="native",
                                 page_action="native",
                                 page_current=0,
                                 page_size=30,
                                 style_as_list_view=True,
                                 style_header={'backgroundColor': 'white',
                                               'fontWeight': 'bold',
                                               'text_align': 'left',
                                               'font_size': '13px',
                                               'border': '1px solid rgb(0, 0, 0, 0.1)',
                                               },
                                 tooltip_header=header_name,
                                 tooltip_delay=0,
                                 tooltip_duration=None,
                                 style_cell={'font_family': 'roboto',
                                             'font_size': '10px',
                                             'text_align': 'left',
                                             'border': '0px solid rgb(0, 0, 0, 0.1)',
                                             'opacity': '0.7',
                                             },
                                 style_data_conditional=[{'if': {'row_index': 'odd'},
                                                          'backgroundColor': 'rgb(0, 0, 0, 0.1)',
                                                          }],
                                export_format="csv",
                                 )
    return table


layout = html.Div(
    [
        html.Div([
            Header(app, 'Global Overview'),

        ]),
        html.Div(
            [
                html.Div(
                    [
                        html.Div(
                            [
                                html.H5("Highlights"),
                                html.Br([]),
                                html.P("Green Growth Index measures country performance in achieving sustainability targets including Sustainable Development Goals, Paris Climate Agreement, and Aichi Biodiversity Targets for four green growth dimensions: efficient and sustainable resource use, natural capital protection, green economic opportunities and social inclusion.",
                                       style={"color": "#ffffff", 'font-size': '15px'},),
                                html.Br([]),
                                html.P("In 2019, there are 117 countries with scores for the Green Growth Index, with 24 countries in Africa, 20 countries in the Americas, 33 countries in Asia, 38 countries in Europe, and only two in Oceania. The scores of almost half of the countries are in the middle range, between 40 and 60, covering about 77 million m2 of the global land area. There are 32 countries that reached a high score between 60 and 80, many of them are in Europe. Those 30 countries with low scores, between 20 and 40, are mainly from Africa and Asia. While there are no countries with very low scores of below 20, none has also received a very high score of over 80 in 2019. Sweden, located in Northern Europe, has the highest Green Growth Index with a score of 78.72, which is still further away from reaching the sustainability target of 100.",
                                       style={"color": "#ffffff", 'font-size': '15px'}),
                            ],
                            className="product",
                        )
                    ],
                    className="pretty_container four columns",
                ),
                html.Div(
                    [

                        html.H6(
                            f"2005-{INDEX_YEAR} Green Growth Index Map",
                            className="subtitle padded",
                        ),
                        dcc.Graph(figure=Map(data), id='world_map',
                                  config=map_dcc_config('GGI_world_map')),
                        html.H6(
                            f"{INDEX_YEAR} Green Growth Index Table",
                            className="subtitle padded",
                        ),
                        Table(data),
                    ],
                    className="pretty_container eight columns"
                ),

            ],
            className="row",
        ),
    ],
    className="page",
)
