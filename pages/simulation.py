import dash_html_components as html
import dash_core_components as dcc
import pandas as pd
import dash
from app import app, ISO_options
from dash.dependencies import Input, Output
from utils import Header
import plotly.express as px
from GM.demo_script import run_EW_scenario, data_dict_expanded
import GM.demo_script_Hermen
from GM.demo_script_Hermen import format_data_dict_sankey, plot_sanky_GE3
from dash.exceptions import PreventUpdate
import time
import plotly.graph_objects as go
from plotly.subplots import make_subplots


scenario_properties = {
    'Scenario_one': {"name": 'Scenario 1'},
    'Scenario_two': {'name': 'Scenario 2'},
    'BAU': {'name': 'Business as Usual'},
}


def water_scenario_box(scenario_id='_one'):
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


def BE2_scenario_box(scenario_id='_one'):

    Scenario_name = scenario_properties[f'Scenario{scenario_id}']['name']

    layout = html.Div(

        [
            html.H5(Scenario_name),
            html.Br([]),
            html.P('Food losses 2050 target', style={'font-size': 17}),
            dcc.Slider(
                id=f'FLOi-slider{scenario_id}',
                step=None,
                value=1,
                min=0.5,  # To update later
                max=1.5,
                marks={
                    0.5: {'label': '-50%', 'style': {'color': 'white'}},
                    0.75: {'label': '-25%', 'style': {'color': 'white'}},
                    1: {'label': '+0%', 'style': {'color': 'white'}},
                    1.25: {'label': '+25%', 'style': {'color': 'white'}},
                    1.5: {'label': '+50%', 'style': {'color': 'white'}},

                },
                included=False,
            ),
            html.Br([]),
            html.P('Food demand 2050 target',
                   style={'font-size': 17}),
            dcc.Slider(
                id=f'FDKGi-slider{scenario_id}',
                step=None,
                value=1,
                min=0.5,  # To update later
                max=1.5,
                marks={
                    0.5: {'label': '-50%', 'style': {'color': 'white'}},
                    0.75: {'label': '-25%', 'style': {'color': 'white'}},
                    1: {'label': '+0%', 'style': {'color': 'white'}},
                    1.25: {'label': '+25%', 'style': {'color': 'white'}},
                    1.5: {'label': '+50%', 'style': {'color': 'white'}},

                },
                included=False,
            ),
            html.Br([]),
            html.P('Crop yields 2050 targets',
                   style={'font-size': 17}),
            dcc.Slider(
                id=f'CYi-slider{scenario_id}',
                step=None,
                value=1,
                min=1,
                max=1.1,
                marks={
                    1: {'label': '+0%', 'style': {'color': 'white'}},
                    1.05: {'label': '+5%', 'style': {'color': 'white'}},
                    1.1: {'label': '+10%', 'style': {'color': 'white'}},
                },
                included=False,
            ),
            html.Br([]),
            html.P('Reforestation annual rate',
                   style={'font-size': 17}),
            dcc.Slider(
                id=f'R_rate-slider{scenario_id}',
                step=None,
                value=0,
                min=0,  # To update with proper values later
                max=100,
                marks={
                    0: {'label': '0%', 'style': {'color': 'white'}},
                    25: {'label': '25%', 'style': {'color': 'white'}},
                    50: {'label': '50%', 'style': {'color': 'white'}},
                    100: {'label': '100%', 'style': {'color': 'white'}},
                },
                included=False,
            ),
        ],
        className='row')

    return layout


