# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from dash.dependencies import Input, Output
import plotly.express as px
from pages import (
    overview,
    pricePerformance,
    portfolioManagement,
    feesMins,
    distributions,
    newsReviews,
    country,
    world
)
import pandas as pd


app = dash.Dash(
    __name__, meta_tags=[{"name": "viewport", "content": "width=device-width"}]
)
app.title = 'GreenGrowthReport'

server = app.server

# Describe the layout/ UI of the app
app.layout = html.Div(
    [dcc.Location(id="url", refresh=False), html.Div(id="page-content")]
)


# Update page
@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def display_page(pathname):
    if pathname == "/SimulationDashBoard/price-performance":
        return pricePerformance.create_layout(app)
    elif pathname == "/SimulationDashBoard/data":
        return portfolioManagement.create_layout(app)
    elif pathname == "/SimulationDashBoard/world-outlouk":
        return world.create_layout(app)
    elif pathname == "/SimulationDashBoard/by-country":
        return country.create_layout(app)
    elif pathname == "/SimulationDashBoard/simulation":
        return newsReviews.create_layout(app)
    elif pathname == "/SimulationDashBoard/full-view":
        return (
            overview.create_layout(app),
            pricePerformance.create_layout(app),
            portfolioManagement.create_layout(app),
            feesMins.create_layout(app),
            distributions.create_layout(app),
            newsReviews.create_layout(app),
        )
    else:
        return overview.create_layout(app)


data = pd.read_csv('data/GGGI/GGIs_2015_2020.csv')
ISO_options = data[['ISO', 'Country']].drop_duplicates().values

Income_region_group = data.groupby(['Variable', 'Year', 'IncomeLevel', 'Region', 'Aggregation']).mean().reset_index()
Income_region_group['ISO'] = 'AVG' + '_' + Income_region_group["IncomeLevel"] + '_' + Income_region_group["Region"]
data = pd.concat([data, Income_region_group])


@app.callback(
    dash.dependencies.Output('Description', 'children'),
    [dash.dependencies.Input('ISO_select', 'value')],
    suppress_callback_exceptions=True)
def update_HTML(ISO):
    data_plot = data[(data.ISO.isin([ISO]))]

    if data_plot[data_plot.Aggregation == 'Index'].shape[0] > 0:
        data_plot = data_plot[data_plot.Aggregation == 'Index']
        Country = data_plot['Country'].values[0]
        Index = data_plot['Value'].values[0]
        Continent = data_plot['Continent'].values[0]
        Status = data_plot['IncomeLevel'].values[0]
    else:
        Country = data_plot.Country.unique()[0]
        Continent = data_plot['Continent'].values[0]
        Status = data_plot['IncomeLevel'].values[0]
        Index = 'Not available'

    return html.Div([
                    html.Div(
                        [
                            html.H5(f"{Country}: {Index}"),
                            html.Br([]),
                            html.P(
                                f"{Country} is a {Status} country located in {Continent}. Its Green Growth index is {Index}.",
                                style={"color": "#ffffff", 'font-size': '15px'},
                                className="row",
                            ),
                        ],
                        className="product",
                    )
                ],
                className="row",
            )


@app.callback(
    dash.dependencies.Output('Perf_ISO', 'figure'),
    [dash.dependencies.Input('ISO_select', 'value')])
def update_polar(ISO):

    data_plot = data[(data.ISO.isin([ISO])) & (data.Year == 2020)].fillna(0)

    cats = data_plot[(data_plot.Aggregation == 'Category')]

    fig = go.Figure()

    fig.add_trace(go.Scatterpolargl(
          r = cats.Value,
          theta = cats.Variable,
          name = "Trial 6",
          marker=dict(size=10, color="#14ac9c"),
          ))
    fig.update_traces(fill='toself')
    fig.update_traces(mode="markers", marker=dict(opacity=0.7))
    fig.update_layout(margin={"r": 20, "t": 20, "l": 20, "b": 20})
    return fig

@app.callback(
    dash.dependencies.Output('Dim_ISO', 'figure'),
    [dash.dependencies.Input('ISO_select', 'value')])
def update_loliplot(ISO):
    data_plot = data[(data.ISO.isin([ISO])) & (data.Year == 2020)].fillna(0)

    dims = data_plot[(data_plot.Aggregation == 'Dimension')]

    fig = px.scatter(dims,
                    x='Variable',
                    y='Value',
                    size=[8 for i in range(4)],
                    color=['blue', 'blue', 'blue', 'blue'],
                     labels={
                         "Variable": "Dimension",
                     },
                    )

    fig.update_traces(marker=dict(size=12,
                                  line=dict(width=12,
                                            color='#14ac9c')),
                      selector=dict(mode='markers'))


    fig.add_trace(go.Bar(y=dims['Value'], x=dims['Variable'],
                         width=[5e-2 for i in range(4)],
                        marker_color=['#14ac9c', '#14ac9c', '#14ac9c', '#14ac9c']))

    fig.update_layout(showlegend=False,hovermode=False)
    fig.update_yaxes(range=[0, 100])

    fig.update_xaxes(showgrid=False)

    return fig


@app.callback(
    dash.dependencies.Output('dim_time_series', 'figure'),
    [dash.dependencies.Input('ISO_select', 'value')])
def update_ts(ISO):
    data_ISO = data[(data.ISO.isin([ISO])) & (data.Aggregation.isin(['Dimension']))]
    fig = px.line(data_ISO,
                  facet_row="Variable",
                  color='Variable',
                  x='Year',
                  y='Value',
                  facet_row_spacing=0.01,
                  labels = {
                     'Value': ''
                  },
                  height=600)
    fig.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
    fig.update_yaxes(visible=True, fixedrange=True)
    fig.update_layout(showlegend=False)
    fig.update_traces(mode='lines+markers')
    return fig


@app.callback(
    dash.dependencies.Output('index_time_series', 'figure'),
    [dash.dependencies.Input('ISO_select', 'value')])
def update_ts_ind(ISO):
    REF = 'AVG_' + "_".join(data[data.ISO == ISO][["IncomeLevel", 'Region']].drop_duplicates().values[0].tolist())

    df = data[(data.ISO.isin([ISO, REF])) & (data.Aggregation == 'Index')]

    fig = px.line(df,
                  x='Year',
                  y='Value',
                  color='ISO',
                  line_dash='ISO',
                  color_discrete_map={ISO: '#14ac9c', REF: 'darkgrey'},
                  height=300)
    fig.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
    fig.update_yaxes(visible=True, fixedrange=True)
    fig.update_traces(mode='lines+markers')
    fig.update_layout(legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1
    ))
    return fig


if __name__ == "__main__":
    app.run_server(debug=True, host='localhost',
                   #dev_tools_ui=False,
                   #dev_tools_props_check=False
                   )
