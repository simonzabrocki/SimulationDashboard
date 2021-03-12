import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px

from utils import Header
from app import app, ISO_options, indicator_data, indicator_properties, dimension_properties


indicator_properties['display_name'] = indicator_properties['Indicator'] + \
    ': ' + indicator_properties['Description']


dimension_options = dimension_properties.Dimension.values


def indicator_line_charts(data, indicator_properties, ISO_list, Indicator):
    indicator_properties = indicator_properties.set_index('Indicator')

    df = data[(data.ISO.isin(ISO_list)) & (data.Indicator == Indicator)]
    title = indicator_properties.loc[Indicator]['Description']
    xaxis_title = indicator_properties.loc[Indicator]['Unit']
    fig = px.scatter(df,
                     x='Year',
                     y='Value',
                     color='ISO',
                     hover_data={'Value': True,
                                 'Year': True,
                                 'Country': True,
                                 'Source': True,
                                 'From': True,
                                 'Imputed': True,
                                 'Corrected': True,
                                 },
                     height=400,
                     )
    fig.update_layout(title=title, yaxis_title=xaxis_title)
    fig.update_traces(mode='lines+markers')
    fig.update_layout(margin={"r": 0, "t": 30, "l": 0, "b": 0})

    return fig


@app.callback(
    dash.dependencies.Output('indicator_select', 'options'),
    [dash.dependencies.Input('dimension_select', 'value')])
def update_indicator_select(dimension):
    props = indicator_properties[indicator_properties.Dimension == dimension].sort_values(by='Indicator')

    indicator_options = props[['Indicator', 'display_name']].values

    return [{'label': display_name, 'value': indicator} for indicator, display_name in indicator_options]


@app.callback(
    dash.dependencies.Output('indicator_select', 'value'),
    [dash.dependencies.Input('dimension_select', 'value')])
def update_indicator_select(dimension):
    props = indicator_properties[indicator_properties.Dimension == dimension].sort_values(by='Indicator')

    indicator_options = props[['Indicator', 'display_name']].values

    return indicator_options[0][0]


@app.callback(
    dash.dependencies.Output('indicator_line_charts', 'figure'),
    [dash.dependencies.Input('indicator_select', 'value'),
     dash.dependencies.Input('ISO_select', 'value')])
def update_indicator_line_charts(Indicator, ISO_list):
    return indicator_line_charts(indicator_data, indicator_properties, ISO_list, Indicator)


layout = html.Div(
    [
        html.Div([Header(app)]),
        # page 1
        html.Div(
            [
                html.Div(
                    [
                        html.Div(
                            [
                                html.H6(
                                    "Dimension",
                                    className="subtitle padded",
                                ),
                                html.Div([dcc.RadioItems(id="dimension_select", options=[{'label': dimension, 'value': dimension} for dimension in dimension_options], value='Efficient and Sustainable Resource Use')],
                                         style={'width': '100%',
                                                'display': 'inline-block',
                                                'align-items': 'center',
                                                'justify-content': 'center',
                                                'font-size': '12px'}
                                         ),
                                html.H6(
                                    "Indicator",
                                    className="subtitle padded",
                                ),
                                html.Div([dcc.Dropdown(id="indicator_select", value='EE1')],
                                         style={'width': '100%',
                                                'display': 'inline-block',
                                                'align-items': 'center',
                                                'justify-content': 'center',
                                                'font-size': '12px'},
                                         ),
                                html.H6(
                                    "Countries",
                                    className="subtitle padded",
                                ),
                                html.Div([dcc.Dropdown(id="ISO_select", options=[{'label': country, 'value': iso} for iso, country in ISO_options], value=['DEU', 'FRA'], multi=True)],
                                         style={'width': '100%',
                                                'display': 'inline-block',
                                                'align-items': 'right',
                                                'justify-content': 'right',
                                                'font-size': '12px'}
                                         ),
                            ],
                            className='pretty_container four columns'
                        ),
                        html.Div(
                            [
                                html.H6(
                                    "Line chart",
                                    className="subtitle padded",
                                ),
                                dcc.Graph(id='indicator_line_charts',
                                          config={'displayModeBar': False}
                                          ),
                            ],
                            className='pretty_container eight columns'),
                    ],
                    className='row'
                ),
            ],
            className="row",
        ),
    ],
    className="page",
)
