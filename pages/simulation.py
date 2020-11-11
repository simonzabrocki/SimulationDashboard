'''Simulation page, as of november 11th 2020 this page is a toy example'''

import dash_html_components as html
from utils import Header
from app import app
import dash_core_components as dcc
import numpy as np
import plotly.graph_objects as go
import dash


def f(x, L, k, xo):
    x = x - 2020
    return L / (1 + np.exp(-k * (x - xo))) - L / (1 + np.exp(k * xo)) + 10


L_range = [20, 70]
k_range = [0.1, 0.5]
x0_range = [5, 25]

scenarios = {
    'Strong investment': [60, 0.4, 5],
    'Business as usual': [30, 0.1, 10],
    'Moderate investment': [40, 0.3, 10],
}
scenarios_dashline = {
    'Strong investment': 'dot',
    'Business as usual': 'dash',
    'Moderate investment': 'dashdot',
}


def plot(L, k, x0):
    x = np.array([i for i in range(2020, 2050)])

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            visible=True,
            line=dict(color="#14ac9c", width=3),
            x=x,
            y=f(x, L, k, x0),
            name='Current Scenario'
        )
    )
    for scenario in scenarios:
        L_s, k_s, x0_s = scenarios[scenario]
        fig.add_trace(
            go.Scatter(
                visible=True,
                line=dict(color="darkgrey", width=1.5, dash=scenarios_dashline[scenario]),
                x=x,
                y=f(x, L_s, k_s, x0_s),
                name=scenario,
            )
        )
    fig.update_yaxes(range=[5, 80])

    fig.update_layout(xaxis_title="Year",
                      title="Share of renewable in electricity mix vs Time",
                      yaxis_title="Share of renewable (%)",)
    return fig


def parameter_slider(slider_id, parameter_range):
    return dcc.Slider(
        id=slider_id,
        min=parameter_range[0],
        max=parameter_range[1],
        step=(parameter_range[1] - parameter_range[0]) / 100,
        value=(parameter_range[1] - parameter_range[0]) / 2,
        marks={parameter_range[0]: f'{parameter_range[0]}',
               parameter_range[1]: f'{parameter_range[1]}'},
        updatemode='drag',
    )


@app.callback(
    dash.dependencies.Output('L-slider', 'value'),
    [dash.dependencies.Input('scenario-button', 'value')])
def update_L_slider(value):
    return scenarios[value][0]


@app.callback(
    dash.dependencies.Output('x0-slider', 'value'),
    [dash.dependencies.Input('scenario-button', 'value')])
def update_x_slider(value):
    return scenarios[value][2]


@app.callback(
    dash.dependencies.Output('k-slider', 'value'),
    [dash.dependencies.Input('scenario-button', 'value')])
def update_k_slider(value):
    return scenarios[value][1]


@app.callback(
    dash.dependencies.Output('L-slider-output-container', 'children'),
    [dash.dependencies.Input('L-slider', 'value'),
     dash.dependencies.Input('k-slider', 'value'),
     dash.dependencies.Input('x0-slider', 'value')])
def update_L_output(L, k, x0):
    return f'Target: {L}'


@app.callback(
    dash.dependencies.Output('k-slider-output-container', 'children'),
    [dash.dependencies.Input('L-slider', 'value'),
     dash.dependencies.Input('k-slider', 'value'),
     dash.dependencies.Input('x0-slider', 'value')])
def update_k_output(L, k, x0):
    return f'Growth Rate: {k}'


@app.callback(
    dash.dependencies.Output('x0-slider-output-container', 'children'),
    [dash.dependencies.Input('L-slider', 'value'),
     dash.dependencies.Input('k-slider', 'value'),
     dash.dependencies.Input('x0-slider', 'value')])
def update_x_output(L, k, x0):
    return f'Delay: {x0}'


@app.callback(
    dash.dependencies.Output('simu_plot', 'figure'),
    [dash.dependencies.Input('L-slider', 'value'),
     dash.dependencies.Input('k-slider', 'value'),
     dash.dependencies.Input('x0-slider', 'value')])
def update_graph(L, k, x0):
    return plot(L, k, x0)


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
                                html.H5("Simulation Tool"),
                                html.Br([]),
                                html.P(
                                    "\
                                    This is feature is still under development. The detailed models have still to be implemented. \
                                    The graph below is a 'made up' curve to display how the tool may look like.\
                                    ",
                                    style={"color": "#FF0000", 'font-size': '16px'},
                                    className="row",
                                ),
                            ],
                            className="product",
                        )
                    ],
                    className="row"),
                html.Div([
                    dcc.RadioItems(
                        id='scenario-button',
                        options=[
                            {'label': 'Business as usual', 'value': 'Business as usual'},
                            {'label': 'Moderate investment', 'value': "Moderate investment"},
                            {'label': 'Strong investment', 'value': 'Strong investment'}
                        ],
                        value='Business as usual'),
                    html.Div(id='L-slider-output-container'),
                    parameter_slider(slider_id='L-slider', parameter_range=L_range),
                    html.Div(id='k-slider-output-container'),
                    parameter_slider(slider_id='k-slider', parameter_range=k_range),
                    html.Div(id='x0-slider-output-container'),
                    parameter_slider(slider_id='x0-slider', parameter_range=x0_range),
                    dcc.Graph(id='simu_plot',
                              config={'displayModeBar': False}
                              ),
                ])


            ],

            className="sub_page",
        ),
    ],
    className="page",
)
