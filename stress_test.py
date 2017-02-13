import time

import pandas as pd

import examples
import linear_program as lp

times = []
start = 30
stop = 31
index = range(start, stop)


for n in index:
    t = time.clock()
    setup = examples.run_setup_n(n, setup=lp.setup_variable_integer)
    t1 = time.clock() - t
    lp.run_variable_integer(*setup)
    t2 = time.clock() - t1 - t
    print str(n) + ': ' + str(t1) + ', ' + str(t2)
    times.append([t1, t2])
pd.DataFrame(times, index=index
             ).to_csv('output/times_{}_{}.csv'.format(start, stop-1))
