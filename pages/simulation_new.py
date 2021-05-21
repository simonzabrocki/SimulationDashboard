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
from pages.scenario_function import run_all_scenarios_water, run_all_scenarios_BE2, run_all_scenarios_GE3


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


def get_args_dict_from_scenario_box(box):
    ided_components = [el for el in box['props']
                       ['children'] if 'id' in el['props']]

    arg_dict = {el['props']['id'][:-4]: el['props']['value'] for el in ided_components}

    return arg_dict


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
                fig_1, fig_2, fig_3 = run_all_scenarios_water(data_dict_expanded, ISO, args_dict_1, args_dict_2)

            if model == 'BE2_model':
                fig_1, fig_2, fig_3 = run_all_scenarios_BE2(GM.demo_script_Hermen.data_dict, ISO, args_dict_1, args_dict_2)
            
            if model == 'GE3_model':
                fig_1, fig_2, fig_3 = run_all_scenarios_GE3(GM.demo_script_Hermen.GE3_data_dict, ISO, args_dict_1, args_dict_2)

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
