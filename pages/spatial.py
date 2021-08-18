import dash_html_components as html
import dash
import dash_core_components as dcc
from app import app, ISO_options
from dash.dependencies import Input, Output
from utils import Header, is_btn_clicked
from dash.exceptions import PreventUpdate
import pandas as pd
import plotly.express as px



power_plant_df = pd.read_csv('data/spatial/power_plant_data.csv')

def model_selection_box():
    layout = html.Div(
        [
            html.H5(
                "Select a Model",
                className="subtitle padded",
            ),
            html.Br([]),
            dcc.Dropdown(id="dropdown-map-simulation-model",
                         options=[
                            {'label': 'Electric plant cooling water withdrawal ',
                             'value': 'EW_models'},
                         ],
                         value='EW_models'
                         )

        ])
    return layout


def scenario_building_box():
    layout = html.Div(
        [
            html.H5(
                "Choose a Scenario",
                className="subtitle padded",
            ),
            html.Br([]),
            html.Div([html.H5('Scenario 1'), html.H6('Not available')],
                     id="map_scenario_box_1",
                     className='product_A'
                     ),
            html.Div([html.H5('Scenario 2'), html.H6('Not available')],
                     id="map_scenario_box_2",
                     className='product_B'
                     ),
            html.H5(
                "Choose a Country",
                className="subtitle padded",
            ),
            html.Br([]),
            html.Div([dcc.Dropdown(id="ISO_map_run_results",
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
                    html.Button('Run', id='map-btn-run', n_clicks=0,
                                disabled=True,
                                style={'font-size': 20,
                                       'font-weight': 'normal',
                                       'color': '#ffffff',
                                       'background': '#808080',
                                       'border': '#808080',
                                       }),
                    dcc.Loading(
                        id="map-loading-scenario",
                        children=html.Div(id='map-loading-output'),
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


def density_map(df):
    #plot_df = power_plant_df.query(f"ISO in ['{ISO}']")

    fig = px.density_mapbox(df.dropna(subset=['Water_Withdrawal']),
                        lat='latitude',
                        lon='longitude',
                        z='Water_Withdrawal',
                        hover_data={'Name':True, 'Capacity':True, 'latitude': False, 'longitude': False, 'Fuel': True},
                        width=1200,
                        height=800,
                        radius=20,
                        zoom=4,
                        ).update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0},
                                        geo=dict(showframe=False,
                                                resolution=50,
                                                showcoastlines=False,
                                                visible=True,
                                                fitbounds="locations",
                                                showcountries=True
                                                ),
                                        legend=dict(orientation="h"),
                                        mapbox_style="carto-positron", 
                                        )
    return fig


def capa_ww_plot(df):
    fig = px.bar(df.groupby('Fuel')[['Capacity', 'Water_Withdrawal']].sum().reset_index().melt(id_vars=['Fuel']),
                 x='Fuel',
                 y='value',
                 color='Fuel',
                 facet_col='variable',
                 facet_col_spacing=0.05,
                 width=1200,
                 height=500,
                 #color_discrete_map=FUEL_COLORMAP,
                 ).update_yaxes(matches=None, showticklabels=True, )

    return fig



def capacity_plot(df):
    capa_plot = px.pie(df.assign(Unit="MW"), names='Fuel', values='Capacity', color='Fuel',
                   hole=0.5)
    return capa_plot


def ww_plot(df):
    ww_plot = px.pie(df.assign(Unit="m3/year").dropna(subset=['Water_Withdrawal']),
                 names='Fuel',
                 values='Water_Withdrawal',
                 color='Fuel',
                 hole=0.5)
    return ww_plot

layout = html.Div(
    [
        html.Div([Header(app, 'Spatial Analysis')]),
        html.Div([html.H4('This page is still under active development. Scenario building is currently unavaible, only existing data exploration is possible')], className='product_A', style={'background': '#FA8072'}),
        html.Div(
            [
                model_selection_box(),
                html.Br([]),
                scenario_building_box()
            ],
            className="pretty_container four columns",
        ),
        html.Div([
            html.Div([
                html.H6([f"Water Withdrawal Heatmap"], className="subtitle padded"),
                dcc.Graph(id='density_map', config={'displayModeBar': False}),
                html.Div([
                    html.Div([
                         html.H6([f"Capacity and Water Withdrawal distributions"], className="subtitle padded"),
                         dcc.Graph(id='capa_ww_plot', config={'displayModeBar': False}),
                    ],
                    className='twelve columns'),
                    # html.Div([
                    #     html.H6([f"Capacity distribution"], className="subtitle padded"),
                    #     dcc.Graph(id='capa_plot', config={'displayModeBar': False}),
                    # ],
                    # className='six columns'),
                    # html.Div([
                    #     html.H6([f"Water Withdrawal distribution"], className="subtitle padded"),
                    #     dcc.Graph(id='ww_plot', config={'displayModeBar': False}),
                    # ],
                    # className='six columns'),
            ], className='row'),
                
            
            ],
            className='pretty_container eight columns'),
            
            
        ])

    ],
    className="page",
)


@app.callback(
    dash.dependencies.Output('density_map', 'figure'),
    dash.dependencies.Output('capa_ww_plot', 'figure'),
    # dash.dependencies.Output('capa_plot', 'figure'),
    # dash.dependencies.Output('ww_plot', 'figure'),
    [dash.dependencies.Input('ISO_map_run_results', 'value')])
def update_density_map(ISO):
    plot_df = power_plant_df.query(f"ISO in ['{ISO}']")
    return density_map(plot_df), capa_ww_plot(plot_df)#capacity_plot(plot_df), ww_plot(plot_df)
