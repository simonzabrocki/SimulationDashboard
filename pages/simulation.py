import dash_html_components as html
import dash_core_components as dcc
import pandas as pd
import dash
from app import app, ISO_options
from dash.dependencies import Input, Output
from utils import Header
import plotly.express as px
from GM.demo_script import scenario, data_dict_expanded
from dash.exceptions import PreventUpdate


scenarios_results = {}

# See if we can change to more smooth scenario
scenarios_results['BAU'] = scenario(data_dict_expanded)


def scenario_box(scenario_id='_one'):
    layout = html.Div(

        [
            html.H5(f'Scenario{scenario_id}'),
            html.Br([]),
            html.P('Water Price annual increase'),
            dcc.Slider(
                id=f'WP-slider{scenario_id}',
                min=0.80,
                max=1.2,
                step=None,
                value=1,
                marks={
                    0.80: {'label': '-20 %'},
                    0.90: {'label': '-10 %'},
                    1: {'label': '0 %', },
                    1.1: {'label': '+ 10 %', },
                    1.2: {'label': '+ 20 %', },

                },
                included=False,
            ),
            html.P('Irrigation Water Efficiency annual increase'),
            dcc.Slider(
                id=f'WRR-slider{scenario_id}',
                step=None,
                value=1,
                min=1,
                max=1.01,
                marks={
                    1: {'label': '0 %', },
                    1.005: {'label': '0.5 %', },
                    1.01: {'label': '+ 1 %', },
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
                        children=[html.Div(id="results-graph-2")],
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
        dcc.Store(id='local-store', storage_type='local'),
        dcc.Store(id='results-local-store', storage_type='local'),
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
                        html.Div([dcc.Dropdown(id="ISO_run_results", options=[{'label': country, 'value': iso} for iso, country in ISO_options], value='FRA')],
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
                            className='row')
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
    [
        Input("local-store", "data"),
        Input("btn-run", "n_clicks"),
    ],
)
def run_scenario(data, n_clicks):

    data = data.copy()

    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    if 'btn-run' in changed_id:
        scenarios_results['scenario_one'] = scenario(
            WP_rate=data['WP_1'], WRR_rate=data['WRR_1'])
        scenarios_results['scenario_two'] = scenario(
            WP_rate=data['WP_2'], WRR_rate=data['WRR_2'])

        return {
            'scenario_one': {
                'EW1': scenarios_results['scenario_one']['EW1'].reset_index().to_json(),
                'EW2': scenarios_results['scenario_one']['EW2'].reset_index().to_json(),
            },
            'scenario_two': {
                'EW1': scenarios_results['scenario_two']['EW1'].reset_index().to_json(),
                'EW2': scenarios_results['scenario_two']['EW2'].reset_index().to_json(),
            },
        }

    else:  # https://community.plotly.com/t/how-to-leave-callback-output-unchanged/7276/8
        raise PreventUpdate


@app.callback(
    Output("results-graph-1", "figure"),
    Output("results-graph-2", "figure"),
    Output("loading-scenario", "children"),
    [
        Input("results-local-store", "data"),
        Input('ISO_run_results', 'value')
    ],
)
def run_scenario(results_data, ISO):
    """TO CLEAN UP !!!!!!!!! EXPERIMENT ONLY"""

    df_EW1_one = pd.read_json(results_data['scenario_one']['EW1']).assign(
        scenario='scenario_one').rename(columns={'0': 'EW1'})
    df_EW1_two = pd.read_json(results_data['scenario_two']['EW1']).assign(
        scenario='scenario_two').rename(columns={'0': 'EW1'})
    EW1_BAU = scenarios_results['BAU']['EW1'].to_frame(
        name='EW1').assign(scenario='BAU').reset_index()

    df_1 = pd.concat([df_EW1_one, df_EW1_two, EW1_BAU], axis=0)

    df_EW2_one = pd.read_json(results_data['scenario_one']['EW2']).assign(
        scenario='scenario_one').rename(columns={'0': 'EW2'})
    df_EW2_two = pd.read_json(results_data['scenario_two']['EW2']).assign(
        scenario='scenario_two').rename(columns={'0': 'EW2'})

    EW2_BAU = scenarios_results['BAU']['EW2'].to_frame(
        name='EW2').assign(scenario='BAU').reset_index()

    df_2 = pd.concat([df_EW2_one, df_EW2_two, EW2_BAU], axis=0)

    fig_1 = px.line(df_1.query(f"ISO == '{ISO}' and Year >= 2000"),
                    x='Year', y='EW1', color='scenario', color_discrete_map={'scenario_one': '#D8A488', 'scenario_two': '#86BBD8', 'BAU': '#A9A9A9'},)

    fig_1.add_vline(x=2019, line_width=3, line_dash="dash", line_color="green")

    fig_2 = px.line(df_2.query(f"ISO == '{ISO}' and Year >= 2000"),
                    x='Year', y='EW2', color='scenario', color_discrete_map={'scenario_one': '#D8A488', 'scenario_two': '#86BBD8', 'BAU': '#A9A9A9'})
    
    fig_2.add_vline(x=2019, line_width=3, line_dash="dash", line_color="green")


    return fig_1, fig_2, None


# @app.callback(
#     Output("results-graph-1", "figure"),
#     Output("results-graph-2", "figure"),
#     Output("loading-scenario", "children"),
#     [
#         Input("local-store", "data"),
#         Input("btn-run", "n_clicks"),
#         Input("results-local-store", "data"),
#     ],
# )
# def run_scenario(data, n_clicks, results_data):
#     print(results_data.keys())
#     print(results_data['scenario_one'].keys())
#     print(pd.read_json(results_data['scenario_one']['EW1']))
#     data = data.copy()

#     changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
#     if 'btn-run' in changed_id:
#         scenarios_results['scenario_one'] = scenario(
#             WP_rate=data['WP_1'], WRR_rate=data['WRR_1'])
#         scenarios_results['scenario_two'] = scenario(
#             WP_rate=data['WP_2'], WRR_rate=data['WRR_2'])

#         df_1 = make_var_df('EW1').reset_index()
#         df_2 = make_var_df('EW2').reset_index()

#         fig_1 = px.line(df_1.query("ISO == 'FRA'"),
#                         x='Year', y='EW1', color='scenario', color_discrete_map={'scenario_one': '#D8A488', 'scenario_two': '#86BBD8', 'BAU': '#A9A9A9'},)
#         fig_2 = px.line(df_2.query("ISO == 'FRA'"),
#                         x='Year', y='EW2', color='scenario', color_discrete_map={'scenario_one': '#D8A488', 'scenario_two': '#86BBD8', 'BAU': '#A9A9A9'})

#         return fig_1, fig_2, None

#     else:  # https://community.plotly.com/t/how-to-leave-callback-output-unchanged/7276/8
#         raise PreventUpdate


def make_var_df(var, scenarios_results=scenarios_results):
    dfs = []
    for scenario, res_dict in scenarios_results.items():
        dfs.append(res_dict[var].to_frame(
            name=var).assign(scenario=scenario))
    return pd.concat(dfs, axis=0)


# Add WP and WRR time series
# Add GDPC for contextqsdqsd 

# Water Requirement Ratio -> Irrigation Water Efficiency !

