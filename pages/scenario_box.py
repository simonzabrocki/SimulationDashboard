import dash_html_components as html
import dash_core_components as dcc
from dash_html_components.Div import Div

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


def TAi_sliders(scenario_id):
    Items = ['Asses', 'Cattle, dairy', 'Cattle, non_dairy',
             'Chickens, broilers', 'Chickens, layers', 'Ducks', 'Goats',
             'Horses', 'Mules', 'Sheep', 'Swine, breeding', 'Swine, market',
             'Turkeys']

    return html.Div([
        html.Div([
            TAi_item_slider(Items[0], scenario_id=scenario_id, mark=True),
            TAi_item_slider(Items[1], scenario_id=scenario_id, mark=False),
            TAi_item_slider(Items[2], scenario_id=scenario_id, mark=False),
            TAi_item_slider(Items[3], scenario_id=scenario_id, mark=False),
        ], className='bare_container four columns'),
        html.Div([
            TAi_item_slider(Items[4], scenario_id=scenario_id, mark=True),
            TAi_item_slider(Items[5], scenario_id=scenario_id, mark=False),
            TAi_item_slider(Items[6], scenario_id=scenario_id, mark=False),
            TAi_item_slider(Items[7], scenario_id=scenario_id, mark=False),
        ], className='bare_container four columns'),
        html.Div([
            TAi_item_slider(Items[9], scenario_id=scenario_id, mark=True),
            TAi_item_slider(Items[9], scenario_id=scenario_id, mark=False),
            TAi_item_slider(Items[10], scenario_id=scenario_id, mark=False),
            TAi_item_slider(Items[11], scenario_id=scenario_id, mark=False),
        ], className='bare_container four columns'),
        

    ], id=f'TAi_pct{scenario_id}',)


def TAi_item_slider(item, scenario_id, mark=False):
    slider_name = f"TAi_pct_{'_'.join(item.split(', '))}"
    marks = {}
    if mark:
        marks = {
            0: {'label': 'x0', 'style': {'color': 'white'}},
            1: {'label': 'x1', 'style': {'color': 'white'}},
            2: {'label': 'x2', 'style': {'color': 'white'}},
        }

    layout = html.Div([
        html.P(f'{item}', style={'font-size': 10}),
        dcc.Slider(
            id=f'{slider_name}{scenario_id}',
            step=0.1,
            value=1,
            min=0,  # To update later
            max=2,
            marks=marks,
            included=False,
        ),

    ], className='row')
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
            html.Br([]),
            html.P('Animal population target', style={'font-size': 17}),
            TAi_sliders(scenario_id),
        ],
        className='row')

    return layout


def VEHC_scenario_box(scenario_id='_one'):

    Scenario_name = scenario_properties[f'Scenario{scenario_id}']['name']

    layout = html.Div(

        [
            html.H5(Scenario_name),
            html.Br([]),
            html.P('Vehicle per Capita Saturation Level by 2050',
                   style={'font-size': 17}),
            dcc.Slider(
                id=f'MAX_sat{scenario_id}',
                step=50,
                value=550,
                min=300,  # To update later
                max=800,
                marks={
                    300: {'label': '300', 'style': {'color': 'white'}},
                    550: {'label': '550', 'style': {'color': 'white'}},
                    800: {'label': '800', 'style': {'color': 'white'}},
                },
                included=False,
            ),
            html.Br([]),
            html.P('GDPC annual growth', style={'font-size': 17}),
            dcc.Slider(
                id=f'GDPC_rate{scenario_id}',
                step=0.05,
                value=1,
                min=0.95,  # To update later
                max=1.1,
                marks={
                    0.95: {'label': '-5%', 'style': {'color': 'white'}},
                    1: {'label': '0%', 'style': {'color': 'white'}},
                    1.05: {'label': '5%', 'style': {'color': 'white'}},
                    1.1: {'label': '10%', 'style': {'color': 'white'}},
                },
                included=False,
            ),
        ],
        className='row')

    return layout
