import os
from random import random

import matplotlib.pyplot as plt


def gen_averages(algos):
    names = ['jazz', 'karate', 'football', 'as-22july06', 'hep-th',
             'star', 'star2', 'netscience', 'email', 'delaunay', 'power']
    opts = [158, 14, 94, 3303, 3926, 6902, 4542, 899, 594, 703, 2203]
    names, opts = list(zip(*sorted(list(zip(names, opts)))))

    for algo in algos:
        print(algo)
        counts = [0] * len(names)
        vc_vals = [0] * len(names)
        rel_errs = [0] * len(names)

        for filename in sorted(os.listdir(algo)):
            if '.sol' in filename:
                i = list(names).index(filename.split('_')[0])
                with open(algo + '/' + filename, 'r') as file:
                    vc_vals[i] += int(file.readline().split(',')[0])
                    counts[i] += 1

        for i in range(len(vc_vals)):
            vc_vals[i] /= counts[i]
            rel_errs[i] = (vc_vals[i] - opts[i]) / opts[i]

        for i in range(len(names)):
            print(names[i])
            print('VC Value', vc_vals[i], 'RelErr', rel_errs[i])
        print()


def gen_qrtds(algos):
    names = ['jazz', 'karate', 'football', 'as-22july06', 'hep-th',
             'star', 'star2', 'netscience', 'email', 'delaunay', 'power']
    opts = [158, 14, 94, 3303, 3926, 6902, 4542, 899, 594, 703, 2203]
    percents = [1 + 0.5 ** i for i in range(11)]
    times = [i / 10 for i in range(51)]
    run_values = {name: [[] for _ in range(len(names))] for name in names}
    run_times = {name: [[] for _ in range(len(names))] for name in names}

    for algo in algos:
        print(algo)

        for filename in sorted(os.listdir(algo)):
            if '.trace' in filename:
                name = filename.split('_')[0]
                i = int(str(filename.split('_')[-1]).split('.')[0])
                with open(algo + '/' + filename, 'r') as file:
                    for line in file:
                        t, vc_val = line.split(',')
                        run_times[name][i].append(float(t))
                        run_values[name][i].append(int(vc_val))

    for name in run_values:
        gen_qrtd(run_values[name], run_times[name], opts[names.index(name)],
                 percents, times)


def gen_qrtd(run_values, run_times, opt, percents, times):
    counts = [[0] * len(times) for _ in range(len(percents))]
    for p in range(len(percents)):
        for run in range(len(run_values)):
            for ti, time in enumerate(times):
                for i in range(len(run_values[run])):
                    if run_times[run][i] >= time:
                        if run_values[run][i] < percents[p] * opt:
                            counts[p][ti] += 1
                        break
    print(counts)
    plt.plot(times, list(zip(*counts)))
    plt.show()


if __name__ == '__main__':
    gen_averages(['LS1'])
    # gen_qrtds(['LS1'])
