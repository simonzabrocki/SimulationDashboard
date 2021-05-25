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
                        src=app.get_asset_url("GGGI_logo.png"),
                        className="logo",
                    ),
                    html.Div([
                        html.Ul([
                            html.Li(
                                [html.A("Home", href="https://greengrowthindex.gggi.org/",), ]),
                            html.Li([html.Span(), ]),
                            html.Li(
                                [html.A("Index and Simulation", href="localhost:8080",), ]),
                            html.Li([html.Span(), ]),
                            html.Li(
                                [html.A("Publications", href="https://greengrowthindex.gggi.org/?page_id=3126",), ]),
                            html.Li([html.Span(), ]),
                            html.Li(
                                [html.A("Authors", href="https://greengrowthindex.gggi.org/?page_id=3080",), ]),
                            html.Li([html.Span(), ]),
                            html.Li(
                                [html.A("Reviewers", href="https://greengrowthindex.gggi.org/?page_id=1975",), ]),
                            html.Li([html.Span(), ]),
                            html.Li(
                                [html.A("Partners", href="https://greengrowthindex.gggi.org/?page_id=2166",), ]),
                            html.Li([html.Span(), ]),
                            html.Li(
                                [html.A("Contact Us", href="https://greengrowthindex.gggi.org/?page_id=2839",), ]),
                        ]),
                    ], className="mainnav"),

                ],
                className="mainheader",
            ),

        ],
        className="mainheader",
    )
    return header


def get_menu():

    menu = html.Div([
                html.Div([
                    html.Div([], className="titlespace",),
                    html.Div([html.P("Green Growth Index", id="pagetitle"), html.P("Global Overview", id="pagetitlechild"), ], className="titlemain",),
                    ], className="titlediv",),
                html.Div([
                    html.Div([
                        html.Div([
                            dcc.Link(html.Button('Green Growth Index',
                                                style={'text-decoration': 'none', 'color': '#14ac9c'}),
                                    href="/SimulationDashBoard/global_overview"),
                                    ], className="tab",),
                        html.Div([
                            dcc.Link(html.Button('Simulation Tool'),
                                href="/SimulationDashBoard/simulation"),
                                ], className="tab",),
                        html.Div([
                            dcc.Link(html.Button('Evidence Library'),
                                href="/SimulationDashBoard/models"),
                                ], className="tab",),
                    ],
                    className="row all-tabs",),
                html.Div(className="separation"),
                ], className="rowtabs",)
    ])

    return menu


def gg_index_menu(active_tab):


    name_link_list = [
        {'label': 'Global Overview', 'value':'/SimulationDashBoard/global_overview'},
        {'label': 'Regional Outlook', 'value':'/SimulationDashBoard/regional-outlouk'},
        {'label': 'Country Profile', 'value':'/SimulationDashBoard/country-profile'},
        {'label': 'Dashboard', 'value':'/SimulationDashBoard/models'},

        ]

    return get_box_menu(name_link_list, active_tab)


def evidence_lib_menu(active_tab):
    name_link_list = [
    {'label': 'Model Description', 'value':'/SimulationDashBoard/models'},
    {'label': 'Model Assumptions', 'value':'/SimulationDashBoard/models'},
    {'label': 'Python Codes', 'value':'/SimulationDashBoard/models'},
    {'label': 'Data', 'value':'/SimulationDashBoard/data'},
    ]
    return get_box_menu(name_link_list, active_tab)



def get_box_menu(name_link_list, active_tab):
    div_list = []

    for name_link in name_link_list:
        name = name_link['label']
        link = name_link['value']

        if name == active_tab:
            div = html.Div([dcc.Link(html.Button(name, style={'background-color':'#14ac9c' , 'color': 'white'}), href=link)], className="thirdtabs",)

        else:
            div = html.Div([dcc.Link(html.Button(name), href=link)], className="thirdtabs")

        div_list.append(div)    

    return  html.Div(div_list, className="thirdtabmain")