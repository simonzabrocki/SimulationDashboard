import dash_html_components as html
import dash_table
import dash_core_components as dcc
import pandas as pd
from GM.models.all_models import all_models
import dash
from app import app
from dash.dependencies import Input, Output
from utils import Header


layout = html.Div(
    [
        html.Div([Header(app)]),
    ],
    className="page",
)
