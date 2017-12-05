In order to run this code, you will need to install python3 and networkx.

Our main executable is main.py and can be run as follows:

python3 main.py -inst <filename> -alg <Approx|Approx2|Approx3|Approx4|BnB|LS1|LS2> -time <cutoff in seconds> -seed <random seed>

This will produce the appropriate output corresponding to the provided instance,
algorithm, cutoff time, and random seed.

The code for our main approximation algorithms can be found in approx.py.
This includes our modified greedy algorithm and our fast implementation of
edge deletion; modified greedy corresponds to the Approx alg input.

The code for our extra approximation algorithms ED, MDG, and GIC can be found
in approx2.py, and correspond to the arguments Approx2, Approx3, and Approx4
respectively. Note that the random seed and cutoff time is ignored for these
algorithms because they are extra.

Our branch and bound (BnB) code is in branch_bound.py.

Our code for the FastVC local search algorithm (LS1) can be found in fastvc.py.

The code for our variation on randomized hill climbing (LS2) can be found in
hill_climbing.py.

Utility functions for graphs, vertex covers, and relative error computation can
be found in graph_utils.py, vc.py, and stats.py, respectively.

We have written several bash files which will run each of the algorithms in
batches. run_approx_tests will run all 4 of the different approximation
algorithms in sequence.