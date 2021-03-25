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
                    html.A(
                        html.Button("About GGGI", id="learn-more-button"),
                        href="https://gggi.org/",
                    ),
                ],
                className="row",
            ),
            html.Div(
                [
                    html.Div(
                        [html.H5("Green Growth Index")],
                        className="seven columns main-title",
                    ),
                    html.Div(
                        [
                            dcc.Link(
                                "About the Index",
                                href="https://greengrowthindex.gggi.org/",
                                className="full-view-link",
                            )
                        ],
                        className="five columns",
                    ),
                ],
                className="twelve columns",
                style={"padding-left": "0"},
            ),
        ],
        className="row",
    )
    return header


def get_menu():
    menu = html.Div(
        [
            dcc.Link(
                "Global Overview",
                href="/SimulationDashBoard/global-overview",
                className="tab first",
            ),
            dcc.Link(
                "Regional Outlook",
                href="/SimulationDashBoard/regional-outlouk",
                className="tab",
            ),
            dcc.Link(
                "Country Profile", href="/SimulationDashBoard/country-profile",
                className="tab"
            ),
            dcc.Link(
                "Country Comparison", href="/SimulationDashBoard/country-comparator",
                className="tab"
            ),
            dcc.Link(
                "Data", href="/SimulationDashBoard/data",
                className="tab"
            ),
            dcc.Link(
                "Models Overview",
                href="/SimulationDashBoard/models",
                className="tab",
            ),
            dcc.Link(
                "Simulation",
                href="/SimulationDashBoard/simulation",
                className="tab",
            ),
        ],
        className="row all-tabs",
    )
    return menu

# def get_menu():
#     menu = html.Div(
#         [
#             dbc.Nav(
#                 [
#                     dbc.DropdownMenu(
#                         [dbc.DropdownMenuItem("Global Overview", href="/SimulationDashBoard/global-overview"),
#                          dbc.DropdownMenuItem("Regional Outlook", href="/SimulationDashBoard/regional-outlouk"),
#                          dbc.DropdownMenuItem("Country Profile", href="/SimulationDashBoard/country-comparator"),
#                          dbc.DropdownMenuItem("Country Comparator", href="/SimulationDashBoard/country-profile"),
#                          dbc.DropdownMenuItem("Data", href="/SimulationDashBoard/data"), ],
#                         label="Green Growth Index",
#                         nav=True,
#                     ),
#                     dbc.DropdownMenu(
#                         [dbc.DropdownMenuItem("Model Overview", href="/SimulationDashBoard/models")],
#                         label="Simulation Tool",
#                         nav=True,
#                     ),
#                 ]
#             ),
#         ],
#         className="row all-tabs",
#     )
#     return menu
