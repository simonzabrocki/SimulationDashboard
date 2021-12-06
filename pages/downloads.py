from os import link
from pages.country_comparator import HTML_text
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px

from utils import Header
from app import app, data, indicator_data, indicator_properties
from dash.dependencies import Input, Output
#from ggmodel_dev.models.utils import all_model_dictionary
import dash_core_components as dcc



def download_box(title, description, id):
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
                        html.Button('Download', style={"color": "#ffffff", 'font-size': '12px'}, id=f'{id}-download-btn'),
                        dcc.Download(id=f"{id}-download"),
                    ],
                    className="product",
                ),
        ],
        className="four columns",
        )

    
    


layout = html.Div(
    [
        html.Div([Header(app, 'Downloads')]),
        # page 1
        html.Div(
            [
                html.Div([
                    download_box('Index', 'All index results.','data'),
                    download_box('Indicators', 'All raw Indicators.','ind'),
                    download_box('Definitions', 'All indicators definitions.','def'),
                    # download_box('Models', 'All models specifications.','model'),
                    ],className="row")
                
                ],
            className="pretty_container twelve columns"
        ),

    ],
    className="page",
)


# @app.callback(
#     Output("model-download", "data"),
#     [
#         Input("model-download-btn", "n_clicks"),
#     ],
#     prevent_initial_call=True,
# )
# def downdload_table(n_clicks):
#     return dcc.send_data_frame(all_model_dictionary['GGGM_model'].summary_df.to_csv, f"GGI_models_summary.csv")


@app.callback(
    Output("data-download", "data"),
    [
        Input("data-download-btn", "n_clicks"),
    ],
    prevent_initial_call=True,
)
def downdload_table(n_clicks):
    return dcc.send_data_frame(data.drop(columns=['Continent', 'Sub-region', 'IncomeLevel', 'Country', 'Variable_name', 'Category', 'Dimension']).to_csv, f"GGIndex_data.csv")



@app.callback(
    Output("ind-download", "data"),
    [
        Input("ind-download-btn", "n_clicks"),
    ],
    prevent_initial_call=True,
)
def downdload_table(n_clicks):
    return dcc.send_data_frame(indicator_data.to_csv, f"indicator_data.csv")



@app.callback(
    Output("def-download", "data"),
    [
        Input("def-download-btn", "n_clicks"),
    ],
    prevent_initial_call=True,
)
def downdload_table(n_clicks):
    return dcc.send_data_frame(indicator_properties.drop(columns=['maxYear', 'minYear', 'display_name']).to_csv, f"indicator_definition.csv")