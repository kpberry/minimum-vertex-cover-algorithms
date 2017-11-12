import os
from contextlib import suppress
from datetime import datetime, timedelta
from random import random, shuffle

import numpy as np


def randomized_hill_climb(problem, model, get_neighbors, evaluate_fitness,
                          gen_model, out_dir='./out/'):
    # make the output directory
    with suppress(FileExistsError):
        os.mkdir(out_dir)
    out_dir += 'rhc.csv'

    # will be used to determine when to restart
    restart_threshold = 10
    best_so_far = None
    most_fit = None

    # this will be used to restart the search if improvements stop
    last_improvement = 0

    with open(out_dir, 'w') as out:
        out.write('mean_fitness,min_fitness,max_fitness,time,stddev_fitness\n')
        start_time = cur_time = datetime.now()

        while (cur_time - start_time) < timedelta(minutes=10):
            # evaluate the fitness of the current model
            cur_fitness = prev_fitness = evaluate_fitness(problem, model)
            fitnesses = [prev_fitness]

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
            if best_so_far is None or np.max(fitnesses) > best_so_far:
                best_so_far = np.max(fitnesses)
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

            # output results
            out.write(str(np.mean(fitnesses)) + ',')
            out.write(str(np.min(fitnesses)) + ',')
            out.write(str(np.max(fitnesses)) + ',')
            out.write(str(datetime.now() - start_time) + ',')
            out.write(str(np.std(fitnesses)) + '\n')
            cur_time = datetime.now()
            print(cur_time - start_time)
            print('Max fitness:', np.max(fitnesses))
            print('Best so far:', best_so_far)
    return most_fit
