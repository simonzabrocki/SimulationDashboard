import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import dash_table
from utils import Header, Footer
from app import app, data, INDEX_YEAR
import dash



def Index_trend(data):
    df = data[(data.Aggregation == 'Index')].groupby(['Year', 'Continent']).mean().reset_index()
    df = df.round(2)

    fig = px.line(df,
                  x='Year',
                  y='Value',
                  color='Continent',
                  hover_data={'Value': True, 'Year': False, 'Continent': True},
                  labels={'Value': 'Score', 'Continent': 'Region'},
                  color_discrete_sequence=px.colors.qualitative.Set2,
                  height=500)

    fig.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
    fig.update_yaxes(visible=True)
    fig.update_xaxes(range=[2005, INDEX_YEAR + 2])
    fig.update_traces(mode='lines', hovertemplate="%{y}", opacity=0.7)

    dots = px.scatter(df[df.Year == INDEX_YEAR],
                      x='Year',
                      y='Value',
                      color='Continent',
                      hover_data={
                                'Value': False,
                                'Year': False,
                                'Continent': False
                                },
                      labels={'Value': 'Score', 'Continent': 'Region'},
                      color_discrete_sequence=px.colors.qualitative.Set2,
                      )

    for plot in dots.data:
        plot['showlegend'] = False

    dots.update_traces(marker_size=10)
    fig.add_traces(dots.data)
    fig.update_layout(hovermode="x")
    return fig


