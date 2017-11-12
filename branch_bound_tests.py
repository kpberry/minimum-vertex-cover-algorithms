# -*- coding: utf-8 -*-
"""
Created on Sat Nov 11 08:57:01 2017

@author: Mostafa Reisi
"""
import networkx as nx
#import pip

#pip.main(['install', 'pulp'])
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
            self.remaining_vertices.sort(key=lambda x: self.graph.degree(x))
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
            result = self.vc_size - 1 # when node is zero we set the lower bound one smaller than the solution
        return result


def read_graph(filename):
    # reads the graph as a sparse adjacency matrix from a file
    graph = {}
    with open(filename, 'r') as file:
        file.readline()
        for i, line in enumerate(file):
            if len(line.strip()) > 0:
                # 1 indexing because this is matlab apparently
                graph[i] = set(int(i) - 1 for i in line.split())
    return graph



graph = nx.Graph()
nodes =  list(range(0, 7))
graph.add_nodes_from(nodes)
graph.add_edges_from([(0,1),(1,2), (2, 3), (2, 4), (3, 4), (3, 5), (3, 6) , (4, 5)])
#graph.add_edges_from([(0,1),(1,2), (2, 3), (3, 4), (3, 5), (3, 6), (4, 5) , (4, 6), (5, 6)])
#graph.add_edges_from([(0,1),(0,2), (0, 3), (0, 4), (0, 5), (0, 6)])
root = BranchBound(graph, graph.nodes(), 0)
frontier = []
frontier.extend([root])
cur_solution_size = inf
while len(frontier) > 0:
    frontier.sort(key=lambda x: x.lb, reverse=True)
    current = frontier.pop()
    cur_children = current.expand()
    if not cur_children:
        if not current.graph.nodes():
            if cur_solution_size > current.vc_size:
                cur_solution_size = current.vc_size
    else:
        frontier.extend(cur_children)

    frontier = [el for el in frontier if el.lb < cur_solution_size]

    print(cur_solution_size)
