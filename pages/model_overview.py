import dash_cytoscape as cyto
from dash_html_components.Div import Div
import networkx as nx
import dash_html_components as html
import dash_table
import dash_core_components as dcc
import pandas as pd
import dash
from app import app
from dash.dependencies import Input, Output
from utils import Header
from ggmodel_dev.models.utils import all_model_dictionary, all_model_properties_df
from utils import is_btn_clicked


cyto.load_extra_layouts()


STYLESHEET = [
    {
        'selector': 'node',

        'style': {'content': 'data(type)',
                  'label': 'data(id)',
                  'font-size': 20,
                  'font-weight': 'bold',
                  'text-halign': 'center',
                  'text-valign': 'center',
                  'border-width': 0,
                  'height': 80, 'width': 80}
    },
    {
        'selector': 'edge',
        'style': {
            'curve-style': 'bezier',
            'target-arrow-shape': 'triangle',
            'selectable': False,
            'grabbable': False,
            'overlay-opacity': 0,
            'line-color': '#D3D3D3',
            'target-arrow-color': '#D3D3D3',
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
    {'selector': '[type = "computationnal"]',
     'style': {
         'background-color': '#D3D3D3',
     }
     },
    {'selector': '[type = "output"]',
     'style': {
         'background-color': '#2a9d8f',
         'height': 150, 'width': 150,
     }
     },
    {
        'selector': 'node:selected',
        'style': {
            'border-color': '#A9A9A9',
            'border-style': 'solid',
            'border-width': 5,
            'border-opacity': 1,
        }
    },
    {
        'selector': 'node:unselected',
        'style': {
            'background-opacity': 0.6
        }
    },
]


def query_model_data(model, data):
    return data[data.Variable.isin(model.summary_df.index)]


def make_ISO_data_summary(ISO, model, data_dict):
    model_data_df = query_model_data(model, data_dict)
    ISO_df = model_data_df[model_data_df.ISO == ISO]
    return pd.merge(ISO_df, model.summary_df, left_on='Variable', right_index=True)


def make_dropdown_menu(model_dictionnary):

    model_group_option = [{'label': key, 'value': key}
                          for key in all_model_properties_df.model_group.unique().tolist()]

    dropdown = html.Div(
        [
            html.H5(
                "Select a sector",
                className="subtitle padded",
            ),
            html.Br([]),
            dcc.Dropdown(id="my-dynamic-dropdown",
                         options=model_group_option,
                         value='Water',
                         clearable=False),
            html.Br([]),
            html.H5(
                "Select a model",
                className="subtitle padded",
            ),
            html.Br([]),
            dcc.Dropdown(id="my-multi-dynamic-dropdown",
                         multi=False, value='EW_model', clearable=False)
        ]
    )
    return dropdown


def GraphModel_to_cytodata(model):
    data = nx.readwrite.json_graph.cytoscape_data(model)

    for dic in data['elements']['nodes']:
        if 'formula' in dic['data']:
            del dic['data']['formula']

    return data


def info_boxes_display():
    layout = html.Div([html.Div(
        [html.P("Sector"), html.P(id="box1_content", style={'font-size': 25})],
        className="mini_container",
    ),
        html.Div(
        [html.P("Status"), html.H6(
            id="box2_content", style={'font-size': 25})],
        className="mini_container",
    ),
    ],
        id="info-container",
        className="row container-display",)
    return layout


def graph_display():
    cy_graph = cyto.Cytoscape(
        id='cytoscape-graph-model',
        layout={'name': 'dagre',
                'animate': True,
                'animationDuration': 300},
        style={'width': '100%', 'height': '1000px'},
        stylesheet=STYLESHEET,
        elements=[],
        zoomingEnabled=True,
        panningEnabled=True,
        autoungrabify=True,
        minZoom=0.2,
        maxZoom=3,
    )

    layout = html.Div([
        html.Div(
            [
                html.Button('Reset Graph', id='btn-reset', n_clicks=0),
                html.Div(
                    [
                        html.Div(
                            [
                                html.H6(
                                    "1. Hover on node for full name",
                                    className="subtitle padded",
                                ),
                                html.Div(
                                    [
                                        html.H5(id="graphbox"), html.P("Hover on node for info", style={
                                            'font-weight': 'bold', 'font-size': 15}, id='cytoscape-mouseoverNodeData-output')
                                    ],
                                    className="product",
                                )
                            ],
                            className='bare_container four columns'
                        ),
                        html.Div(
                            [
                                html.H6(
                                    "2. Click on Node for description",
                                    className="subtitle padded",
                                ),
                                html.Div(
                                    [
                                        html.H5(id="graphbox"), html.P(
                                            "Click on a node to get the description", id='cytoscape-tapNodeData-output',  style={'font-weight': 'bold', 'font-size': 15})
                                    ],
                                    className="product"
                                )
                            ],
                            className='bare_container four columns'
                        ),
                        html.Div(
                            [
                                html.H6(
                                    "3. Get the impacts on Indicators",
                                    className="subtitle padded",
                                ),
                                html.Div(
                                    [
                                        html.H5(id="impactbox"), html.P(
                                            "Click on a node to see its impact", id='cytoscape-tapNodeData-impact', style={'font-weight': 'bold', 'font-size': 15})
                                    ],
                                    className="product",
                                ),
                            ],
                            className='bare_container four columns'
                        ),
                    ],
                    id="var-info-box",
                    className="row"
                ),
                html.Div([
                    cy_graph
                    ]),
            ],
            className='row'
        ),
    ]
    )
    return layout


def highlighted_node_stylesheet(G, source, target):
    all_paths = list(nx.all_simple_paths(G, source, target))

    source_target = []

    for path in all_paths:
        source_target += [(path[i], path[i + 1])
                          for i, _ in enumerate(path[:-1])]

    child_style = []
    for s_t in source_target:

        child_style.append({'selector': f'edge[source = "{s_t[0]}"][target = "{s_t[1]}"]',
                            'style': {
                                'line-color': 'black',
                                'width': 5,
                                'target-arrow-color': 'black'
                            }})

        child_style.append({'selector': f'node[id = "{s_t[1]}"]',
                            'style': {
                                'border-color': 'black',
                                'border-style': 'dotted',
                                'border-width': 3,
                                'border-opacity': 1,
                            }})

    return child_style


def description_display():
    tmp_text = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."

    layout = html.Div([
        html.H6("Model description:", className="subtitle padded"),
        html.Div(
            [
                html.P(tmp_text, id='description-graph-model',
                       style={'font-size': 13})
            ],
            className='product'),
        html.H6("Model sources:", className="subtitle padded"),
        html.Div(
            [
                html.P('model sources', id='source-graph-model',
                       style={'font-size': 13})
            ],
            className='product'),
    ]
    )

    return layout


def summary_table_display():
    layout = html.Div([
        html.H6(
            "Model summary table: ",
            className="subtitle padded",
        ),
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
                        make_dropdown_menu(all_model_dictionary),
                        info_boxes_display(),
                        description_display(),
                        html.Div([
                            html.Button('Download Summary Table', id='btn-download', n_clicks=0),
                            dcc.Download(id="download-summary-csv"),

                        ]),
                        
                        

                    ],
                    className="pretty_container four columns",
                    id="model-presentation-display",
                ),
                html.Div(
                    [
                        graph_display(),
                        summary_table_display(),
                    ],
                    id="right-column",
                    className="pretty_container eight columns",
                )
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
    model_option = (
        all_model_properties_df.query(f'model_group == "{value}"')[
            ['model', 'display_name']]
        .rename(columns={'model': 'value', 'display_name': 'label'})
        .to_dict('records')
    )
    return model_option, model_option[0]['value']


@app.callback(
    Output("summary_table", "data"),
    [
        Input("my-multi-dynamic-dropdown", "value"),
    ],
)
def update_summary_table(model_option):
    return all_model_dictionary[model_option].summary_df.reset_index().to_dict('records')

@app.callback(
    Output("download-summary-csv", "data"),
    [
        Input("btn-download", "n_clicks"),
        Input("my-multi-dynamic-dropdown", "value"),
    ],
    prevent_initial_call=True,
)
def downdload_table(n_clicks, model_option):
    if is_btn_clicked('btn-download'):
        return dcc.send_data_frame(all_model_dictionary[model_option].summary_df.to_csv, f"{model_option}_summary.csv")

@app.callback(
    Output("cytoscape-graph-model", "elements"),
    [
        Input("my-multi-dynamic-dropdown", "value"),
        Input("btn-reset", "n_clicks")
    ],
)
def update_graph_plot(model_option, n_clicks):
    model = all_model_dictionary[model_option]

    if is_btn_clicked('btn-reset'):
        return GraphModel_to_cytodata(model)['elements']

    return GraphModel_to_cytodata(model)['elements']


@app.callback(
    Output("description-graph-model", "children"),
    Output('source-graph-model', 'children'),
    [
        Input("my-multi-dynamic-dropdown", "value"),
    ],
)
def update_graph_description(model_option):
    description = all_model_properties_df.query(f'model == "{model_option}"').description.values[0]
    source = all_model_properties_df.query(f'model == "{model_option}"').source.values[0]
    source = [html.Ol(el) for el in source]
    return description, source


@app.callback(
    Output("box1_content", "children"),
    Output('box2_content', 'children'),
    [
        Input("my-multi-dynamic-dropdown", "value"),
    ],
)
def update_boxes(model_option):
    symbol = all_model_properties_df.query(
        f'model == "{model_option}"').symbol.values[0]
    status = all_model_properties_df.query(
        f'model == "{model_option}"').status.values[0]
    return symbol, status


@app.callback(Output('cytoscape-tapNodeData-output', 'children'),
              [Input('cytoscape-graph-model', 'tapNodeData'),
               Input("btn-reset", "n_clicks")])
def displayTapNodeData(data, n_clicks):
    if data:
        if data['type'] != 'computationnal':
            return html.Div(
                [
                    html.P(f"{data['id']}: {data['name']}. ({data['unit']})", style={ 'font-size': 15, 'font-weight': 'bold'}),
                ]
            )
        else:
            return html.Div(
                [
                    html.P(f"{data['out']} = {data['name']}", style={'font-size': 15, 'font-weight': 'bold'}),
                ]
            )
    else:
        return html.P("Click on a node to get more information", style={'font-weight': 'bold', 'font-size': 15})


@app.callback(Output('cytoscape-mouseoverNodeData-output', 'children'),
              [
                  Input('cytoscape-graph-model', 'mouseoverNodeData'),
               ])
def displayHoverNodeData(data):
    if data:
        if data['type'] != 'computationnal':
            return f"{data['id']}: {data['name']}"
        else:
            return f"{data['out']} = {data['name']}"
    else:
        return "Hover on a node to get its full name"


@app.callback(Output('cytoscape-tapNodeData-impact', 'children'),
              [Input('cytoscape-graph-model', 'tapNodeData'),
               Input("my-multi-dynamic-dropdown", "value"),
               ])
def displayImpactNodeData(data, model_option):
    G = all_model_dictionary[model_option]
    outputs = G.outputs_()
    impacted_nodes = []
    
    if not data:
        return "Click on a node to see its impact"

    if data['id'] in G:
        for output in outputs:
            if nx.has_path(G, data['id'], output):
                name = G.nodes[output]['name']
                impacted_nodes.append(name)

    return ', '.join(impacted_nodes)


@app.callback(Output('cytoscape-graph-model', 'stylesheet'),
              [Input('cytoscape-graph-model', 'tapNodeData'),
               Input("my-multi-dynamic-dropdown", "value"),
               Input('cytoscape-graph-model', 'mouseoverNodeData'),
               Input('cytoscape-graph-model', 'selectedNodeData'),
               ])
def highlightpath(data, model_option, hover_node, selected_node):

    res = STYLESHEET.copy()

    if data and not selected_node:
        return res

    if data:
        G = all_model_dictionary[model_option]
        outputs = G.outputs_()
        if data['id'] in G:
            for output in outputs:
                if nx.has_path(G, data['id'], output):
                    res += highlighted_node_stylesheet(G, data['id'], output)

        node = data['id']

        style = [({'selector': f'node[id = "{node}"]',
                   'style': {
                       'label': 'data(name)',
                                'border-color': 'black',
                                'border-style': 'dotted',
                                'height': 160, 'width': 160,
                                'font-size': 12,
                                'border-width': 3,
                                'border-opacity': 1,
                   }})]
        res = res + style

    return res


@app.callback(
    Output('cytoscape-graph-model', 'mouseoverNodeData'),
    Output('cytoscape-graph-model', 'tapNodeData'),
    Output('cytoscape-graph-model', 'selectedNodeData'),
    [
        Input("btn-reset", "n_clicks")
    ])
def master_reset(n_clicks):
    return None, None, None
