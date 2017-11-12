import os
from contextlib import suppress
from datetime import datetime, timedelta
from random import sample

import numpy as np


def simulate_genetics(problem, model, evaluate_fitness, gen_model,
                      crossover, mutation, num_models=100,
                      dynamic_population=False, max_models=1500,
                      out_dir='./out/'):
    # make the output directory
    with suppress(FileExistsError):
        os.mkdir(out_dir)
    out_dir += 'ga.csv'

    most_fit = model

    # these will be used to determine if the exploration rate is too slow
    last_improvement = 0
    best_so_far = None

    # TODO increase the number of models when the improvement rate slows a lot
    with open(out_dir, 'w') as out:
        out.write('mean_fitness,min_fitness,max_fitness,time,stddev_fitness\n')
        start_time = cur_time = datetime.now()

        # generate the initial population
        models = [gen_model(problem) for _ in range(num_models)]

        while (cur_time - start_time) < timedelta(minutes=10):
            # calculate the fitness of each model
            fitnesses = [(m, evaluate_fitness(problem, m)) for m in models]
            fitnesses = sorted(fitnesses, key=lambda s: s[1], reverse=True)

            most_fit, max_fitness = fitnesses[0]

            # get the parents - 2 random models and the best 30% of the others
            parents = sample(models, 2)
            parents += [mf[0] for mf in fitnesses[:int(num_models * 0.3)]]

            # keep the best model
            models = [most_fit]
            # add the offspring of the parents
            models += [
                mutation(crossover(*sample(parents, 2), problem), problem)
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

            # log results
            fitnesses = [f[1] for f in fitnesses]
            out.write(str(np.mean(fitnesses)) + ',')
            out.write(str(min(fitnesses)) + ',')
            out.write(str(max(fitnesses)) + ',')
            out.write(str(datetime.now() - cur_time) + ',')
            out.write(str(np.std(fitnesses)) + '\n')
            cur_time = datetime.now()
            print(cur_time - start_time)
            print('Max fitness:', max(fitnesses))
    return most_fit
