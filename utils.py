import dash
import dash_html_components as html
import dash_core_components as dcc
import pandas as pd
from dash.dependencies import Input, Output


def format_data(data):
    data = data.copy()
    variable_names = {
        'ESRU': 'Efficient and sustainable resource use',
        'NCP': 'Natural capital protection',
        'GEO': 'Green economic opportunities',
        'SI': 'Social inclusion',
        'EE': 'Efficient and and sustainable energy',
        'EW': 'Efficient and sustainable water use',
        'SL': 'Sustainable land use',
        'ME': 'Material use efficiency',
        'EQ': 'Environmental quality',
        'GE': 'Greenhouse gas emissions reductions',
        'BE': 'Biodiversity and ecosystem protection',
        'CV': 'Cultural and social value',
        'GV': 'Green investment',
        'GT': 'Green trade',
        'GJ': 'Green employment',
        'GN': 'Green innovation',
        'AB': 'Access to basic services and resources',
        'GB': 'Gender balance',
        'SE': 'Social equity',
        'SP': 'Social protection'
    }
    var_names = pd.DataFrame.from_dict(variable_names, orient='index')
    var_names.columns = ['Variable_name']
    data = data.set_index('Variable')
    data['Variable_name'] = var_names
    data = data.reset_index()

    return data


def Header(app):
    return html.Div([get_header(app), html.Br([]), get_menu()])


def get_header(app):
    header = html.Div(
        [
            html.Div(
            [
                    html.Img(
                        src=app.get_asset_url("GGGI_logo1.png"),
                        className="logo",
                    ),

                    html.Div([
                        html.Ul([
                                html.Li([html.A("Home", href="https://greengrowthindex.gggi.org/",),]),
                                html.Li([html.Span(),]), 
                                html.Li([html.A("Index and Simulation", href="localhost:8080",),]),
                                html.Li([html.Span(),]),
                                html.Li([html.A("Publications", href="https://greengrowthindex.gggi.org/?page_id=3126",),]),
                                html.Li([html.Span(),]),    
                                html.Li([html.A("Authors", href="https://greengrowthindex.gggi.org/?page_id=3080",),]),
                                html.Li([html.Span(),]),
                                html.Li([html.A("Reviewers", href="https://greengrowthindex.gggi.org/?page_id=1975",),]),
                                html.Li([html.Span(),]),    
                                html.Li([html.A("Partners", href="https://greengrowthindex.gggi.org/?page_id=2166",),]),
                                html.Li([html.Span(),]),                                                                                                            
                                html.Li([html.A("Contact Us", href="https://greengrowthindex.gggi.org/?page_id=2839",),]),
                            ]),
                    ],className="mainnav"),

            ],
            className="mainheader",
            ),
               
    ],
    className="mainheader",
    )
    return header


def get_menu():
     

    menu = html.Div(
        [
           #html.Div([
           #        html.Div([
           #                
           #                html.Div([                               
           #                      dcc.Link(html.Button('Global Green Index', id='btn-nclicks-1', n_clicks_timestamp=1), href="/SimulationDashBoard/global_overview"),
           #                     ], className="tab",),
           #                html.Div([
           #                      dcc.Link(html.Button('Simulation Tool', id='btn-nclicks-2', n_clicks_timestamp=2), href="/SimulationDashBoard/simulation"),
           #                     ], className="tab",),
           #                html.Div([
           #                      dcc.Link(html.Button('Evidence Library', id='btn-nclicks-3', n_clicks_timestamp=3), href="/SimulationDashBoard/models"),
           #                     ], className="tab",), 
           #        
           #        ],
           #        className="row all-tabs",),
           #],className="rowtabs",),
        ])
    return menu





