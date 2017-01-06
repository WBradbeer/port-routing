import time

import pandas as pd

import examples

times = []
start = 2
stop = 10
index = range(start, stop)



for n in index:
    t = time.clock()
    examples.run_lp_n(n)
    times.append(time.clock() - t)

pd.DataFrame(times,index=index
             ).to_csv('times_{}_{}.csv'.format(start, stop-1))
