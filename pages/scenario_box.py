import dash_html_components as html
import dash_core_components as dcc

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
                id=f'WP_rate{scenario_id}',
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
                id=f'WRR_rate{scenario_id}',
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
                id=f'FLOi_target{scenario_id}',
                step=None,
                value=1,
                min=0.5,  # To update later
                max=1.5,
                marks={
                    0.5: {'label': '-50%', 'style': {'color': 'white'}},
                    0.75: {'label': '-25%', 'style': {'color': 'white'}},
                    1: {'label': '+0%', 'style': {'color': 'white'}},
                    1.25: {'label': '+25%', 'style': {'color': 'white'}},
                    1.5: {'label': '+50%', 'style': {'color': 'white'}}
                },
                included=False,
            ),
            html.Br([]),
            html.P('Food demand 2050 target',
                   style={'font-size': 17}),
            dcc.Slider(
                id=f'FDKGi_target{scenario_id}',
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
                id=f'CYi_target{scenario_id}',
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
                id=f'R_rate{scenario_id}',
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
                id=f'MM_Ti{scenario_id}',
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
                id=f'MM_ASi{scenario_id}',
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

