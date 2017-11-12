# -*- coding: utf-8 -*-
"""
Created on Sat Nov 11 08:57:01 2017

@author: Mostafa Reisi
"""
import networkx as nx
import pip

from graph_utils import read_graph

pip.main(['install', 'pulp'])
import pulp as lp

from numpy import inf


class BranchBound(object):
    def __init__(self, graph, remaining_vertices, vc_size):
        self.graph = graph
        # NetworkX returns this as a NodeView, which is bad
        self.remaining_vertices = list(remaining_vertices)
        self.vc_size = vc_size
        self.lb = self.get_lower_bound()

    def get_pruned_graph(self, node):
        # Copy the graph and return the modified copy
        graph = self.graph.copy()
        graph.remove_node(node)
        # Have to put this in a list to prevent modification of a lazy iterator
        isolates = list(nx.isolates(graph))
        graph.remove_nodes_from(isolates)
        return graph

    def expand(self):
        if len(self.remaining_vertices) > 0:
            # the right child - not include selected vertex in the set
            # self.remaining_vertices[:-1] makes a copy of the first n - 1
            #   remaining vertices instead of passing around the original list
            right_child = BranchBound(self.graph.copy(),
                                      self.remaining_vertices[:-1],
                                      self.vc_size)
            # prune the graph. self.remaining_vertices[-1] gets the last
            # vertex in the remaining_vertices
            pruned_graph = self.get_pruned_graph(self.remaining_vertices[-1])
            pruned_vertices = set(pruned_graph.nodes())
            # make sure that we only use remaining vertices after pruning
            remaining_pruned_vertices = list(
                pruned_vertices.intersection(self.remaining_vertices[:-1])
            )
            # left child - include the selected node in the set
            left_child = BranchBound(pruned_graph,
                                     remaining_pruned_vertices,
                                     self.vc_size + 1)
            return [left_child, right_child]
        else:
            return []

    def get_lower_bound(self):
        # solve a linear programming to find the lowerbound
        graph = self.graph  # we use this graph to set up a LP problem
        nodes = graph.nodes()
        edges = graph.edges()
        if nodes:
            prob = lp.LpProblem('VC', lp.LpMinimize)
            x = lp.LpVariable.dict('x', nodes, lowBound=0)
            prob += sum(x[i] for i in nodes)
            for e in edges:
                prob += (x[e[0]] + x[e[1]] >= 1)
            for n in nodes:
                if n not in self.remaining_vertices:
                    prob += (x[n] <= 0)
            # solve the problem
            result = prob.solve()
        else:
            result = self.vc_size
        return result


def run(filename):
    # generate a graph
    graph = nx.Graph()
    # convert the input graph into an nx graph
    input_graph = read_graph(filename)
    graph.add_nodes_from([i for i in input_graph])
    for j in input_graph:
        graph.add_edges_from([(j, i) for i in input_graph[j]])

    root = BranchBound(graph, graph.nodes(), 0)
    frontier = []
    frontier.extend([root])
    cur_solution_size = inf
    while len(frontier) > 0:
        frontier.sort(key=lambda x: x.lb, reverse=True)
        current = frontier.pop()
        cur_children = current.expand()
        if not cur_children:
            cur_solution_size = current.vc_size
        else:
            frontier.extend(cur_children)

        frontier = [el for el in frontier if el.lb < cur_solution_size]

        print(cur_solution_size)


if __name__ == '__main__':
    run('./data/Data/karate.graph')
