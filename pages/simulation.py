import dash_html_components as html
import dash_core_components as dcc
from app import app, ISO_options
from dash.dependencies import Input, Output
from utils import Header, is_btn_clicked
from dash.exceptions import PreventUpdate
from ggmodel_dev.utils import get_data_dict_from_folder, get_data_dict_from_folder_parquet

from pages.scenario_box import (GE3_scenario_box,
                                BE2_scenario_box,
                                water_scenario_box,
                                VEHC_scenario_box,
                                ELEC_scenario_box,
                                RECYCLE_scenario_box,
                                )

from pages.scenario_function import (run_all_scenarios_VEHC,
                                     run_all_scenarios_EW,
                                     run_all_scenarios_BE2,
                                     run_all_scenarios_GE3,
                                     run_all_scenarios_ELEC,
                                     run_all_scenarios_RECYCLE,
                                     )


scenario_properties = {
    'Scenario_one': {"name": 'Scenario 1'},
    'Scenario_two': {'name': 'Scenario 2'},
    'BAU': {'name': 'Business as Usual'},
}

scenario_box_dictionnary = {
    'EW_models': water_scenario_box,
    'BE2_model': BE2_scenario_box,
    'GE3_model': GE3_scenario_box,
    'VEHC_model': VEHC_scenario_box,
    'ELEC_model': ELEC_scenario_box,
    'RECYCLE_model': RECYCLE_scenario_box,
}

scenario_data_dictionnary = {
    'EW_models': get_data_dict_from_folder('data/sim/EW'),
    'BE2_model': get_data_dict_from_folder('data/sim/BE2'),
    'GE3_model': get_data_dict_from_folder_parquet('data/sim/GE3'),
    'VEHC_model': get_data_dict_from_folder('data/sim/VEHC'),
    'ELEC_model': get_data_dict_from_folder('data/sim/ELEC'),
    'RECYCLE_model': get_data_dict_from_folder('data/sim/RECYCLE'),

}

scenario_function_dictionnary = {
    'EW_models': run_all_scenarios_EW,
    'BE2_model': run_all_scenarios_BE2,
    'GE3_model': run_all_scenarios_GE3,
    'VEHC_model': run_all_scenarios_VEHC,
    'ELEC_model': run_all_scenarios_ELEC,
    'RECYCLE_model': run_all_scenarios_RECYCLE,

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
                            {'label': 'Efficient Water Model (Water)',
                             'value': 'EW_models'},
                            {'label': 'Land Use Model (Landuse)',
                             'value': 'BE2_model'},
                            {'label': 'Electric Power Plants Model (Energy)', 'value': 'ELEC_model'},
                            {'label': 'Agricultural Emissions Model (Landuse)', 'value': 'GE3_model'},
                            {'label': 'Vehicle Ownership rate Model (Transport)', 'value': 'VEHC_model'},
                            {'label': 'Recycled material Model (Material)', 'value': 'RECYCLE_model'}

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
                    html.Button('Download (beta)', id='btn-download', n_clicks=0,
                                style={'font-size': 15,
                                       'font-weight': 'normal',
                                       'color': '#ffffff',
                                       'background': '#D3D3D3',
                                       'border': '#D3D3D3',
                                       }),
                    dcc.Download(id="download-xls"),

                ],
                className='row'
            ),
        ],
        className='row'
    )

    return layout


def extract_values_from_ided_component(component):
    '''Dangerous way to filter out the index'''
    return {component['props']['id'][:-4]: component['props']['value']}


def get_args_dict_from_scenario_box(box):
    '''TO DO: Recursive search of the id'''
    ided_components = [el for el in box['props']
                       ['children'] if 'id' in el['props']]

    arg_dict = {}
    for component in ided_components:
        if 'value' in component['props']:
            arg_dict.update(extract_values_from_ided_component(component))
        else:
            unested_comp = []
            # to make recursive, not sustainable as is
            for comp_1 in component['props']['children']:
                for comp_2 in comp_1['props']['children']:
                    for comp_3 in comp_2['props']['children']:
                        if 'id' in comp_3['props']:
                            unested_comp.append(comp_3)

            for el in unested_comp:
                arg_dict.update(extract_values_from_ided_component(el))

    return arg_dict

def get_sim_tab():
    return html.Div(
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
            )

layout = html.Div(
    [
        html.Div([Header(app, 'Simulation')]),
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
                html.Div([get_sim_tab()], id='sim-spatial-tabs-content', className='pretty_container eight columns'),
            ],
            className='row'
        ),
    ],
    className="page",
)




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


def get_spatial_tab():
    return html.Div([
        html.Div([html.H3('Not available')], className='product_A', style={'background': '#D3D3D3'}),
        html.Div([dcc.Graph(id='map', config={'displayModeBar': False}),], className='row')
        ]
    )


@app.callback(Output('sim-spatial-tabs-content', 'children'),
              Input('sim-spatial-tabs', 'value'))
def render_tab(tab):
    if tab == 'sim':
        return get_sim_tab()
    elif tab == 'spatial':
        return get_spatial_tab()


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
    ],
    prevent_initial_call=True,
)
def run_scenario(box_1, box_2, ISO, model, n_clicks):
    if is_btn_clicked('btn-run'):
        args_dict_1 = get_args_dict_from_scenario_box(box_1)
        args_dict_2 = get_args_dict_from_scenario_box(box_2)

        #print(round(time.time()*100))

        try:
            scenario_function = scenario_function_dictionnary[model]
            data = scenario_data_dictionnary[model]
            fig_1, fig_2, fig_3, scenarios_results = scenario_function(
                data, ISO, args_dict_1, args_dict_2)

        except Exception as e:
            print(e)
            return {}, {}, {}, None

        return fig_1, fig_2, None

    else:  # https://community.plotly.com/t/how-to-leave-callback-output-unchanged/7276/8
        raise PreventUpdate


# @app.callback(
#     Output("download-xls", "data"),
#     [
#         Input('scenario_box_1', 'children'),
#         Input('scenario_box_2', 'children'),
#         Input('ISO_run_results', 'value'),
#         Input('dropdown-simulation-model', 'value'),
#         Input("btn-download", "n_clicks"),
#     ],
#     prevent_initial_call=True,
# )
# def downdload_table(box_1, box_2, ISO, model, n_clicks):
#     if is_btn_clicked('btn-download'):
#         args_dict_1 = get_args_dict_from_scenario_box(box_1)
#         args_dict_2 = get_args_dict_from_scenario_box(box_2)

#         t = round(time.time()*100)

#         #return dcc.send_file(f'outputs/simulation_results.xlsx')

#         try:
#             scenario_function = scenario_function_dictionnary[model]
#             data = scenario_data_dictionnary[model]
#             fig_1, fig_2, fig_3, scenarios_results = scenario_function(
#                 data, ISO, args_dict_1, args_dict_2)


#         except Exception as e:
#             print(e)
#             return {}, {}, {}, None

#     else: 
#         raise PreventUpdate