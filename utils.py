import dash
import dash_html_components as html
import dash_core_components as dcc


def Header(app, active_tab='Global Overview'):
    top_header = get_header(app)
    menu = get_menu(active_tab)

    page_title = html.Div(
        [
            html.Div([
                page_menu(active_tab)],
                className='twelve columns'),
        ],
        className="row")

    return html.Div([
        html.Div([
            top_header,
            html.Br([]),
            menu,
            ], className='mainheader'),
        page_title])

def Footer():
     return html.Footer('© Global Green Growth Institute 2022. All Rights Reserved.')

     
def get_header(app):
    header = html.Div(
        [
            html.Div(
                [   
                    html.Img(
                            src=app.get_asset_url("GGGI_logo.png"),
                            className="logo",
                            ),
                    # html.Div([
                        
                    #     html.Ul([
                    #         html.Li(
                    #             [html.A("Home", href="https://greengrowthindex.gggi.org/",), ]),
                    #         html.Li([html.Span(), ]),
                    #         html.Li(
                    #             [html.A("Index and Simulation", href="localhost:8080",), ]),
                    #         html.Li([html.Span(), ]),
                    #         html.Li(
                    #             [html.A("Publications", href="https://greengrowthindex.gggi.org/?page_id=3126",), ]),
                    #         html.Li([html.Span(), ]),
                    #         html.Li(
                    #             [html.A("Authors", href="https://greengrowthindex.gggi.org/?page_id=3080",), ]),
                    #         html.Li([html.Span(), ]),
                    #         html.Li(
                    #             [html.A("Reviewers", href="https://greengrowthindex.gggi.org/?page_id=1975",), ]),
                    #         html.Li([html.Span(), ]),
                    #         html.Li(
                    #             [html.A("Partners", href="https://greengrowthindex.gggi.org/?page_id=2166",), ]),
                    #         html.Li([html.Span(), ]),
                    #         html.Li(
                    #             [html.A("Contact Us", href="https://greengrowthindex.gggi.org/?page_id=2839",), ]),
                    #     ]),
                    # ], className="mainnav"),
                ],className="twelve columns",
            ),
        ],
    )
    return header


def get_menu(active_tab):

    tab_menu = {
        'Global Overview': "Green Growth Index",
        'Regional Outlook': "Green Growth Index",
        'Country Profile': "Green Growth Index",
        'Country Comparison': "Green Growth Index",
        'Data': "Evidence Library",
        #'Models': "Evidence Library",
        'Codes': "Evidence Library",
        'Simulation': "Simulation Tool",
        'Downloads': "Evidence Library",
    }

    tabs_links = {
        'Green Growth Index': '/SimulationDashBoard/global_overview',
        #'Simulation Tool': '/SimulationDashBoard/simulation',
        'Evidence Library': '/SimulationDashBoard/data',
    }

    menu_list = []

    for name, link in tabs_links.items():
        if name == tab_menu[active_tab]:
            tab = dcc.Link(
                name,
                href=link,
                className="tab",
                style={'color': '#FFFFFF', 'font-weight': 'bold'}

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
    if active_tab in ['Models', 'Data', 'Codes', 'Downloads']:
        return evidence_lib_menu(active_tab)
    if active_tab in ['Simulation', 'Spatial Analysis']:
        return simtool_menu(active_tab)


def simtool_menu(active_tab):
    name_link_list = [
        {'label': 'Simulation', 'value': '/SimulationDashBoard/simulation'},
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
        # {'label': 'Models', 'value': '/SimulationDashBoard/models'},
        {'label': 'Data', 'value': '/SimulationDashBoard/data'},
        {'label': 'Codes', 'value': '/SimulationDashBoard/codes'},
        {'label': 'Downloads', 'value': '/SimulationDashBoard/downloads'},
    ]
    div_list = get_menu_div_list(name_link_list, active_tab,  className='tab')
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


def dcc_config(file_name):
    return {'toImageButtonOptions': {'format': 'png',
                                     'filename': f'{file_name}',
                                     'scale': 2,
                                     },
            'displaylogo': False,
            'modeBarButtonsToRemove': ['zoom2d', 'pan2d',
                                       'select2d', 'lasso2d',
                                       'zoomIn2d', 'zoomOut2d', 'toggleSpikelines', 'autoScale2d']}