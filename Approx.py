import networkx as nx
import sys
import time
from random import randint, seed

class Approx:
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

    def calc_vc(self, G, random_seed):
        seed(random_seed)
        c = []
        while nx.number_of_edges(G) != 0:
            edgesNum = nx.number_of_edges(G)
            rN = randint(0,edgesNum - 1)
            edges = list(G.edges())
            e = edges[rN]
            v1 = e[0]
            v2 = e[1]
            c.append(v1)
            c.append(v2)
            G.remove_node(v1)
            G.remove_node(v2)
        return c

    def check_vc(self, G, c):
        for e in list(G.edges()):
            if e[0] not in c and e[1] not in c:
                print(e)
                return False
        return True

    def main(self):

        num_args = len(sys.argv)

        if num_args < 2:
            print("error: not enough input arguments")
            exit(1)

        graph_file = sys.argv[1]
        random_seed = int(sys.argv[2])
        output_file = graph_file.split(".")[0]

        graph_file = "Data/Data/" + graph_file
        G = self.read_graph(graph_file)
        start_time = time.time()
        c = self.calc_vc(G, random_seed)
        total_time = time.time() - start_time

        output_sol = "Solutions/" + output_file + "_Approx_" + str(random_seed) + ".sol"
        output_trace = "Solutions/" + output_file + "_Approx_" + str(random_seed) + ".trace"

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


