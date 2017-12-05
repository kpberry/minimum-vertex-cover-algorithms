# Main executable file. Can be run with arguments of the form described in the
# assignment PDF.

import argparse

import approx
import branch_bound
import fastvc
import hill_climbing

if __name__ == '__main__':
    # Define the possible arguments.
    parser = argparse.ArgumentParser()
    parser.add_argument('-inst', type=str)
    parser.add_argument('-alg', type=str)
    parser.add_argument('-time', type=int)
    parser.add_argument('-seed', type=int)

    # Read the arguments
    args = parser.parse_args()
    inst = args.inst
    alg = args.alg
    time = args.time
    # Seed defaults to 0 and is ignored in approx and BnB
    if args.seed:
        seed = args.seed
    else:
        seed = 0

    # Run the specified algorithm.
    if alg == 'BnB':
        branch_bound.run(inst, time, seed)
    elif alg == 'Approx':
        approx.run(inst, time, seed)
    elif alg == 'LS1':
        hill_climbing.run(inst, time, seed)
    elif alg == 'LS2':
        fastvc.run(inst, time, seed)
    else:
        print('Invalid algorithm entered.')

    # Notify that the algorithm is done running
    print('Evaluation complete for ' + alg + ' on ' + inst
          + ' with ' + str(time) + ' seconds and a seed of ' + str(seed))
