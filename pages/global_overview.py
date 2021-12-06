import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import dash_table
from utils import Header
import dash
from dash.dependencies import Input, Output
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
        index=['Country', 'Continent', 'Sub-region'], columns='Variable', values='Value')[['Index', 'ESRU', 'NCP', 'GEO', 'SI']]
    table_df = table_df.reset_index().rename(columns={"Sub-region": 'Subregion'})

    header_name = {'Index': 'Index',
                   'ESRU': 'Efficient and sustainable resource use',
                   'NCP': 'Natural capital protection',
                   'GEO': 'Green economic opportunities',
                   'SI': 'Social inclusion',
                   }

    table = dash_table.DataTable(id='index-table',
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
                                                          },
                                                          {
                                                            "if": {"state": "selected"},
                                                            "backgroundColor": "rgba(45, 178, 155, 0.3)",
                                                            "border": "1px solid green",
                                                        }
                                                          ],
                                export_format="csv",
                                 )
    return table


# To put elsewhere
def get_text_metrics(data):
    index_2020 = data.query("Aggregation == 'Index' and Year == 2020")

    n_ISO_continent = index_2020.groupby('Continent').apply(lambda x: x.ISO.unique().shape[0])
    n_ISO = n_ISO_continent.sum()
    n_high_score = index_2020.query('Value > 60 and Value < 80').shape[0]
    n_low_score = index_2020.query('Value > 20 and Value < 40').shape[0]
    
    n_very_low_score = index_2020.query('Value < 20').shape[0]
    
    top_country = index_2020.sort_values(by="Value", ascending=False).head(1)
    return n_ISO, n_ISO_continent, n_high_score, n_low_score, n_very_low_score, top_country


n_ISO, n_ISO_continent, n_high_score, n_low_score, n_very_low, top_country = get_text_metrics(data)


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
                                html.P(f"In {INDEX_YEAR}, there are {n_ISO} countries with scores for the Green Growth Index, with {n_ISO_continent.loc['Africa']} countries in Africa, {n_ISO_continent.loc['Americas']} countries in the Americas, {n_ISO_continent.loc['Asia']} countries in Asia, {n_ISO_continent.loc['Europe']} countries in Europe, and only {n_ISO_continent.loc['Oceania']} in Oceania. The scores of almost half of the countries are in the middle range, between 40 and 60, covering about 77 million m2 of the global land area. There are {n_high_score} countries that reached a high score between 60 and 80, many of them are in Europe. Those {n_low_score} countries with low scores, between 20 and 40, are mainly from Africa and Asia. There are no countries with very low scores of below 20. {top_country['Country'].iloc[0]}, located in {top_country['Sub-region'].iloc[0]}, has the highest Green Growth Index with a score of {top_country['Value'].iloc[0]}, which is still further away from reaching the sustainability target of 100.",
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

@app.callback(
    Output("index-table", "style_data_conditional"),
    Input("index-table", "active_cell"),
)
def style_selected_rows(active_cell):
    if active_cell is None:
        return dash.no_update

    css = [
        {'if': {'row_index': 'odd'},
    'backgroundColor': 'rgb(0, 0, 0, 0.1)',
        },
        {"if": {'row_index': active_cell['row']},
            "backgroundColor": "rgba(45, 178, 155, 0.3)",
            "border": "1px solid green",
            },
           {
        # 'active' | 'selected'
        "if": {"state": "selected"},
        "backgroundColor": "rgba(45, 178, 155, 0.3)",
        "border": "1px solid green",
    }, 
    
    ]
    return css
