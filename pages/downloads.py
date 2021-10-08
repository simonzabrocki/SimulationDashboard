from os import link
from pages.country_comparator import HTML_text
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px

from utils import Header, is_btn_clicked
from app import app, data, indicator_data, indicator_properties
from dash.dependencies import Input, Output
from ggmodel_dev.models.utils import all_model_dictionary
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
        className="three columns",
        )

    
    


layout = html.Div(
    [
        html.Div([Header(app, 'Downloads')]),
        # page 1
        html.Div(
            [
                html.Div([
                    download_box('All Results', 'Indicators, categories, dimensions and Index.','data'),
                    download_box('All Indicators', 'Raw Indicators.','ind'),
                    download_box('All definitions', 'Indicators definition.','def'),
                    download_box('All Models', 'Models specifications.','model'),

                    ],className="row")
                
                ],
            className="pretty_container twelve columns"
        ),

    ],
    className="page",
)


@app.callback(
    Output("model-download", "data"),
    [
        Input("model-download-btn", "n_clicks"),
    ],
    prevent_initial_call=True,
)
def downdload_table(n_clicks):
    if is_btn_clicked('model-download-btn'):
        return dcc.send_data_frame(all_model_dictionary['GGGM_model'].summary_df.to_csv, f"GGI_models_summary.csv")


@app.callback(
    Output("data-download", "data"),
    [
        Input("data-download-btn", "n_clicks"),
    ],
    prevent_initial_call=True,
)
def downdload_table(n_clicks):
    if is_btn_clicked('data-download-btn'):
        return dcc.send_data_frame(data.drop(columns=['Continent', 'UNregion', 'IncomeLevel', 'Region', 'Country', 'Variable_name', 'Category', 'Dimension']).to_csv, f"GGIndex_data.csv")



@app.callback(
    Output("ind-download", "data"),
    [
        Input("ind-download-btn", "n_clicks"),
    ],
    prevent_initial_call=True,
)
def downdload_table(n_clicks):
    if is_btn_clicked('ind-download-btn'):
        return dcc.send_data_frame(indicator_data.to_csv, f"indicator_data.csv")



@app.callback(
    Output("def-download", "data"),
    [
        Input("def-download-btn", "n_clicks"),
    ],
    prevent_initial_call=True,
)
def downdload_table(n_clicks):
    if is_btn_clicked('ind-download-btn'):
        return dcc.send_data_frame(indicator_properties.drop(columns=['maxYear', 'minYear']).to_csv, f"indicator_definition.csv")