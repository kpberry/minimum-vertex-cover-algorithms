# File containing auxiliary approximation algorithms, including a networkx
# implementation of edge deletion, maximum degree greedy selection, and
# greedy independent cover selection.
# Assumes that data is located in the folder ./Data/
# Will not be used by main.py

import networkx as nx
import time
from random import randint, seed
import operator


class Approx:
    # Copy of the graph reading function from graph_utils.py
    def read_graph(self, filename):
        G = nx.Graph()
        with open(filename, "r") as inputfile:
            graph_data = inputfile.readline()
            i = 0
            for line in inputfile:
                i += 1
                node_data = list(map(lambda x: int(x), line.split()))
                for node in node_data:
                    G.add_edge(i, node)
        return G

    # Approximation algorithm which iteratively selects edges, adds the
    # endpoints to the vertex cover, then deletes the edge.
    def edge_deletion(self, G):
        seed(0)
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
        return c

    # Approximation algorithm that greedily selects the vertex of max degree in
    # the graph, then adds it and delets any of its outgoing edges.
    def maximum_degree_greedy(self, G):
        c = []
        while nx.number_of_edges(G) != 0:
            maxdegree = \
            sorted(G.degree_iter(), key=operator.itemgetter(1), reverse=True)[0]
            v = maxdegree[0]
            c.append(v)
            G.remove_node(v)
        return c

    # Approximation algorithm that greedily selects the vertex of min degree,
    # adds each of its neighbors to the vertex cover, then deletes the newly
    # covered edges.
    def greedy_independent_cover(self, G):
        c = []
        while nx.number_of_edges(G) != 0:
            mindegree = sorted(G.degree_iter(), key=operator.itemgetter(1))[0]
            v = mindegree[0]
            v_list = G.neighbors(v)
            c.extend(v_list)
            G.remove_node(v)
            G.remove_nodes_from(v_list)
        return c
    # Function which checks whether or not a set of vertices is a vertex cover
    def check_vc(self, G, c):
        for e in list(G.edges()):
            if e[0] not in c and e[1] not in c:
                print(e)
                return False
        return True

    # IO stuff
    def main(self):
        input_file_name = ["as-22july06.graph", "delaunay_n10.graph",
                           "email.graph", "football.graph", "hep-th.graph",
                           "jazz.graph", "karate.graph", "netscience.graph",
                           "power.graph", "star.graph", "star2.graph"]

        for graph_file in input_file_name:
            print(graph_file + " edge_deletion")
            random_seed = 0
            output_file = graph_file.split(".")[0]

            graph_file = "./Data/" + graph_file
            G = self.read_graph(graph_file)
            start_time = time.time()
            c = self.edge_deletion(G)
            total_time = time.time() - start_time

            output_sol = "Solutions/edge_deletion/" + output_file + "_Approx_" + str(
                random_seed) + ".sol"
            output_trace = "Solutions/edge_deletion/" + output_file + "_Approx_" + str(
                random_seed) + ".trace"

            output1 = open(output_sol, 'w')
            output1.write(str(len(c)) + "\n")
            output1.write(",".join(str(v) for v in c))
            output1.close()

            output2 = open(output_trace, 'w')
            output2.write(str(total_time) + "," + str(len(c)))

        for graph_file in input_file_name:
            random_seed = 0
            output_file = graph_file.split(".")[0]
            print(graph_file + " MDG")
            graph_file = "Data/" + graph_file
            G = self.read_graph(graph_file)
            start_time = time.time()
            c = self.maximum_degree_greedy(G)
            total_time = time.time() - start_time

            output_sol = "Solutions/maximum_degree_greedy/" + output_file + "_Approx_" + str(
                random_seed) + ".sol"
            output_trace = "Solutions/maximum_degree_greedy/" + output_file + "_Approx_" + str(
                random_seed) + ".trace"

            output1 = open(output_sol, 'w')
            output1.write(str(len(c)) + "\n")
            output1.write(",".join(str(v) for v in c))
            output1.close()

            output2 = open(output_trace, 'w')
            output2.write(str(total_time) + "," + str(len(c)))

        for graph_file in input_file_name:
            random_seed = 0
            output_file = graph_file.split(".")[0]
            print(graph_file + " GIC")
            graph_file = "Data/" + graph_file
            G = self.read_graph(graph_file)
            start_time = time.time()
            c = self.greedy_independent_cover(G)
            total_time = time.time() - start_time

            output_sol = "Solutions/greedy_independent_cover/" + output_file + "_Approx_" + str(
                random_seed) + ".sol"
            output_trace = "Solutions/greedy_independent_cover/" + output_file + "_Approx_" + str(
                random_seed) + ".trace"

            output1 = open(output_sol, 'w')
            output1.write(str(len(c)) + "\n")
            output1.write(",".join(str(v) for v in c))
            output1.close()

            output2 = open(output_trace, 'w')
            output2.write(str(total_time) + "," + str(len(c)))


if __name__ == '__main__':
    # run the experiments
    runexp = Approx()
    runexp.main()