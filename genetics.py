from datetime import datetime, timedelta
from random import sample, seed, choice

# TODO switch to networkx
from approx import greedy_vc
from graph_utils import read_graph
from vc import is_solution, eval_fitness, crossover, mutation


def simulate_genetics(problem, evaluate_fitness, gen_model, crossover,
                      mutation, filename, cutoff_time, num_models=100,
                      dynamic_population=False, max_models=1500, random_seed=0):
    seed(random_seed)
    most_fit = gen_model(problem)

    # these will be used to determine if the exploration rate is too slow
    last_improvement = 0
    smallest_vc = most_fit
    best_so_far = None

    base = filename.split('/')[-1].split('.')[0] \
           + '_LS2_' + str(cutoff_time) + '_' \
           + str(random_seed)
    # TODO increase the number of models when the improvement rate slows a lot
    with open(base + '.trace', 'w') as trace:
        start_time = cur_time = datetime.now()

        # generate the initial population
        models = [gen_model(problem) for _ in range(num_models)]

        while (cur_time - start_time) < timedelta(seconds=cutoff_time):
            # calculate the fitness of each model
            fitnesses = [(m, evaluate_fitness(problem, m)) for m in models]
            fitnesses = sorted(fitnesses, key=lambda s: s[1], reverse=True)

            most_fit, max_fitness = fitnesses[0]
            smallest_vc = min(smallest_vc, min([i for i in models if
                                                is_solution(problem, i)],
                                               key=lambda k: sum(k)),
                              key=lambda k: sum(k))

            # get the parents - 2 random models and the best 30% of the others
            parents = sample(models, 2)
            parents += [mf[0] for mf in fitnesses[:int(num_models * 0.3)]]

            # keep the best model
            models = [most_fit]
            # add the offspring of the parents

            models += [
                mutation(crossover(choice(parents), choice(parents), problem),
                         problem)
                for _ in range(num_models - len(models))
            ]
            # make sure we have the correct number of models
            assert num_models == len(models)

            # change the population size if the size is dynamic
            if dynamic_population:
                # update the best seen model and last improvement time
                if best_so_far is None or max_fitness > best_so_far + 1:
                    best_so_far = max_fitness
                    last_improvement -= 1
                else:
                    last_improvement += 1

                # if there hasn't been improvement in a while, increase the
                # population size by 2 or more to broaden the search space
                if last_improvement >= 5 and num_models < max_models:
                    increase = max(2, int(0.4 * num_models))
                    increase = min(1500 - num_models, increase)
                    num_models += increase
                    print('Stagnating. Increasing model pool size by '
                          + str(increase) + '.')
                    last_improvement = 0
                # if there have been a lot of improvements recently, decrease
                # the population size to narrow the search space and speed up
                # the search
                elif last_improvement <= -5 and num_models > 3:
                    decrease = max(1, int(0.05 * num_models))
                    num_models -= decrease
                    print('Accelerating. Decreasing model pool size by '
                          + str(decrease) + '.')
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
    simulate_genetics(graph, eval_fitness, greedy_vc,
                      crossover, mutation, filename, cutoff_time,
                      num_models=3, dynamic_population=True,
                      max_models=1000, random_seed=random_seed)
