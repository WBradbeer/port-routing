import time

import pandas as pd

import examples
import linear_program as lp

times = []
start = 100
stop = 200
index = range(start, stop)


for n in index:
    t = time.clock()
    tr = time.time()
    setup = examples.run_gurobi_setup_n(n)
    t1 = time.clock() - t
    lp.run_gurobi(*setup)
    t2 = time.clock() - t1 - t
    tr2 = time.time() - tr
    print str(n) + ': ' + str(t1) + ', ' + str(t2) + ', ' + str(tr2)
    times.append([t1, t2, tr2])

pd.DataFrame(times, index=index
             ).to_csv('output/times_{}_{}.csv'.format(start, stop-1))
