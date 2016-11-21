import time

import pandas as pd

import examples

times = []
start = 2
stop = 20
index = range(start, stop)

for n in index:
    t = time.clock()
    examples.run_example_n(n)
    times.append(time.clock() - t)

pd.DataFrame(times,index=index
             ).to_csv('times_{}_{}.csv'.format(start, stop-1))
