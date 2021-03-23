import dash_html_components as html
import dash_core_components as dcc
import pandas as pd
import dash
from app import app, ISO_options
from dash.dependencies import Input, Output
from utils import Header
import plotly.express as px
from GM.demo_script import run_EW_scenario, data_dict_expanded
from dash.exceptions import PreventUpdate


scenarios_results = {}

# See if we can change to more smooth scenario
scenarios_results['BAU'] = run_EW_scenario(data_dict_expanded)


def scenario_box(scenario_id='_one'):
    layout = html.Div(

        [
            html.H5(f'Scenario{scenario_id}'),
            html.Br([]),
            html.P('Water Price annual increase', style={'font-size': 17}),
            dcc.Slider(
                id=f'WP-slider{scenario_id}',
                min=0.80,
                max=1.2,
                step=None,
                value=1,
                marks={
                    0.80: {'label': '-20%', 'style': {'color': 'white'}},
                    0.90: {'label': '-10%', 'style': {'color': 'white'}},
                    1: {'label': '0%', 'style': {'color': 'white'}},
                    1.1: {'label': '+10%', 'style': {'color': 'white'}},
                    1.2: {'label': '+20%', 'style': {'color': 'white'}},

                },
                included=False,
            ),
            html.Br([]),
            html.P('Irrigation Water Efficiency annual increase',
                   style={'font-size': 17}),
            dcc.Slider(
                id=f'WRR-slider{scenario_id}',
                step=None,
                value=1,
                min=1,
                max=1.01,
                marks={
                    1: {'label': '0%', 'style': {'color': 'white'}},
                    1.005: {'label': '0.5%', 'style': {'color': 'white'}},
                    1.01: {'label': '+1%', 'style': {'color': 'white'}},
                },
                included=False,
            ),

        ],
        className='row')

    return layout


def scenario_building_box():
    layout = html.Div(
        [
            html.H5(
                "Scenario Building",
                className="subtitle padded",
            ),
            html.Br([]),
            html.Div(
                [
                    scenario_box(scenario_id='_one'),
                ],
                className='product_A'
            ),
            html.Div(
                [
                    scenario_box(scenario_id='_two'),
                ],
                className='product_B'
            ),
            html.Div(
                [
                    html.Button('Run', id='btn-run', n_clicks=0),
                    dcc.Loading(
                        id="loading-scenario",
                        children=html.Div(id='loading-output'),
                        type="dot",
                    ),
                ],
                className='row'
            ),
        ],
        className='row'
    )

    return layout


layout = html.Div(
    [
        dcc.Store(id='local-store', storage_type='session'),
        dcc.Store(id='results-local-store', storage_type='session', data={}),
        html.Div([Header(app)]),
        html.Div(
            [
                scenario_building_box()
            ],
            className="pretty_container four columns",
        ),
        html.Div(
            [
                html.Div(
                    [
                        html.H6(
                            "Simulation Results",
                            className="subtitle padded",
                        ),
                        html.Div([dcc.Dropdown(id="ISO_run_results",
                                               options=[{'label': country, 'value': iso} for iso, country in ISO_options],
                                               value='FRA')],
                                 style={'width': '100%',
                                        'display': 'inline-block',
                                        'align-items': 'center',
                                        'justify-content': 'center',
                                        'font-size': '20px'}
                                 ),
                        html.Div(
                            [
                                dcc.Graph(id='results-graph-1',
                                          config={'displayModeBar': False}),
                                dcc.Graph(id='results-graph-2',
                                          config={'displayModeBar': False}),
                            ],
                            className='row'),
                        html.H6(
                            "Socio-economic context",
                            className="subtitle padded",
                        ),
                        html.Div(
                            [
                                dcc.Graph(id='context-graph-1',
                                          config={'displayModeBar': False}),
                            ],
                            className='row'),
                    ],
                    className='pretty_container eight columns'
                )
            ],
            className='row'
        ),
    ],
    className="page",
)


