import time

import examples
import linear_program as lp

times = []
ports = 5
scanner_lb = 10
scanner_ub = 11
scanner_range = range(scanner_lb, scanner_ub+1)

import matlab.engine
eng = matlab.engine.start_matlab()

t = time.clock()
setup = examples.run_setup_n(ports, setup=lp.setup_variable_integer)
t1 = time.clock() - t
print lp.run_variable_integer(*setup, scanner_range=scanner_range)
t2 = time.clock() - t1 - t
print 'Time: ' + str(t1) + ', ' + str(t2)
