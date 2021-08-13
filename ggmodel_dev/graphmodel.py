# New model
"""
Graph Model package to implement and vizualize green growth models

WARNINGs:
- As pandas explains, using loc[:, :, blabla] has really terrible performance, try to avoid

ROADMAP:
- Add auto unit check 
- Allow for arbitrary 'type' field that can have customizable plotting props
- Split in different file
- For fun maybe try to add some numba to speed up

- Add a concatenate function to properly concatenate models without duplicates OK !
- Automatically parse the computation to avoid having to type the name OK !
- Cleanup the parser TODO
- Rewrite parser and drawer as function rather than objects TODO
- Add on pip for easier use by the team + clean github repo

"""
__author__ = 'Simon Zabrocki'

import networkx as nx
import graphviz
import numpy as np
import pandas as pd
from functools import partial, reduce
import inspect
import copy
import time


draw_properties = {
    'fillcolor': {'input': '#e76f51',
                  'parameter': '#e9c46a',
                  'variable': '#f4a261',
                  'output': '#2a9d8f',
                  'computationnal': '#e76f51'},
    'fontcolor': {'input': '#eeeeee',
                  'parameter': '#eeeeee',
                  'variable': '#eeeeee',
                  'output': '#eeeeee',
                  'computationnal': '#000000'},
    'color': {'input': '#eeeeee',
              'parameter': '#eeeeee',
              'variable': '#eeeeee',
              'output': '#eeeeee',
              'computationnal': '#A9A9A9'},
    'style': {'input': 'filled',
              'parameter': 'filled',
              'variable': 'filled',
              'output': 'filled',
              'computationnal': ''},
}


class GraphModel(nx.DiGraph):
    '''GraphModel allows to write a model as a Graph.

    TO DO: Add minimal code example

    Attributes:
        node_ordering (list): Topological order of the computationnal nodes.
    '''

    def __init__(self, graph_specifications):
        '''Initialize a graph from a specification.

        Args:
            graph_specifications(dict): dict of node specification.
        '''
        super(GraphModel, self).__init__()
        self.make_graph(graph_specifications)
        self.node_ordering = self.get_computational_nodes_ordering()
        self.model_function = model_function(self)
        self.graph_specifications = graph_specifications

    def check_nodes_and_edges(self, nodes, edges):
        '''Checks that arguments of computations are defined in nodes.

        Args:
            nodes (List): list of nodes.
            edges (List): list of edges.
        '''
        node_set = set([n[0] for n in nodes])
        edge_set = set([e[0] for e in edges])
        diff = edge_set - node_set
        assert edge_set <= node_set, f"{diff} is used in a computation but is not defined in a node"

    def check_types(self, summary_df):
        '''Checks that node types are well defined with respect to computional/non computationnal.

        Args:
            nodes (List): list of nodes.
            edges (List): list of edges.
        '''
        summary_df = summary_df.copy().reset_index()
        summary_df_comp = summary_df[~summary_df.computation.isna()]
        summary_df_non_comp = summary_df[summary_df.computation.isna()]

        non_comp_wrong_nodes = summary_df_non_comp[~summary_df_non_comp.type.isin(['input', 'parameter'])].id.tolist()
        comp_wrong_nodes = summary_df_comp[~summary_df_comp.type.isin(['variable', 'output'])].id.tolist()

        assert len(non_comp_wrong_nodes) == 0, f'nodes {non_comp_wrong_nodes} are non computational but have wrong types'
        assert len(comp_wrong_nodes) == 0, f'nodes {comp_wrong_nodes} are computational but have wrong types'

    def make_graph(self, graph_nodes):
        '''Make the nx.Digraph object.

        Args:
            graph_nodes(List): list of formatted nodes

        Returns:
            None, Initialize the graph object.
        '''
        nodes, edges, summary_df = GraphParser().parse(graph_nodes)
        self.check_nodes_and_edges(nodes, edges)
        self.check_types(summary_df)
        self.add_nodes_from(nodes)
        self.add_edges_from(edges)
        self.summary_df = summary_df  # a bit clunky to put it here
        return None

    def get_node_by_type(self, node_type):
        '''Returns the nodes of a given node_type'''
        return [node_id for node_id, node in self.nodes.items() if node['type'] == node_type]

    def inputs_(self):
        return self.get_node_by_type('input')

    def outputs_(self):
        return self.get_node_by_type('output')

    def variables_(self):
        return self.get_node_by_type('variable')

    def parameters_(self):
        return self.get_node_by_type('parameter')

    def get_computational_nodes_ordering(self):
        '''Returns the sorted list of computationnal nodes.

        Returns:
            ordering(list): List of ordered computationnal nodes.
        '''
        ordering = [node for node in nx.topological_sort(self) if '_comp' in node]
        return ordering

    def run(self, X):
        '''Run the GraphModel given inputs and parameters.

        Args:
            X(dict): dictionnary of input and parameters.

        Returns:
            X(dict): inputs, variables and outputs of the graph.
        '''

        X = self.model_function(X)

        return X

    def run_step_wise(self, X):
        '''Debbugging function:
        Run the GraphModel given inputs and parameters step by step.

        Args:
            X(dict): dictionnary of input and parameters.

        Returns:
            X(dict): inputs, variables and outputs of the graph.
        '''
        X = self.step_wise_model_function(X)
        return X

    def step_wise_model_function(self, X):
        '''The function computed by the model. Used for debugging.
        Args:
            X(dict): The values of inputs, parameters, variables and outputs of the graph.
        Returns:
            X(dict): The values of inputs, parameters, variables and outputs of the graph.
        '''
        X = X.copy()
        for node_id in self.node_ordering:
            start = time.time()
            print(node_id, end=': ')

            node = self.nodes[node_id]
            computation = node['formula']

            result = computation(**X)
            out = node['out']
            X[out] = result

            end = time.time()
            print(end - start)

        return X

    def draw(self, draw_properties=draw_properties):
        '''Draw the graph.

        Args:
            draw_properties(dict): dictionnary of properties for the graph plot.
        '''
        return GraphDrawer(draw_properties).draw(self)

    def draw_computation(self, inputs_parameters, draw_properties=draw_properties):
        '''Draw the graph with the computated values.

        Args:
            draw_properties(dict): dictionnary of properties for the graph plot.
            inputs(dict): dictionnary of input values.
            parameters(dict): dictionnary of parameter values.
        '''
        return GraphDrawer(draw_properties).draw_computation(self, inputs_parameters)


