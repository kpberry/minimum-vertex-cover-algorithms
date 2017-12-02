from datetime import datetime, timedelta
from random import random, seed, choice

from graph_utils import read_graph
from vc import is_solution, eval_fitness


def get_close_neighbor(vc, graph, iterations=5000):
    for i in range(iterations):
        v = int(random() * len(vc))
        if v in graph and vc[v] == 1:
            for u in graph[v]:
                if vc[u] == 0:
                    break
            else:
                copy = [u for u in vc]
                copy[v] = 0
                return copy
    return None


def get_neighbors(vc, graph, graph_is_solution, iterations=10, degree=2):
    if graph_is_solution:
        for i in range(iterations):
            copy = [v for v in vc]
            for i in range(int(random() * degree) + 1):
                copy[int(random() * len(vc))] = 0
            yield copy
    else:
        zeroes = [i for i in range(len(vc)) if vc[i] == 1]
        for i in range(iterations):
            copy = [v for v in vc]
            for i in range(int(random() * degree) + 1):
                copy[choice(zeroes)] = 1
            yield copy


def randomized_hill_climb(problem, gen_model, filename, cutoff_time,
                          random_seed):
    seed(random_seed)
    degree = 0
    most_fit = model = gen_model(problem)
    best_so_far = fitness = eval_fitness(problem, model)

    base = filename.split('/')[-1].split('.')[0] \
           + '_LS1_' + str(cutoff_time) + '_' \
           + str(random_seed)

    model_is_solution = is_solution(problem, model)

    with open(base + '.trace', 'w') as trace:
        start_time = cur_time = datetime.now()

        while (cur_time - start_time) < timedelta(seconds=cutoff_time):
            neighbor = get_close_neighbor(model, problem)

            if neighbor is not None and model_is_solution:
                model = neighbor
                if random() > 0.99:
                    fitness = eval_fitness(problem, neighbor)
                    best_so_far = max(best_so_far, fitness)
                if sum(neighbor) < sum(most_fit):
                    most_fit = model
                    # log results
                    trace.write('{:0.2f}'.format(
                        (cur_time - start_time).total_seconds()
                    ))
                    trace.write(',' + str(sum(most_fit)) + '\n')
            else:
                # get the model's neighbors in a random order
                neighbors = get_neighbors(model, problem, model_is_solution,
                                          degree=degree)

                # update the current model if it has a neighbor with a better or
                # slightly worse fitness
                for n in neighbors:
                    fitness = eval_fitness(problem, n)
                    if fitness > best_so_far * random():
                        model = n
                        model_is_solution = is_solution(problem, model)
                        if fitness > best_so_far and model_is_solution:
                            best_so_far = fitness
                            most_fit = model
                            # log results
                            trace.write('{:0.2f}'.format(
                                (cur_time - start_time).total_seconds()
                            ))
                            trace.write(',' + str(sum(most_fit)) + '\n')
                        break
            print(sum(most_fit), sum(model), fitness, best_so_far,
                  model_is_solution)

            # keep track of whether or not the model improved
            cur_time = datetime.now()

    with open(base + '.sol', 'w') as sol:
        sol.write(str(sum(most_fit)) + '\n')
        sol.write(','.join([str(i + 1) for i in range(len(most_fit)) if
                            most_fit[i] == 1]))
    assert (is_solution(problem, most_fit))
    return most_fit


def run(filename, cutoff_time, random_seed):
    seed(random_seed)
    graph = read_graph(filename)
    randomized_hill_climb(graph,
                          lambda g: [1] * (max(graph) + 1),
                          # construct_vc,
                          filename, cutoff_time, random_seed)


if __name__ == '__main__':
    run('./data/Data/star.graph', 600, 0)