def GE3_scenario_box(scenario_id='_one'):

    Scenario_name = scenario_properties[f'Scenario{scenario_id}']['name']

    step = 0.1
    layout = html.Div(

        [
            html.H5(Scenario_name),
            html.Br([]),
            html.P('% Manure treated', style={'font-size': 17}),
            dcc.Slider(
                id=f'MM_Ti-slider{scenario_id}',
                step=step,
                value=1/2,
                min=0,  # To update later
                max=1,
                marks={
                    0: {'label': '0%', 'style': {'color': 'white'}},
                    1: {'label': '100%', 'style': {'color': 'white'}},
                },
                included=False,
            ),
            html.Br([]),
            html.P('% Manure applied to soils', style={'font-size': 17}),
            dcc.Slider(
                id=f'MM_ASi-slider{scenario_id}',
                step=step,
                value=1,
                min=0,  # To update later
                max=1,
                marks={
                    0: {'label': '0%', 'style': {'color': 'white'}},
                    1: {'label': '100%', 'style': {'color': 'white'}},
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
                            {'label': 'Efficient Water Model', 'value': 'EW_models'},
                            {'label': 'Land Use Model', 'value': 'BE2_model'},
                            {'label': 'Agricultural Emissions Model', 'value': 'GE3_model'},
                         ],
                         value='EW_models'
                         )

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
            html.Div([],
                     id="scenario_box_1",
                     className='product_A'
                     ),
            html.Div([],
                     id="scenario_box_2",
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


scenario_box_dictionnary = {
    'EW_models': water_scenario_box,
    'BE2_model': BE2_scenario_box,
    'GE3_model': GE3_scenario_box,
}


@app.callback(
    Output('scenario_box_1', 'children'),
    Output('scenario_box_2', 'children'),
    [
        Input('dropdown-simulation-model', 'value'),
    ]
)
def update_scenario_box(model_name):
    scenario_box_function = scenario_box_dictionnary[model_name]
    return scenario_box_function(scenario_id='_one'), scenario_box_function(scenario_id='_two')


component_variable_dictionnary = {
    'WP-slider': 'WP_rate',
    'WRR-slider': 'WRR_rate',
    'FDKGi-slider': 'FDKGi_target',
    'FLOi-slider': 'FLOi_target',
    'CYi-slider': 'CYi_target',
    'R_rate-slider': 'R_rate',
    'MM_Ti-slider': 'MM_Ti',
    'MM_ASi-slider': 'MM_ASi',
}


def get_args_dict_from_scenario_box(box):
    ided_components = [el for el in box['props']
                       ['children'] if 'id' in el['props']]
    arg_dict = {el['props']['id'].rstrip('_one').rstrip('_two'): el['props']['value'] for el in ided_components}

    arg_dict = {component_variable_dictionnary[k]: v for k, v in arg_dict.items()}

    return arg_dict



@app.callback(
    Output("results-graph-1", "figure"),
    Output("results-graph-2", "figure"),
    Output('context-graph-1', 'figure'),
    Output("loading-output", "children"),
    [
        Input('scenario_box_1', 'children'),
        Input('scenario_box_2', 'children'),
        Input('ISO_run_results', 'value'),
        Input('dropdown-simulation-model', 'value'),
        Input("btn-run", "n_clicks"),
    ]
)
def run_scenario(box_1, box_2, ISO, model, n_clicks):
    '''To clean up'''
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    if 'btn-run' in changed_id:

        args_dict_1 = get_args_dict_from_scenario_box(box_1)
        args_dict_2 = get_args_dict_from_scenario_box(box_2)

        try:  # To generalize
            if model == 'EW_models':
                scenarios_results = {}

                data_dict = {key: value.loc[[ISO]] for key, value in data_dict_expanded.items()}

                scenarios_results['BAU'] = run_EW_scenario(data_dict)
                

                scenarios_results['scenario_one'] = run_EW_scenario(data_dict_expanded=data_dict, **args_dict_1)

                scenarios_results['scenario_two'] = run_EW_scenario(data_dict_expanded=data_dict, **args_dict_2)

                df_1 = format_var_results(scenarios_results, 'EW1')
                df_2 = format_var_results(scenarios_results, 'EW2')
                df_3 = format_var_results(scenarios_results, 'GDPC')

                fig_1 = scenario_line_plot('EW1', df_1, ISO)
                fig_2 = scenario_line_plot('EW2', df_2, ISO)
                fig_3 = scenario_line_plot('GDPC', df_3, ISO)

            if model == 'BE2_model':

                scenarios_results = {}

                data_dict = {k: v.loc[ISO, 2018:] for k, v in GM.demo_script_Hermen.data_dict.items() if k not in ['CL_corr_coef']}
                
                
            
                data_dict = GM.demo_script_Hermen.run_BE2_projection(data_dict)
                
                data_dict['CL_corr_coef'] = 1.4
                
                data_dict['R_rate'].loc[:, 2018] = 0
                
                scenarios_results['BAU'] = GM.demo_script_Hermen.run_BE2_scenario(data_dict=data_dict)
                scenarios_results['scenario_one'] = GM.demo_script_Hermen.run_BE2_scenario(data_dict=data_dict, **args_dict_1)
                scenarios_results['scenario_two'] = GM.demo_script_Hermen.run_BE2_scenario(data_dict=data_dict, **args_dict_2)

                df_1 = format_var_results(scenarios_results, 'BE2')
                df_2 = format_var_results(scenarios_results, 'delta_CL')

                fig_1 = scenario_line_plot('BE2', df_1, ISO)
                fig_2 = scenario_line_plot('delta_CL', df_2, ISO)
                fig_3 = {}
            
            if model == 'GE3_model':
                scenarios_results = {}
                data_dict = {k: v.loc[ISO, 2018, :] for k, v in GM.demo_script_Hermen.GE3_data_dict.items()}


                scenarios_results['BAU'] = GM.demo_script_Hermen.run_GE3_scenario(data_dict=data_dict, MM_Ti=data_dict['MM_Ti'],MM_ASi=data_dict['MM_ASi'])
                scenarios_results['scenario_one'] = GM.demo_script_Hermen.run_GE3_scenario(data_dict=data_dict, **args_dict_1)
                scenarios_results['scenario_two'] = GM.demo_script_Hermen.run_GE3_scenario(data_dict=data_dict, **args_dict_2)

                #d_1 , c_1 = format_data_dict_sankey(scenarios_results['scenario_one'])
                d_1 , c_1 = format_data_dict_sankey({k: v for k, v in scenarios_results['scenario_one'].items() if k in ['TEE_CO2eq', 'TMA_CO2eq', 'TMT_CO2eq', 'TMP_CO2eq']})
                d_2 , c_2 = format_data_dict_sankey({k: v for k, v in scenarios_results['scenario_two'].items() if k in ['TEE_CO2eq', 'TMA_CO2eq', 'TMT_CO2eq', 'TMP_CO2eq']})
                d_3 , c_3 = format_data_dict_sankey({k: v for k, v in scenarios_results['BAU'].items() if k in ['TEE_CO2eq', 'TMA_CO2eq', 'TMT_CO2eq', 'TMP_CO2eq']})
                


                # fig_1 = make_subplots(rows=2, cols=1)
                # fig_1.append_trace(plot_sanky_GE3(d_1, c_1)['data'][0], row=1, col=1)
                # fig_1.append_trace(plot_sanky_GE3(d_2, c_2)['data'][0], row=2, col=1)


                fig_1 = plot_sanky_GE3(d_1, c_1).update_layout(title='Scenario 1')
                fig_2 = plot_sanky_GE3(d_2, c_2).update_layout(title='Scenario 2')
                fig_3 = plot_sanky_GE3(d_3, c_3).update_layout(title='Business as Usual')

        except Exception as e:
            print(e)
            return {}, {}, {}, None
       
        return fig_1, fig_2, fig_3, None
   

    else:  # https://community.plotly.com/t/how-to-leave-callback-output-unchanged/7276/8
        raise PreventUpdate


def format_var_results(scenarios_results, var):
    df = pd.concat([
        scenarios_results['scenario_one'][var].reset_index().assign(
            scenario='Scenario 1'),
        scenarios_results['scenario_two'][var].reset_index().assign(
            scenario='Scenario 2'),
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