class GraphDrawer():
    '''A class to draw the Graph models.

    Attributes:
        draw_properties(dict): dictionnary of properties for the graph plot.
    '''

    def __init__(self, draw_properties):
        '''Initialize the GraphDrawer

        Attributes:
            draw_properties(dict): dictionnary of properties for the graph plot.
        '''
        self.draw_properties = draw_properties
        return None

    def get_node_label(self, node):
        '''Get the label of a given node.

        TO CLEAN UP !!!

        Args:
            node(node): Node of the graph.

        Returns:
            label(str): A label for the node.
        '''
        node_id, label, node_type = node[0], node[1]['name'], node[1]['type']

        if node_type != 'computationnal':
            label = f"{label} \n ({node_id})"
            if 'value' in node[1]:
                value = node[1]['value']
                label = f"{label} \n {value}"
            if 'unit' in node[1]:
                unit = node[1]['unit']
                label = f"{label} \n {unit}"
        return label

    def draw_node(self, dot, node, draw_properties):
        '''Draw a node of the graph.

        TO CLEAN UP !!!

        Args:
            dot(dot): dot object for drawing.
            node(node): Node of the graph.
            draw_properties(dict): dictionnary of properties for the graph plot.

        Returns:
            None, updates the dot object.
        '''
        label = self.get_node_label(node)
        node_type = node[1]['type']
        dot.node(node[0], node[0], {"shape": "rectangle",
                                    "peripheries": "1",
                                    'label': label,
                                    'fillcolor': draw_properties['fillcolor'][node_type],
                                    'style': draw_properties['style'][node_type],
                                    'color': draw_properties['color'][node_type],
                                    'fontcolor': draw_properties['fontcolor'][node_type],
                                    'fontname': 'roboto'
                                    }
                 )

    def draw_edge(self, dot, a, b, draw_properties):
        '''Draw an edge of the graph.

        Args:
            dot(dot): dot object for drawing.
            a(node): Node of the graph.
            b(node): Node of the graph.
            draw_properties(dict): dictionnary of properties for the graph plot.
        '''
        dot.edge(a, b, color='#A9A9A9')

    def draw(self, G):
        '''Draw a full Graph Model

        Args:
            G(GraphModel): A graph model.

        Returns:
            dot(obj): The plot object of the graph.
        '''
        draw_properties = self.draw_properties
        dot = graphviz.Digraph(graph_attr={'splines': 'ortho'})
        for node in G.nodes(data=True):
            self.draw_node(dot, node, draw_properties)
        for a, b in G.edges:
            self.draw_edge(dot, a, b, draw_properties)
        return dot

    def draw_computation(self, G, inputs_parameters):
        '''Draw a full Graph Model with the computed values:

        Args:
            G(GraphModel): A graph model.
            inputs(dict): dictionnary of input values.
            parameters(dict): dictionnary of parameter values.

        Returns:
            dot(obj): The plot object of the graph.
        '''
        X = G.run(inputs_parameters)
        for node_id in X:
            G.nodes[node_id]['value'] = X[node_id]
        dot = self.draw(G)

        for node_id in X:  # Ugly, need to find better option for drawing
            del G.nodes[node_id]['value']

        return dot


