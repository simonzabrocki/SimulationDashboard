# -*- coding: utf-8 -*-
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from app import app
from pages import (
    global_overview,
    simulation,
    country_profile,
    regional_outlook,
    data_viz,
    model_overview
)

app.layout = html.Div(
    [dcc.Location(id="url", refresh=False), html.Div(id="page-content")]
)

server = app.server


# Update page

@app.callback(Output("page-content", "children"),
              [Input("url", "pathname")])
def display_page(pathname):
    if pathname == "/SimulationDashBoard/regional-outlouk":
        return regional_outlook.layout
    elif pathname == "/SimulationDashBoard/country-profile":
        return country_profile.layout
    elif pathname == "/SimulationDashBoard/models":
        return model_overview.layout
    elif pathname == "/SimulationDashBoard/data":
        return data_viz.layout
    else:
        return global_overview.layout


if __name__ == "__main__":
    app.run_server(debug=True, host='localhost', port=8080,
                   #dev_tools_ui=False,
                   #dev_tools_props_check=False,
                   )
