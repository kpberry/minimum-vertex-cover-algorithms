from datetime import datetime, timedelta
from random import random, seed, choice

from graph_utils import read_graph
from vc import is_solution, eval_fitness


# TODO minimize num copies - use diffs
def get_neighbors(vc, graph, iterations=10, degree=1):
    for i in range(iterations):
        v = int(random() * len(vc))
        if v in graph:
            for u in graph[v]:
                if vc[u] == 0:
                    break
            else:
                vc[v] = 0
                yield vc


def get_neighbors2(vc, graph, iterations=1, degree=1):
    if is_solution(graph, vc):
        for i in range(iterations):
            copy = [v for v in vc]
            copy[int(random() * len(vc))] = 0
            yield copy
    else:
        ones = []
        zeroes = []
        for i in range(len(vc)):
            if vc[i] == 1:
                ones.append(i)
            else:
                zeroes.append(i)
        for i in range(iterations):
            copy = [v for v in vc]
            copy[choice(ones)] = 0
            copy[choice(zeroes)] = 1
            yield copy


def randomized_hill_climb(problem, get_neighbors, evaluate_fitness,
                          gen_model, filename, cutoff_time, random_seed):
    seed(random_seed)
    # will be used to determine when to restart
    stagnation_threshold = 50
    degree = 0
    best_so_far = None
    most_fit = model = gen_model(problem)

    smallest_vc = most_fit

    # this will be used to restart the search if improvements stop
    last_improvement = 0

    base = filename.split('/')[-1].split('.')[0] \
           + '_LS1_' + str(cutoff_time) + '_' \
           + str(random_seed)

    with open(base + '.trace', 'w') as trace:
        start_time = cur_time = datetime.now()

        while (cur_time - start_time) < timedelta(seconds=cutoff_time):
            # evaluate the fitness of the current model
            cur_fitness = prev_fitness = evaluate_fitness(problem, model)
            # if is_solution(problem, model):
            #     smallest_vc = min(smallest_vc, model, key=lambda k: sum(k))

            # get the model's neighbors in a random order
            neighbors = get_neighbors(model, problem, degree=degree)

            # update the current model if it has a neighbor with a better or
            # slightly worse fitness
            for n in neighbors:
                fitness = evaluate_fitness(problem, n)
                if fitness > prev_fitness:
                    if is_solution(problem, model) and \
                            (best_so_far is None or cur_fitness > best_so_far):
                        most_fit = model
                        # log results
                        trace.write('{:0.2f}'.format(
                            (cur_time - start_time).total_seconds()
                        ))
                        trace.write(',' + str(sum(smallest_vc)) + '\n')
                        print(sum(most_fit))
                    model = n
                    cur_fitness = fitness
                    break

            # keep track of whether or not the model improved
            cur_time = datetime.now()
            if cur_fitness > prev_fitness:
                last_improvement = 0
                degree = 1
            else:
                last_improvement += 1

            # if there has been no improvement for a while, randomly restart
            if last_improvement >= stagnation_threshold:
                stagnation_threshold += 1
                model = gen_model(problem)
                last_improvement = 0

    with open(base + '.sol', 'w') as sol:
        sol.write(str(sum(smallest_vc)) + '\n')
        sol.write(','.join([str(i + 1) for i in range(len(smallest_vc)) if
                            smallest_vc[i] == 1]))
    return most_fit


def run(filename, cutoff_time, random_seed):
    seed(random_seed)
    graph = read_graph(filename)
    randomized_hill_climb(graph, get_neighbors, eval_fitness,
                          lambda g: [1] * (max(graph) + 1),
                          filename, cutoff_time, random_seed)


if __name__ == '__main__':
    run('./data/Data/power.graph', 600, 0)