class GraphParser():
    '''A class to parse the specification of a graph
    '''

    def __init__(self):
        '''
        Initialize a parser.
        '''
        return None

    def format_node(self, node):
        if 'computation' in node:
            formula = node['computation']
            computation_name = inspect.getsource(formula).split('**kwargs:')[-1].strip().strip('}')
            node['computation'] = {'formula': formula, 'name': computation_name}
            node['in'] = inspect.getfullargspec(formula).args

            return node

        else:
            return node

    def parse_node(self, raw_node):
        '''Parse a node.

        Args:
            raw_node(dict): raw node given in graph_specifications.

        Returns:
            node(node): A formatted non computationnal node.
        '''
        node = (raw_node['id'], {k: raw_node[k] for k in ('type', 'unit', 'name')})
        return node

    def parse_computational_node(self, raw_node):
        '''Parse a computationnal node.

        Args:
            raw_node(dict): raw node given in graph_specifications.

        Returns:
            node(node): A formatted computationnal node
        '''
        node_id = f"{raw_node['id']}_comp"
        node_param = {}
        node_param['formula'] = raw_node['computation']['formula']
        node_param['name'] = raw_node['computation']['name']
        node_param['out'] = raw_node['id']
        node_param['in'] = raw_node['in']
        node_param['type'] = 'computationnal'

        node = (node_id, node_param)

        return node

    def parse_computational_edges(self, comp_node):
        '''Parse edges from and to a computationnal node.

        Args:
            comp_node(dict): a computationnal node.

        Returns:
            edges(list): list of edges in the graph.
        '''
        edges = []
        for in_node in comp_node[1]['in']:
            edge = (in_node, comp_node[0])
            edges.append(edge)
        edges.append((comp_node[0], comp_node[0].split('_comp')[0]))
        return edges

    def parse(self, graph_specifications):
        '''Parse the graph specification

        Args:
            graph_specifications(dict): dict of nodes

        Returns:
            nodes(List): list of parsed nodes.
            egdes(List): list of parsed edges.
            summary_df(pd.DataFrame): DataFrame summarizing the graph
        '''

        graph_specifications = copy.deepcopy(graph_specifications)

        edges, nodes = [], []

        for node_id, raw_node in graph_specifications.items():
            raw_node['id'] = node_id

            # formats the node to match the previous framework.
            raw_node = self.format_node(raw_node)

            node = self.parse_node(raw_node)

            nodes.append(node)

            if 'computation' in raw_node:
                node = self.parse_computational_node(raw_node)
                nodes.append(node)

                comp_edges = self.parse_computational_edges(node)
                edges += comp_edges

        return nodes, edges, self.summary(graph_specifications)

    def summary(self, graph_specifications):
        '''Return a pandas dataframe to summarize the node of the graph as specified in the graph_specification.

        TO IMPROVE.
        '''
        summary_df = pd.DataFrame()

        for node_id, node in graph_specifications.items():

            node['id'] = node_id

            if 'computation' in node:
                comp = node['computation']['name']
            else:
                comp = np.nan

            row = pd.DataFrame({'name': node['name'], 'type': node['type'],
                                'unit': node['unit'], 'computation': comp}, index=[node['id']])
            summary_df = summary_df.append(row)

        summary_df.index.name = 'id'

        return summary_df


