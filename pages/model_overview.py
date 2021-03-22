import dash_cytoscape as cyto
import networkx as nx
import dash_html_components as html
import dash_table
import dash_core_components as dcc
import pandas as pd
from GM.models.all_models import all_models, model_properties
import dash
from app import app
from dash.dependencies import Input, Output
from utils import Header


model_dictionnary = all_models


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
            # 'background-color': 'black',
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
                          for key in model_dictionnary.keys()]
    dropdown = html.Div(
        [
            html.H6(
                "Select model group: ",
                className="subtitle padded",
            ),
            dcc.Dropdown(id="my-dynamic-dropdown",
                         options=model_group_option,
                         value='EW_models'),
            html.H6(
                "Select model: ",
                className="subtitle padded",
            ),
            dcc.Dropdown(id="my-multi-dynamic-dropdown",
                         multi=False, value='EW_model')
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
        [html.H6(id="box1"), html.P("TO DO", id='box1_content')],
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

                html.Div(
                    [
                        html.Div(
                            [html.H5(id="graphbox"), html.P("Hover on node for info", style={
                                'font-weight': 'bold', 'font-size': 15}, id='cytoscape-mouseoverNodeData-output')],
                            className="mini_container",
                        ),
                        cy_graph
                    ], className='container eight columns'),
                html.Div(
                    [
                        html.Button('Reset Graph', id='btn-reset', n_clicks=0),
                        html.H6(
                            "Node description",
                            className="subtitle padded",
                        ),
                        html.Div(
                            [html.H5(id="graphbox"), html.P("Click on a node to get more information",
                                                            id='cytoscape-tapNodeData-output')],
                            className="product",
                        ),
                        html.H6(
                            "Impact",
                            className="subtitle padded",
                        ),
                        html.Div(
                            [html.H5(id="impactbox"), html.P(
                                "", id='cytoscape-tapNodeData-impact', style={'font-weight': 'bold', 'font-size': 20})],
                            className="product",
                        ),


                    ],
                    id="var-info-box",
                    className="pretty_container four columns",
                ),
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

    layout = html.Div([html.H6("Model description:", className="subtitle padded"),
                       html.P(tmp_text, id='description-graph-model')])
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
    model_option = [{'label': key, 'value': key}
                    for key in model_dictionnary[value].keys()]
    return model_option, model_option[0]['value']


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
        Input("btn-reset", "n_clicks")
    ],
)
def update_graph_plot(model_option, group_option, n_clicks):
    model = model_dictionnary[group_option][model_option]

    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    if 'btn-reset' in changed_id:
        return GraphModel_to_cytodata(model)['elements']

    return GraphModel_to_cytodata(model)['elements']


@app.callback(
    Output("description-graph-model", "children"),
    [
        Input("my-multi-dynamic-dropdown", "value"),
        Input("my-dynamic-dropdown", "value"),
        Input("btn-reset", "n_clicks")
    ],
)
def update_graph_description(model_option, group_option, n_clicks):
    model = model_dictionnary[group_option][model_option]

    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    if 'btn-reset' in changed_id:
        return GraphModel_to_cytodata(model)['elements']

    if model_option not in model_properties:
        return 'TODO'
    else:
        return model_properties[model_option]['description']


@app.callback(
    Output("box1_content", "children"),
    [
        Input("my-multi-dynamic-dropdown", "value"),
        Input("my-dynamic-dropdown", "value"),
        Input("btn-reset", "n_clicks")
    ],
)
def update_boxes(model_option, group_option, n_clicks):
    model = model_dictionnary[group_option][model_option]

    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    if 'btn-reset' in changed_id:
        return GraphModel_to_cytodata(model)['elements']

    if model_option not in model_properties:
        return 'TODO'

    if model_properties[model_option]['model_group'] == 'Water':
        return "💧"
    if model_properties[model_option]['model_group'] == 'AFOLU':
        return "🌲"
    else:
        return 'TODO'


@app.callback(Output('cytoscape-tapNodeData-output', 'children'),
              [Input('cytoscape-graph-model', 'tapNodeData'),
               Input("btn-reset", "n_clicks")])
def displayTapNodeData(data, n_clicks):
    if data:
        if data['type'] != 'computationnal':
            return html.Div(
                [
                    html.P(f"{data['id']}", style={
                           'font-size': 20, 'font-weight': 'bold'}),
                    html.P(
                        f"This node is an {data['type']}"),
                    html.P(
                        f"It represents the {data['name']}.", style={'font-weight': 'bold'}),
                    html.P(
                        f"It expressed in {data['unit']}.")
                ]
            )
        else:
            return html.Div(
                [
                    html.P(f"{data['id']}", style={
                           'font-size': 20, 'font-weight': 'bold'}),
                    html.P(f"This node computes: "),
                    html.P(f"{data['out']} = {data['name']}",
                           style={"font-weight": 'bold'})
                ]
            )

    return html.P("Click on a node to get more information", style={'font-weight': 'bold'})


@app.callback(Output('cytoscape-mouseoverNodeData-output', 'children'),
              Input('cytoscape-graph-model', 'mouseoverNodeData'))
def displayHoverNodeData(data):
    if data:
        if data['type'] != 'computationnal':
            return f"Represents {data['id']}: {data['name']}"
        else:
            return f"Computes {data['out']} = {data['name']}"


@app.callback(Output('cytoscape-tapNodeData-impact', 'children'),
              [Input('cytoscape-graph-model', 'tapNodeData'),
               Input("my-multi-dynamic-dropdown", "value"),
               Input("my-dynamic-dropdown", "value"),
               Input("btn-reset", "n_clicks")])
def displayImpactNodeData(data, model_option, group_option, n_clicks):
    G = model_dictionnary[group_option][model_option]
    outputs = G.outputs_()
    impacted_nodes = []

    if not data:
        return ''

    if data['id'] in G:
        for output in outputs:
            if nx.has_path(G, data['id'], output):
                impacted_nodes.append(output)

    return ', '.join(impacted_nodes)


@app.callback(Output('cytoscape-graph-model', 'stylesheet'),
              [Input('cytoscape-graph-model', 'tapNodeData'),
               Input("my-multi-dynamic-dropdown", "value"),
               Input("my-dynamic-dropdown", "value"),
               Input("btn-reset", "n_clicks")])
def highlightpath(data, model_option, group_option, n_clicks):
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]

    if 'btn-reset' in changed_id:
        return STYLESHEET

    if not data:
        return STYLESHEET
    else:
        G = model_dictionnary[group_option][model_option]
        outputs = G.outputs_()

        res = STYLESHEET.copy()
        if data['id'] in G:
            for output in outputs:
                if nx.has_path(G, data['id'], output):
                    res += highlighted_node_stylesheet(G, data['id'], output)
        return res