def dimension_trend(data):

    df = data[(data.Aggregation.isin(['Dimension']))].groupby(
        ["Variable_name", 'Variable', 'Year', 'Continent']).mean().reset_index()
    df['Value'] = df['Value'].round(2)

    fig = px.line(df,
                  x='Year',
                  y='Value',
                  labels={'Year': 'Year', 'Value': 'Score', 'Variable_name': 'Dimension'},
                  facet_col='Continent',
                  color='Variable_name',
                  facet_col_wrap=2,
                  facet_col_spacing=0.04,
                  hover_data={'Variable': False,
                              'Year': False,
                              'Value': False,
                              'Continent': False,
                              'Variable_name': False},
                  height=700,
                  color_discrete_sequence=["#8fd1e7", "#9dcc93", "#f7be49", "#d9b5c9"],
                  )

    fig.update_yaxes(matches=None, showgrid=True, showticklabels=True)
    fig.update_xaxes(range=[2005, INDEX_YEAR + 2])
    fig.update_traces(mode='lines', hovertemplate="%{y}",)

    dots = px.scatter(df[df.Year == INDEX_YEAR],
                      x='Year',
                      y='Value',
                      labels={'Year': 'Year', 'Value': 'Score'},
                      facet_col='Continent',
                      color='Variable_name',
                      facet_col_wrap=2,
                      facet_col_spacing=0.04,
                      hover_data={'Variable': False,
                                  'Year': False,
                                  'Value': False,
                                  'Continent': False,
                                  'Variable_name': False},
                      height=700,
                      color_discrete_sequence=["#8fd1e7", "#9dcc93", "#f7be49", "#d9b5c9"],
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

    return fig


def category_lolipop(data):

    df = data[(data.Aggregation == 'Category') & (data.Year == INDEX_YEAR)]
    df = df.dropna().groupby(
        ['Variable', 'Continent', 'Variable_name', 'Dimension']).mean().reset_index()
    df = df.round(2).sort_values(by='Dimension')

    fig = px.scatter(df,
                     y='Variable',
                     x='Value',
                     color='Dimension',
                     facet_col='Continent',
                     facet_col_spacing=0.05,
                     hover_name='Variable_name',
                     hover_data={'Value': True, 'Continent': False, 'Variable': False},
                     labels={'Variable': 'Category', 'Value': 'Score'},
                     color_discrete_map={
                         "Social Inclusion": "#d9b5c9",
                         "Natural Capital Protection": "#f7be49",
                         "Efficient and Sustainable Resource Use": "#8fd1e7",
                         "Green Economic Opportunities": "#9dcc93",
                     },
                     height=600,
                     )
    fig.update_xaxes(showgrid=True, range=[0, 100], tickvals=[
                     20, 40, 60, 80], visible=True, title='')
    fig.update_yaxes(showgrid=False, range=[-1, 16])

    fig.update_traces(marker=dict(size=12, opacity=0.8))
    fig.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))

    bars = px.bar(df,
                  y='Variable',
                  x='Value',
                  facet_col='Continent',
                  facet_col_spacing=0.05,
                  hover_name='Variable_name',
                  hover_data={'Value': True, 'Continent': False},
                  labels={'Variable': '', 'Value': '', 'Continent': 'Region'},
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


def Table(data):

    df = data[(data.Year == INDEX_YEAR) & (data.Aggregation.isin(['Dimension']))
              ].groupby(['Variable', 'Continent']).mean()
    df = df.reset_index().pivot(index=['Continent'], columns='Variable', values='Value')
    df.columns.name = None
    df = df.round(2).reset_index()
    df = df.rename(columns={'Continent': 'Region'})
    header_name = {'ESRU': 'Efficient and sustainable resource use',
                   'NCP': 'Natural capital protection',
                   'SI': 'Social inclusion',
                   'GEO': 'Green economic opportunities'
                   }

    tooltip = {key: {
        'value': header_name[key],
        'use_with': 'both'  # both refers to header & data cell
    } for key in header_name}
    table = dash_table.DataTable(id='table',
                                 columns=[{"name": i, "id": i} for i in df.columns],
                                 data=df.to_dict('records'),
                                 style_as_list_view=True,
                                 sort_action="native",
                                 tooltip=tooltip,
                                 style_header={'backgroundColor': 'white',
                                               'fontWeight': 'bold',
                                               'text_align': 'center',
                                               'font_size': '12px',
                                               'border': '1px solid rgb(0, 0, 0, 0.1)',
                                               },
                                 style_cell={'font_family': 'roboto',
                                             'font_size': '12px',
                                             'text_align': 'center',
                                             'border': '0px solid rgb(0, 0, 0, 0.1)',
                                             'opacity': '0.7',
                                             },
                                 style_data_conditional=[{'if': {'row_index': 'odd'},
                                                          'backgroundColor': 'rgb(0, 0, 0, 0.1)',
                                                          }]
                                 )
    return table


def dcc_config(file_name):
    return {'toImageButtonOptions': {'format': 'png',
                                     'filename': f'{file_name}.png',
                                     'scale': 2,
                                     },
            'displaylogo': False,
            'modeBarButtonsToRemove': ['zoom2d', 'pan2d',
                                       'select2d', 'lasso2d',
                                       'zoomIn2d', 'zoomOut2d', 'toggleSpikelines', 'autoScale2d']}


cover = data[(data.Aggregation == 'Index') & (data.Year == INDEX_YEAR)].dropna(subset=['Value']).shape[0]



def conditional_color_col(col):
    return [
            {
                'if': {
                    'filter_query': f'\u007b{col}\u007d > 60', # comparing columns to each other
                    'column_id': f'{col}'
                },
                'backgroundColor': '#14ac9c'
            },
            {
                'if': {
                    'filter_query': f'\u007b{col}\u007d > 40 && \u007b{col}\u007d  < 60', # comparing columns to each other
                    'column_id': f'{col}'
                },
                'backgroundColor': '#ffffbf'
            },
            {
                'if': {
                    'filter_query': f'\u007b{col}\u007d > 20 && \u007b{col}\u007d  < 40', # comparing columns to each other
                    'column_id': f'{col}'
                },
                'backgroundColor': '#fc8d59'
            },
            {
                'if': {
                    'filter_query': f'\u007b{col}\u007d < 20 && \u007b{col}\u007d > 1', # comparing columns to each other
                   'column_id': f'{col}'
                },
                'backgroundColor': '#f14326'
            }
        ]


def region_table(data, Continent='Africa'):
    table_df = data[(data.Year == INDEX_YEAR) & (data.Aggregation.isin(['Index', 'Dimension'])) & (data.Continent.isin([Continent]))].pivot(
        index=['Country', 'UNregion'], columns='Variable', values='Value')[['Index', 'ESRU', 'NCP', 'SI', 'GEO']]
    table_df = table_df.reset_index().rename(columns={"UNregion": 'Subregion'})
    table_df['Rank'] = table_df.Index.rank(ascending=False)
    table_df = table_df[['Country', 'Subregion', 'Rank', 'Index', 'ESRU', 'NCP', 'SI', 'GEO']]
    
    header_name = {'Index': 'Index',
                   'Rank': 'Rank',
                   'ESRU': 'Efficient and sustainable resource use',
                   'NCP': 'Natural capital protection',
                   'SI': 'Social inclusion',
                   'GEO': 'Green economic opportunities',
                   }

    table = dash_table.DataTable(id='continent-table',
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
                                style_data_conditional=conditional_color_col('Index') + conditional_color_col('ESRU') + conditional_color_col('NCP') + conditional_color_col('SI') + conditional_color_col('GEO'),
                                )
    return table

continent_options = data.Continent.unique()

layout = html.Div(
    [
        html.Div([Header(app, 'Regional Outlook')]),
        # page 1
        html.Div(
            [
                # ISO sel
                html.Div(
                    [
                        html.Div(
                            [
                                html.H5(f"Highlights"),
                                html.Br([]),
                                html.P(
                                    "Average scores for the Green Growth Index are provided for countries within five geographic regions – Africa, the Americas, Asia, Europe, and Oceania. Although the trends differ across regions for the four green growth dimensions, green economic opportunities is consistently below targets and largely stable across time, except in Europe where the trend is rising slightly and greater than other regions. Another positive trend to note is that across all regions, social inclusion scores have risen systematically over the past 15 years. This is especially true in areas with many developing countries like Asia and Africa.",
                                    style={"color": "#ffffff", 'font-size': '15px'},
                                    className="row",
                                ),
                            ],
                            className="product",
                        )
                    ],
                    className="pretty_container four columns",
                ),
                html.Div(
                    [
                        html.Div(
                            [
                                html.Div(
                                    [
                                        html.H6(
                                            "Index Regional Trends",
                                            className="subtitle padded",
                                        ),
                                        dcc.Graph(figure=Index_trend(data),
                                                  config=dcc_config('Index_Regional_Trends'),
                                                  id='Index Regional Trends'),
                                        html.H6(
                                            "Dimension Regional Trends",
                                            className="subtitle padded",
                                        ),
                                        dcc.Graph(figure=dimension_trend(data),
                                                  config=dcc_config('Dimension_Regional_Trends'),
                                                  id="Dimension Regional Trends"),
                                        html.H6(
                                            f"{INDEX_YEAR} Dimensions by Region",
                                            className="subtitle padded",
                                        ),
                                        Table(data),
                                        html.H6(
                                            f"{INDEX_YEAR} Indicators by Region",
                                            className="subtitle padded",
                                        ),
                                        dcc.Graph(figure=category_lolipop(data),
                                                  config=dcc_config('Indicators_Regional_DotPlot'),
                                                  id=f"{INDEX_YEAR} Indicators by Region"),
                                        html.H6(
                                            f"Index table",
                                            className="subtitle padded",
                                        ),
                                        dcc.Dropdown(id="continent_select",
                                               options=[{'label': continent, 'value': continent}
                                                        for continent in continent_options],
                                               value='Africa'),
                                        html.P(),
                                        region_table(data),
                                    ],
                                    className="twelve columns",
                                )
                            ],
                            className="row",
                        ),
                    ],
                    className="pretty_container eight columns"),
                # ROW 1
            ],
            className="row",
        ),
        Footer(),
    ],
    
    className="page",
)

@app.callback(
    dash.dependencies.Output('continent-table', 'data'),
    [dash.dependencies.Input('continent_select', 'value')],
    suppress_callback_exceptions=True)
def update(continent):
    table_df = data[(data.Year == INDEX_YEAR) & (data.Aggregation.isin(['Index', 'Dimension'])) & (data.Continent.isin([continent]))].pivot(
    index=['Country', 'UNregion'], columns='Variable', values='Value')[['Index', 'ESRU', 'NCP', 'SI', 'GEO']]
    table_df = table_df.reset_index().rename(columns={"UNregion": 'Subregion'})
    table_df['Rank'] = table_df.Index.rank(ascending=False)


    return table_df.to_dict('records')