# Function composition

def compose(*functions):
    return reduce(lambda f, g: lambda x: f(g(X=x)), functions, lambda x: x)


def node_function(node, X):
    X = X.copy()
    function, out_node = node['formula'], node['out']
    X[out_node] = function(**X)
    return X


def model_function(G):
    '''The function computed by the model'''
    functions_list = [partial(node_function, node=G.nodes[node_id])
                      for node_id in G.node_ordering[::-1]]
    return compose(*functions_list)


# Node merging quite ugly now to improve, bugs when  same duplicated output
def get_duplicated_nodes(list_of_graph_specs):
    id_type_df = get_id_type_df(list_of_graph_specs)
    return id_type_df.loc[id_type_df.id.duplicated()].id.tolist()


def get_id_type_df(list_of_graph_specs):
    id_type_df = [[(d, node['type']) for d, node in graph_spec.items()]
                  for graph_spec in list_of_graph_specs]
    id_type_df = pd.DataFrame(sum(id_type_df, []), columns=['id', 'type']).drop_duplicates()
    return id_type_df


def get_nodes_df(node_list, node_id):
    nodes_df = pd.DataFrame(node_list)
    assert nodes_df[['unit', 'name']].drop_duplicates().shape[0] == 1, f'{node_id} has different name or unit across specifications'
    return nodes_df


def get_node_from_list_of_specs(node_id, list_of_graph_specs):
    node_list = [nodes[node_id] for nodes in list_of_graph_specs if node_id in nodes.keys()]
    return node_list


def merge_nodes(node_list, node_id):
    nodes_to_merge = get_nodes_df(node_list, node_id)      

    if 'variable' in nodes_to_merge.type.unique():
        computation = nodes_to_merge.dropna(subset=['computation']).computation.unique()[0]
        unit = nodes_to_merge.unit.unique()[0]
        name = nodes_to_merge.name.unique()[0]
        return {'name': name, 'type': 'variable', 'unit': unit, 'computation': computation}
    elif set(['input', 'output']) <= set(nodes_to_merge.type.unique()):
        computation = nodes_to_merge.dropna(subset=['computation']).computation.unique()[0]
        unit = nodes_to_merge.unit.unique()[0]
        name = nodes_to_merge.name.unique()[0]
        return {'name': name, 'type': 'variable', 'unit': unit, 'computation': computation}

    else:
        
        return nodes_to_merge.drop_duplicates().to_dict(orient='records')[0]


def concatenate_graph_specs(list_of_graph_specs):
    '''Concatenate a list of graph specifications.

    - Duplicated nodes are removed.
    - Nodes that are inputs in some and outputs in other becomes variables.
    '''

    concatenated_specs = {}
    for graph_specs in list_of_graph_specs:
        concatenated_specs.update(graph_specs)


    duplicated_nodes = get_duplicated_nodes(list_of_graph_specs)

    merged_nodes = {}

    for node_id in duplicated_nodes:
        nodes_to_merge = get_node_from_list_of_specs(node_id, list_of_graph_specs)
        merged_node = merge_nodes(nodes_to_merge, node_id)
        merged_nodes[node_id] = merged_node
            
    concatenated_specs.update(merged_nodes)

    return concatenated_specs


def merge_models(model_list):
    concatenated_spec = concatenate_graph_specs([model.graph_specifications for model in model_list])
    merged_model = GraphModel(concatenated_spec)
    return merged_model


def converte_to_format(old_nodes):
    
    '''To remove not usefull anymore'''
    new_nodes = {}

    for node in old_nodes:
        new_nodes[node['id']] = node.copy()

#         if 'computation' in node:
#             new_nodes[new_nodes['id']].pop('in', None)
#             new_nodes[new_nodes['id']].pop('computation', None)

        new_nodes[node['id']].pop('id', None)

        if 'computation' in node:
            new_nodes[node['id']]['computation'] = node['computation']['formula']
            new_nodes[node['id']].pop('in', None)
    return new_nodes
