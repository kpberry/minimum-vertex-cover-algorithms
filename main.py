import argparse

import branch_bound

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-inst', type=str, nargs=1)
    parser.add_argument('-alg', type=str, nargs=1)
    parser.add_argument('-time', type=int, nargs=1)
    parser.add_argument('-seed', type=int, nargs=1)

    args = parser.parse_args()
    inst = args.inst[0]
    alg = args.alg[0]
    time = args.time[0]
    seed = args.seed[0]

    print(alg)
    if alg == 'BnB':
        branch_bound.run(inst, time, seed)
    elif alg == 'Approx':
        pass
    elif alg == 'LS1':
        pass
    elif alg == 'LS2':
        pass
    else:
        print('Invalid algorithm entered.')