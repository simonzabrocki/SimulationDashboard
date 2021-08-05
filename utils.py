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
    top_header = get_header(app)
    menu = get_menu(active_tab)

    page_title = html.Div(
        [
            html.Div([
                page_menu(active_tab)],
                className='pretty_container twelve columns'),
        ],
        className="row")

    return html.Div([top_header, html.Br([]), menu, page_title])


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


def get_page_title(active_tab):
    pass


def get_menu_old(active_tab):

    name_link_list = [
        {'label': 'Green Growth Index',
            'value': '/SimulationDashBoard/global_overview'},
        {'label': 'Simulation Tool', 'value': '/SimulationDashBoard/simulation'},
        {'label': 'Evidence Library', 'value': '/SimulationDashBoard/models'},
    ]

    div_list = get_menu_div_list(name_link_list, active_tab=active_tab, active_style={
                                 'text-decoration': 'none', 'color': '#2db29b'}, className="tab")

    menu = html.Div(div_list, className="row all-tabs")
    return menu


def get_menu(active_tab):

    tab_menu = {
        'Global Overview': "Green Growth Index",
        'Regional Outlook': "Green Growth Index",
        'Country Profile': "Green Growth Index",
        'Country Comparison': "Green Growth Index",
        'Data': "Evidence Library",
        'Models Overview': "Evidence Library",
        'Simulation': "Simulation Tool"
    }

    tabs_links = {
        'Green Growth Index': '/SimulationDashBoard/global_overview',
        'Simulation Tool': '/SimulationDashBoard/simulation',
        'Evidence Library': '/SimulationDashBoard/models',
    }

    menu_list = []

    for name, link in tabs_links.items():
        if name == tab_menu[active_tab]:
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


def page_menu(active_tab):
    if active_tab in ['Global Overview', 'Regional Outlook', 'Country Profile', 'Country Comparison']:
        return gg_index_menu(active_tab)
    if active_tab in ['Models Overview', 'Data']:
        return evidence_lib_menu(active_tab)
    if active_tab in ['Simulation', 'Spatial Analysis']:
        return simtool_menu(active_tab)


def simtool_menu(active_tab):
    name_link_list = [
        {'label': 'Simulation', 'value': '/SimulationDashBoard/simulation'},
        #{'label': 'Spatial Analysis', 'value': '/SimulationDashBoard/simulation/spatial'},
    ]
    div_list = get_menu_div_list(name_link_list, active_tab, className='tab')

    return html.Div(div_list, className="row all-tabs")


def gg_index_menu(active_tab):
    name_link_list = [
        {'label': 'Global Overview', 'value': '/SimulationDashBoard/global_overview'},
        {'label': 'Regional Outlook', 'value': '/SimulationDashBoard/regional-outlouk'},
        {'label': 'Country Profile', 'value': '/SimulationDashBoard/country-profile'},
        {'label': 'Country Comparison',
            'value': '/SimulationDashBoard/country-comparator'},
    ]
    div_list = get_menu_div_list(name_link_list, active_tab, className='tab')

    return html.Div(div_list, className="row all-tabs")


def evidence_lib_menu(active_tab):
    name_link_list = [
        {'label': 'Models Overview', 'value': '/SimulationDashBoard/models'},
        {'label': 'Data', 'value': '/SimulationDashBoard/data'},
    ]
    div_list = get_menu_div_list(name_link_list, active_tab,  className='tab')
    # return html.Div(div_list, className="thirdtabmain")
    return html.Div(div_list, className="row all-tabs")


def get_menu_div_list(name_link_list, active_tab, className='thirdtabs', active_style={'background-color': '#0bb89c', 'color': 'white'}):
    div_list = []

    for name_link in name_link_list:
        name = name_link['label']
        link = name_link['value']

        if name == active_tab:
            div = html.Div(
                [dcc.Link(html.Button(name, style=active_style), href=link)], className=className)

        else:
            div = html.Div(
                [dcc.Link(html.Button(name), href=link)], className=className)

        div_list.append(div)

    return div_list


def is_btn_clicked(btn_id):
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    return btn_id in changed_id
