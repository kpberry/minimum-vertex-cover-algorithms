# -*- coding: utf-8 -*-
"""
Created on Sat Nov 11 08:57:01 2017

@author: Mostafa Reisi
"""
from datetime import datetime, timedelta
from random import seed, randint

import networkx as nx
import pulp as lp

from graph_utils import read_graph

#TODO use greedy vc as starting point
class BranchBound(object):
    def __init__(self, graph, remaining_vertices, used_vertices, vc_size):
        self.graph = graph
        # NetworkX returns this as a NodeView, which is bad
        self.used_vertices = list(used_vertices)
        self.remaining_vertices = list(remaining_vertices)
        self.vc_size = vc_size
        if self.graph.number_of_nodes() > 5000:
            self.lb = self.get_lower_bound_approx(graph.copy(), 0)
        else:
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
                                      self.used_vertices,
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
                                     self.used_vertices
                                     + [self.remaining_vertices[-1]],
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
            result = self.vc_size - 1
        return result


    def get_lower_bound_approx(self, G, random_seed):
        c = []
        while nx.number_of_edges(G) != 0:
            edgesNum = nx.number_of_edges(G)
            rN = randint(0, edgesNum - 1)
            edges = list(G.edges())
            e = edges[rN]
            v1 = e[0]
            v2 = e[1]
            c.append(v1)
            c.append(v2)
            G.remove_node(v1)
            G.remove_node(v2)
        len(c) / 2 + self.vc_size


def run(filename, cutoff_time, random_seed):
    seed(random_seed)
    # generate a graph
    graph = nx.Graph()
    # convert the input graph into an nx graph
    input_graph = read_graph(filename)
    graph.add_nodes_from([i for i in input_graph])
    for j in input_graph:
        graph.add_edges_from([(j, i) for i in input_graph[j]])

    root = BranchBound(graph, graph.nodes(), [], 0)
    frontier = []
    frontier.extend([root])
    cur_solution_size = graph.number_of_nodes()
    start_time = datetime.now()
    best = BranchBound(graph, graph.nodes(), [], graph.number_of_nodes())
    best_is_set = False
    base = filename.split('/')[-1].split('.')[0] \
           + '_BnB_' + str(cutoff_time) + '_' \
           + str(random_seed)
    with open(base + '.trace', 'w') as trace:
        while len(frontier) > 0 and datetime.now() - start_time < timedelta(
                seconds=cutoff_time):
            frontier.sort(key=lambda x: x.lb)
            current = frontier.pop()
            cur_children = current.expand()
            if not cur_children:
                if not current.graph.nodes():
                    if cur_solution_size > current.vc_size:
                        cur_solution_size = current.vc_size
                        best = current
                        best_is_set = True
            else:
                frontier.extend(cur_children)

            frontier = [el for el in frontier if el.lb < cur_solution_size]

            trace.write('{:0.2f}'.format(
                (datetime.now() - start_time).total_seconds()
            ))
            trace.write(',' + str(cur_solution_size) + '\n')

    with open(base + '.sol', 'w') as sol:
        sol.write(str(best.vc_size) + '\n')
        sol.write(','.join([str(i + 1) for i in sorted(best.used_vertices)]))
