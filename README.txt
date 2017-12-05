In order to run this code, you will need to install python3 and networkx.

Our main executable is main.py and can be run as follows:

    python3 main.py -inst <Path to instance> -alg <Approx | BnB | LS1 | LS2> -time <Cutoff time> -seed <Integer seed value>

The code for our approximation algorithms can be found in approx.py. By default,
the MG (modified greedy) algorithm will be run.

Our branch and bound code is in branch_bound.py.

Our code for the FastVC local search algorithm (LS1) can be found in fastvc.py.

The code for our variation on randomized hill climbing can be found in
hill_climbing.py.

Utility functions for graphs, vertex covers, and relative error computation can
be found in graph_utils.py, vc.py, and stats.py, respectively.