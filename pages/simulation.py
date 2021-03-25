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

import time


scenario_properties = {
    'Scenario_one': {"name": 'Scenario 1'},
    'Scenario_two': {'name': 'Scenario 2'},
    'BAU': {'name': 'Business as Usual'},
}

def scenario_box(scenario_id='_one'):
    
    Scenario_name = scenario_properties[f'Scenario{scenario_id}']['name']

    layout = html.Div(

        [
            html.H5(Scenario_name),
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


def model_selection_box():
    layout = html.Div(
        [
            html.H5(
                "Select a Model",
                className="subtitle padded",
            ),
            html.Br([]),
            dcc.Dropdown(id="dropdown-simulation-model",
                         options=[
                             {'label': 'Water Model',
                             'value': 'EW_models'}],
                         value='EW_models')

        ])
    return layout


def scenario_building_box():
    layout = html.Div(
        [
            html.H5(
                "Built a Scenario",
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
            html.H5(
                "Choose a Country",
                className="subtitle padded",
            ),
            html.Br([]),
            html.Div([dcc.Dropdown(id="ISO_run_results",
                                   options=[{'label': country, 'value': iso}
                                            for iso, country in ISO_options],
                                   value='FRA')],
                     style={'width': '100%',
                            'display': 'inline-block',
                            'align-items': 'center',
                            'justify-content': 'center',
                            'font-size': '20px'}
                     ),
            html.Br([]),       
            html.Br([]),
            html.Br([]),
            html.Div(
                [
                    html.Button('Run', id='btn-run', n_clicks=0,
                                style={'font-size': 20,
                                       'font-weight': 'normal',
                                       'color': '#ffffff',
                                       'background': '#14ac9c',
                                       'border': '#14ac9c',
                                       }),
                    dcc.Loading(
                        id="loading-scenario",
                        children=html.Div(id='loading-output'),
                        color='#14ac9c',
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
        html.Div([Header(app)]),
        html.Div(
            [
                model_selection_box(),
                html.Br([]),
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
    Output("results-graph-1", "figure"),
    Output("results-graph-2", "figure"),
    Output('context-graph-1', 'figure'),
    Output("loading-output", "children"),
    [
        Input("WRR-slider_one", "value"),
        Input("WP-slider_one", "value"),
        Input("WRR-slider_two", "value"),
        Input("WP-slider_two", "value"),
        Input('ISO_run_results', 'value'),
        Input("btn-run", "n_clicks"),
    ],
)
def run_scenario(WRR_1, WP_1, WRR_2, WP_2, ISO, n_clicks):
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    if 'btn-run' in changed_id:

        try:
            scenarios_results = {}

            data_dict = {key: value.loc[[ISO]]
                        for key, value in data_dict_expanded.items()}


            scenarios_results['BAU'] = run_EW_scenario(data_dict)

            scenarios_results['scenario_one'] = run_EW_scenario(data_dict_expanded=data_dict,
                                                                WP_rate=WP_1, WRR_rate=WRR_1)

            scenarios_results['scenario_two'] = run_EW_scenario(data_dict_expanded=data_dict,
                                                                WP_rate=WP_2, WRR_rate=WRR_2)



            df_1 = format_var_results(scenarios_results, 'EW1')
            df_2 = format_var_results(scenarios_results, 'EW2')
            df_3 = format_var_results(scenarios_results, 'GDPC')

            fig_1 = scenario_line_plot('EW1', df_1, ISO)
            fig_2 = scenario_line_plot('EW2', df_2, ISO)
            fig_3 = scenario_line_plot('GDPC', df_3, ISO)
        
        except Exception as e:
            return {}, {}, {}, None

        return fig_1, fig_2, fig_3, None

    else:  # https://community.plotly.com/t/how-to-leave-callback-output-unchanged/7276/8
        raise PreventUpdate


def format_var_results(scenarios_results, var):
    df = pd.concat([
        scenarios_results['scenario_one'][var].reset_index().assign(scenario='Scenario 1'),
        scenarios_results['scenario_two'][var].reset_index().assign(scenario='Scenario 2'),
        scenarios_results['BAU'][var].reset_index().assign(scenario='BAU'),
        ], axis=0).rename(columns={0: var})

    return df


def scenario_line_plot(var, df, ISO):  # ugly af
    fig = px.line(df.query(f"ISO == '{ISO}' and Year >= 2000"),
                  x='Year',
                  y=var,
                  color='scenario',
                  color_discrete_map={'Scenario 1': '#D8A488',
                                      'Scenario 2': '#86BBD8',
                                      'BAU': '#A9A9A9'},
                  )

    fig.add_vline(x=2019, line_width=3, line_dash="dash", line_color="green")
    fig.update_layout(hovermode="x")
    fig.update_layout(legend_title_text='Scenario')
    return fig