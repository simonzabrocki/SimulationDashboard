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

from pages.scenario_box import GE3_scenario_box, BE2_scenario_box, water_scenario_box


scenario_properties = {
    'Scenario_one': {"name": 'Scenario 1'},
    'Scenario_two': {'name': 'Scenario 2'},
    'BAU': {'name': 'Business as Usual'},
}

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

scenario_function_dictionnary = {
    'EW_models': run_EW_scenario,
    'BE2_model': GM.demo_script_Hermen.run_BE2_scenario,
    'GE3_model': GM.demo_script_Hermen.run_GE3_scenario,
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

                d_1 , c_1 = format_data_dict_sankey({k: v for k, v in scenarios_results['scenario_one'].items() if k in ['TEE_CO2eq', 'TMA_CO2eq', 'TMT_CO2eq', 'TMP_CO2eq']})
                d_2 , c_2 = format_data_dict_sankey({k: v for k, v in scenarios_results['scenario_two'].items() if k in ['TEE_CO2eq', 'TMA_CO2eq', 'TMT_CO2eq', 'TMP_CO2eq']})
                d_3 , c_3 = format_data_dict_sankey({k: v for k, v in scenarios_results['BAU'].items() if k in ['TEE_CO2eq', 'TMA_CO2eq', 'TMT_CO2eq', 'TMP_CO2eq']})
                

                fig_1 = plot_sanky_GE3(d_1, c_1).update_layout(title='Scenario 1')
                fig_2 = plot_sanky_GE3(d_2, c_2).update_layout(title='Scenario 2')
                fig_3 = plot_sanky_GE3(d_3, c_3).update_layout(title='Business as Usual')

        except Exception as e:
            print(e)
            return {}, {}, {}, None
       
        return fig_1, fig_2, None
   

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
