import time

import pandas as pd

import examples
import linear_program as lp

times = []
start = 2
stop = 15
index = range(start, stop)



for n in index:
    t = time.clock()
    setup = examples.run_setup_n(n, times=True, setup=lp.setup_variable)
    t1 = time.clock() - t
    lp.run_variable(*setup)
    t2 = time.clock() - t1
    print str(n) + ': ' + str(t1) + ', ' + str(t2)
    times.append([t1, t2])

pd.DataFrame(times, index=index
             ).to_csv('output/times_{}_{}.csv'.format(start, stop-1))
