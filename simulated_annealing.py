from math import exp
from random import random, shuffle


def default_switch_prob(current, candidate, t):
    return 1 if candidate > current else exp(-(current - candidate) / t)


def default_temperature(k):
    return 0.000001 * exp(-k ** 2)


def simulate_annealing(problem, model, get_neighbors, evaluate_fitness,
                       temperature=default_temperature,
                       switch_prob=default_switch_prob, iterations=100):
    cur_fitness = evaluate_fitness(problem, model)
    for i in range(iterations):
        t = temperature(i / iterations)
        neighbors = get_neighbors(model)
        shuffle(neighbors)
        fitnesses = [cur_fitness]
        for n in neighbors:
            fitness = evaluate_fitness(problem, n)
            fitnesses.append(fitness)
            if switch_prob(cur_fitness, fitness, t) >= random():
                model = n
                cur_fitness = fitness
                break
    return model
