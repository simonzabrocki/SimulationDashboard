import dash_cytoscape as cyto
import networkx as nx
import dash_html_components as html
import dash_table
import dash_core_components as dcc
import pandas as pd
from GM.models.all_models import all_models
import dash
from app import app
from dash.dependencies import Input, Output
from utils import Header

model_dictionnary = all_models


def query_model_data(model, data):
    return data[data.Variable.isin(model.summary_df.index)]


def make_ISO_data_summary(ISO, model, data_dict):
    model_data_df = query_model_data(model, data_dict)
    ISO_df = model_data_df[model_data_df.ISO == ISO]
    return pd.merge(ISO_df, model.summary_df, left_on='Variable', right_index=True)


def make_dropdown_menu(model_dictionnary):

    model_group_option = [{'label': key, 'value': key} for key in model_dictionnary.keys()]
    dropdown = html.Div(
        [
            html.Label(["Model group:", dcc.Dropdown(id="my-dynamic-dropdown",
                                                     options=model_group_option,
                                                     value='EW_models')]),
            html.Label(
                [
                    "Model:",
                    dcc.Dropdown(id="my-multi-dynamic-dropdown", multi=False, value='EW_model'),
                ]
            ),
        ]
    )

    return dropdown


cyto.load_extra_layouts()


STYLESHEET = [
    {
        'selector': 'node',

        'style': {'content': 'data(type)',
                  'label': 'data(id)',
                  'text-halign': 'center',
                  'text-valign': 'center',
                  'height': 80, 'width': 80}
    },
    {
        'selector': 'edge',
        'style': {
            'curve-style': 'bezier',
            'target-arrow-shape': 'triangle',
        }
    },
    {'selector': '[type = "input"]',
     'style': {
         'background-color': '#e76f51',
     }
     },
    {'selector': '[type = "parameter"]',
     'style': {
         'background-color': '#e9c46a',
     }
     },
    {'selector': '[type = "variable"]',
     'style': {
         'background-color': '#f4a261',
     }
     },
    {'selector': '[type = "output"]',
     'style': {
         'background-color': '#2a9d8f',
         'height': 150, 'width': 150,
     }
     },
]


def GraphModel_to_cytodata(model):
    data = nx.readwrite.json_graph.cytoscape_data(model)

    for dic in data['elements']['nodes']:
        if 'formula' in dic['data']:
            del dic['data']['formula']

    return data


def info_boxes_display():
    layout = html.Div([html.Div(
        [html.H6(id="box1"), html.P("TO DO")],
        className="mini_container",
    ),
        html.Div(
        [html.H6(id="box2"), html.P("TO DO")],
        className="mini_container",
    ),
        html.Div(
        [html.H6(id="box3"), html.P("TO DO")],
        className="mini_container",
    )],
        id="info-container",
        className="row container-display",)
    return layout


def graph_display():
    layout = html.Div([
        html.Div(
            [html.H5(id="graphbox"), html.P("Hover on node for info", id='cytoscape-mouseoverNodeData-output')],
            className="mini_container",
        ),
        cyto.Cytoscape(
            id='cytoscape-graph-model',
            layout={'name': 'dagre',
                    'animate': True,
                    'animationDuration': 300},
            style={'width': '100%', 'height': '1000px'},
            stylesheet=STYLESHEET,
            zoomingEnabled=True,
            panningEnabled=True,
            autoungrabify=True,
            minZoom=0.2,
            maxZoom=3,
        ),
    ]
    )
    return layout


def description_display():
    tmp_text = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."

    layout = html.Div([html.P("Model description:", className="control_label"),
                       html.P(tmp_text, id='description-graph-model')])
    return layout


def summary_table_display():
    layout = html.Div([
        html.P("Model summary table:", className="control_label"),
        dash_table.DataTable(id='summary_table',
                             columns=[{'name': 'id', 'id': 'id'},
                                      {'name': 'name', 'id': 'name'},
                                      {'name': 'type', 'id': 'type'},
                                      {'name': 'unit', 'id': 'unit'},
                                      {'name': 'computation', 'id': 'computation'}
                                      ],
                             style_table={'overflowX': 'auto',
                                          'height': '600px',
                                          'overflowY': 'auto'},
                             style_cell={'font_family': 'roboto'}
                             )

    ]
    )
    return layout


layout = html.Div(
    [
        html.Div([Header(app)]),
        html.Div(
            [
                html.Div(
                    [
                        make_dropdown_menu(all_models),
                        info_boxes_display(),
                        description_display(),
                        summary_table_display()
                    ],
                    className="pretty_container four columns",
                    id="model-presentation-display",
                ),
                html.Div(
                    [
                        graph_display()
                    ],
                    id="right-column",
                    className="pretty_container eight columns",
                ),
            ],
            className="row",
        ),
    ],
    className="page",
)


@app.callback(
    dash.dependencies.Output("my-multi-dynamic-dropdown", "options"),
    dash.dependencies.Output("my-multi-dynamic-dropdown", "value"),
    [dash.dependencies.Input("my-dynamic-dropdown", "value")],
)
def update_multi_options(value):
    model_option = [{'label': key, 'value': key} for key in model_dictionnary[value].keys()]
    return model_option, model_option[0]['value']


# Selectors -> main graph
@app.callback(
    Output("summary_graph", "figure"),
    [
        Input("country_selector", "value"),
        Input("model_selector", "value"),
    ],
)
def make_summary_plot(country_selector, model_selector):
    data_summary_df = make_ISO_data_summary(
        country_selector, model_dictionnary[model_selector], data)
    return plot_EW1_summary(data_summary_df)


@app.callback(
    Output("summary_table", "data"),
    [
        Input("my-multi-dynamic-dropdown", "value"),
        Input("my-dynamic-dropdown", "value"),
    ],
)
def update_summary_table(model_option, group_option):
    return model_dictionnary[group_option][model_option].summary_df.reset_index().to_dict('records')


@app.callback(
    Output("cytoscape-graph-model", "elements"),
    [
        Input("my-multi-dynamic-dropdown", "value"),
        Input("my-dynamic-dropdown", "value"),
    ],
)
def update_graph_plot(model_option, group_option):
    model = model_dictionnary[group_option][model_option]
    return GraphModel_to_cytodata(model)['elements']


@app.callback(Output('cytoscape-mouseoverNodeData-output', 'children'),
              Input('cytoscape-graph-model', 'mouseoverNodeData'))
def displayTapNodeData(data):
    if data:
        if data['type'] != 'computationnal':
            return f"This node represents the {data['type']} {data['name']} expressed in {data['unit']}."
        else:
            return f"This node computes {data['out']} = {data['name']}"
