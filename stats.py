# File for computing the relative errors for all of the generated output

import os


def gen_rel_errors(algos):
    names = ['jazz', 'karate', 'football', 'as-22july06', 'hep-th',
             'star', 'star2', 'netscience', 'email', 'delaunay', 'power']
    opts = [158, 14, 94, 3303, 3926, 6902, 4542, 899, 594, 703, 2203]
    names, opts = list(zip(*sorted(list(zip(names, opts)))))

    for algo in algos:
        print(algo)
        counts = [0] * len(names)
        vc_vals = [0] * len(names)
        rel_errs = [0] * len(names)

        # get the quality of the solution and increment the solution count for
        # the algorithm with the given name
        for filename in sorted(os.listdir(algo)):
            if '.sol' in filename:
                i = list(names).index(filename.split('_')[0])
                with open(algo + '/' + filename, 'r') as file:
                    vc_vals[i] += int(file.readline().split(',')[0])
                    counts[i] += 1

        # Compute the relative errors
        for i in range(len(vc_vals)):
            vc_vals[i] /= counts[i]
            rel_errs[i] = (vc_vals[i] - opts[i]) / opts[i]

        # Output the results
        for i in range(len(names)):
            print(names[i])
            print('VC Value', vc_vals[i], 'RelErr', rel_errs[i])
        print()


if __name__ == '__main__':
    gen_rel_errors(['BnB', 'LS1', 'LS2', 'Approx'])