@app.callback(
    Output("local-store", "data"),
    [
        Input("WRR-slider_one", "value"),
        Input("WP-slider_one", "value"),
        Input("WRR-slider_two", "value"),
        Input("WP-slider_two", "value"),
    ],
)
def update_scenario_parameters(WRR_1, WP_1, WRR_2, WP_2):
    return {'WRR_1': WRR_1, 'WP_1': WP_1, 'WRR_2': WRR_2, 'WP_2': WP_2}


@app.callback(
    Output("results-local-store", "data"),
    Output("loading-output", "children"),
    [
        Input("local-store", "data"),
        Input("btn-run", "n_clicks"),
    ],
)
def run_scenario(data, n_clicks):

    data = data.copy()

    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    if 'btn-run' in changed_id:
        scenarios_results['scenario_one'] = run_EW_scenario(
            WP_rate=data['WP_1'], WRR_rate=data['WRR_1'])
        scenarios_results['scenario_two'] = run_EW_scenario(
            WP_rate=data['WP_2'], WRR_rate=data['WRR_2'])

        # do case by case to not save too much data
        return {
            'scenario_one': {
                'EW1': scenarios_results['scenario_one']['EW1'].reset_index().to_json(),
                'EW2': scenarios_results['scenario_one']['EW2'].reset_index().to_json(),
                'GDPC': scenarios_results['scenario_one']['GDPC'].reset_index().to_json(),
            },
            'scenario_two': {
                'EW1': scenarios_results['scenario_two']['EW1'].reset_index().to_json(),
                'EW2': scenarios_results['scenario_two']['EW2'].reset_index().to_json(),
                'GDPC': scenarios_results['scenario_one']['GDPC'].reset_index().to_json(),
            },
        }, None

    else:  # https://community.plotly.com/t/how-to-leave-callback-output-unchanged/7276/8
        raise PreventUpdate


@app.callback(
    Output('context-graph-1', 'figure'),
    Output("results-graph-1", "figure"),
    Output("results-graph-2", "figure"),
    [
        Input("results-local-store", "data"),
        Input('ISO_run_results', 'value')
    ],
)
def plot_scenario_results(results_data, ISO):
    """TO CLEAN UP !!!!!!!!! EXPERIMENT ONLY still ugly"""
    # FIND WAY TO FORMAT A BIT MORE CLEANLY
    results_data['BAU'] = scenarios_results['BAU']

    df_1 = format_var_df('EW1', results_data)
    df_2 = format_var_df('EW2', results_data)

    df_context_1 = format_var_df('GDPC', results_data)

    # Wrap graph in function
    context_fig_1 = scenario_line_plot('GDPC', df_context_1, ISO)
    fig_1 = scenario_line_plot('EW1', df_1, ISO)
    fig_2 = scenario_line_plot('EW2', df_2, ISO)

    return context_fig_1, fig_1, fig_2


def scenario_line_plot(var, df, ISO):  # ugly af
    fig = px.line(df.query(f"ISO == '{ISO}' and Year >= 2000"),
                  x='Year',
                  y=var,
                  color='scenario',
                  color_discrete_map={'scenario_one': '#D8A488',
                                      'scenario_two': '#86BBD8',
                                      'BAU': '#A9A9A9'},
                  )

    fig.add_vline(x=2019, line_width=3, line_dash="dash", line_color="green")
    
    return fig


def format_var_df(var, results_data):
    '''TO CLEAN UP'''
    dfs = []
    for scenario, res_dict in results_data.items():

        if scenario == 'BAU':
            df = res_dict[var].to_frame(name=var).assign(
                scenario=scenario).reset_index()

        else:
            df = pd.read_json(res_dict[var]).assign(
                scenario=scenario).rename(columns={'0': var})

        dfs.append(df)

    return pd.concat(dfs, axis=0)


def make_var_df(var, scenarios_results=scenarios_results):
    dfs = []
    for scenario, res_dict in scenarios_results.items():
        dfs.append(res_dict[var].to_frame(
            name=var).assign(scenario=scenario))
    return pd.concat(dfs, axis=0)


# Add WP and WRR time series
