import dash
import dash_html_components as html
import dash_core_components as dcc
import pandas as pd


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


def Header(app, active_tab='Global Overview'):
    return html.Div([get_header(app), html.Br([]), get_menu(active_tab)])


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


def get_menu(active_tab):

    tabs_links = {
        'Global Overview': "/SimulationDashBoard/global-overview",
        'Regional Outlook': "/SimulationDashBoard/regional-outlouk",
        'Country Profile': "/SimulationDashBoard/country-profile",
        'Country Comparison': "/SimulationDashBoard/country-comparator",
        'Data': "/SimulationDashBoard/data",
        'Models Overview': "/SimulationDashBoard/models",
        'Simulation': "/SimulationDashBoard/simulation"
    }

    menu_list = []

    for name, link in tabs_links.items():
        if name == active_tab:
            tab = dcc.Link(
                name,
                href=link,
                className="tab",
                style={'color': '#2db29b'}
            )
        else:
            tab = dcc.Link(
                name,
                href=link,
                className="tab",
            )
        menu_list.append(tab)

    menu = html.Div(menu_list, className="row all-tabs")
    return menu


def is_btn_clicked(btn_id):
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    return btn_id in changed_id
