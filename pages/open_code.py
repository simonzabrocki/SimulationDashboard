from os import link
from pages.country_comparator import HTML_text
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px

from utils import Header, Footer
from app import app




def github_link_box(title, description, link):
    return html.Div(
        [
            html.Div(
                    [

                        html.H5(f'{title}', style={'font-weight': 'bold'}),
                        html.Hr(style={"color": "#ffffff"}),
                        html.P(
                            f"{description}",
                            style={"color": "#ffffff", 'font-size': '18px'},
                            className="row",
                        ),
                        html.A(html.Button('Code', style={"color": "#ffffff", 'font-size': '12px'}), href=f'{link}', target="_blank"),
                    ],
                    className="product",
                ),
        ],
        className="four columns",
        )

    
    


layout = html.Div(
    [
        html.Div([Header(app, 'Codes')]),
        # page 1
        html.Div(
            [
                html.Div([
                    github_link_box('Green Growth Index', 'A python program to download, process and perform all the step to compute the green growth index.','https://github.com/simonzabrocki/Anticipe'),
                    github_link_box('Graph Models', 'A python framework to compute and visualize GGGI models using computational graphs.','https://github.com/Global-Green-Growth-Institute/GraphModels'),
                    github_link_box('Interface', 'A Dash web application to vizualize the index and simulate green growth policies','https://github.com/simonzabrocki/SimulationDashboard')
                    ],className="row")
                
                ],
            className="pretty_container twelve columns"
        ),
        Footer(),
    ],
    className="page",
)
