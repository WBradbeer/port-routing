import time

import pandas as pd

import examples
import linear_program as lp

times = []
start = 2
stop = 14
index = range(start, stop)

import matlab.engine
eng = matlab.engine.start_matlab()

for n in index:
    t = time.clock()
    setup = examples.run_setup_n(n, times=True, setup=lp.setup_fixed)
    t1 = time.clock() - t
    print sum(lp.run_times_matlab(*setup))
    t2 = time.clock() - t1
    print str(n) + ': ' + str(t1) + ', ' + str(t2)
    times.append([t1, t2])

pd.DataFrame(times, index=index
             ).to_csv('output/times_{}_{}.csv'.format(start, stop-1))
