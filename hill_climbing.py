from datetime import datetime, timedelta
from random import random, shuffle, seed

from approx import greedy_vc
from graph_utils import read_graph
from vc import is_solution, get_neighbors, eval_fitness


def randomized_hill_climb(problem, get_neighbors, evaluate_fitness,
                          gen_model, filename, cutoff_time, random_seed):
    seed(random_seed)
    # will be used to determine when to restart
    restart_threshold = 10
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
            fitnesses = [prev_fitness]
            if is_solution(problem, model):
                smallest_vc = min(smallest_vc, model, key=lambda k: sum(k))

            # get the model's neighbors in a random order
            neighbors = get_neighbors(model, problem)
            shuffle(neighbors)

            # update the current model if it has a neighbor with a better or
            # slightly worse fitness
            for n in neighbors:
                fitness = evaluate_fitness(problem, n)
                fitnesses.append(fitness)
                if fitness > prev_fitness + random() - 0.1:
                    model = n
                    cur_fitness = fitness
                    break

            # keep track of the best model so far
            if best_so_far is None or max(fitnesses) > best_so_far:
                best_so_far = max(fitnesses)
                most_fit = model

            # keep track of whether or not the model improved
            if cur_fitness > prev_fitness:
                last_improvement = 0
            else:
                last_improvement += 1

            # if there has been no improvement for a while, randomly restart
            if last_improvement >= restart_threshold:
                restart_threshold += 1
                model = gen_model(problem)
                last_improvement = 0

            cur_time = datetime.now()
            # log results
            trace.write('{:0.2f}'.format(
                (cur_time - start_time).total_seconds()
            ))
            trace.write(',' + str(sum(smallest_vc)) + '\n')
        with open(base + '.sol', 'w') as sol:
            sol.write(str(sum(smallest_vc)) + '\n')
            sol.write(','.join([str(i + 1) for i in range(len(smallest_vc)) if
                                smallest_vc[i] == 1]))
    return most_fit


def run(filename, cutoff_time, random_seed):
    seed(random_seed)
    graph = read_graph(filename)
    randomized_hill_climb(graph, get_neighbors, eval_fitness, greedy_vc,
                          filename, cutoff_time, random_seed)
