import dash_html_components as html
import dash_core_components as dcc
from app import app, ISO_options
from dash.dependencies import Input, Output
from utils import Header, is_btn_clicked
from dash.exceptions import PreventUpdate

from pages.scenario_box import (GE3_scenario_box,
                                BE2_scenario_box,
                                water_scenario_box,
                                VEHC_scenario_box,
                                )

from pages.scenario_function import (run_all_scenarios_VEHC, run_all_scenarios_water,
                                     run_all_scenarios_BE2,
                                     run_all_scenarios_GE3,
                                     get_data_dict_from_folder,
                                     get_data_dict_from_folder_parquet
                                     )


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
                            {'label': 'Vehicle Ownership rate Model', 'value': 'VEHC_model'}
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
    '''TO DO: Recursive search of the id'''
    ided_components = [el for el in box['props']
                       ['children'] if 'id' in el['props']]

    arg_dict = {el['props']['id'][:-4]: el['props']['value'] for el in ided_components if 'value' in el['props']}

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
    'VEHC_model': VEHC_scenario_box,
}

scenario_data_dictionnary = {
    'EW_models': get_data_dict_from_folder('data/sim/EW'),
    'BE2_model': get_data_dict_from_folder('data/sim/BE2'),
    'GE3_model': get_data_dict_from_folder_parquet('data/sim/GE3'),
    'VEHC_model': get_data_dict_from_folder('data/sim/VEHC'),
}

scenario_function_dictionnary = {
    'EW_models': run_all_scenarios_water,
    'BE2_model': run_all_scenarios_BE2,
    'GE3_model': run_all_scenarios_GE3,
    'VEHC_model': run_all_scenarios_VEHC,
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
    if is_btn_clicked('btn-run'):
        args_dict_1 = get_args_dict_from_scenario_box(box_1)
        args_dict_2 = get_args_dict_from_scenario_box(box_2)
        print(args_dict_1)

        try:
            scenario_function = scenario_function_dictionnary[model]
            data = scenario_data_dictionnary[model]
            fig_1, fig_2, fig_3 = scenario_function(
                data, ISO, args_dict_1, args_dict_2)

        except Exception as e:
            print(e)
            return {}, {}, {}, None

        return fig_1, fig_2, None

    else:  # https://community.plotly.com/t/how-to-leave-callback-output-unchanged/7276/8
        raise PreventUpdate
