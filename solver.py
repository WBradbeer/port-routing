from copy import copy
import json

import numpy as np
import pandas as pd

import linear_program as lp


SOLVERS = {
    'gurobi': (lp.setup_gurobi, lp.run_gurobi),
}


def solve(data, solver='gurobi'):
    setup = SOLVERS[solver][0]
    run = SOLVERS[solver][1]
    return run(*setup(**data))


def get_data_from_path(path, prob_num=1):
    port_info = pd.read_csv(path + "foreign_port_info.csv",
                            index_col="Port")
    c_sent = port_info["Containers"]
    p_capacity = port_info["Capacity"]
    c_received = pd.read_csv(path + "containers_received.csv",
                                  index_col="Port")["Containers"]
    s_ports = list(port_info.index)

    distances = pd.read_csv(path + "port_costs.csv",
                            index_col="Port")
    source = len(s_ports)
    dest = len(c_received)
    sps = range(0, source)
    dp = range(source, source + dest)
    cost_f = distances[sps][:-dest]
    cost_d = distances[dp][:-dest]

    problem = json.load(open(path+ "problem{}.json".format(prob_num)))

    s_capacity = problem['scanner_capacity']
    return {
        'cost_f': cost_f,
        'cost_d': cost_d,
        'containers_sent': c_sent,
        'port_capacities': p_capacity,
        'dest_capacities': c_received,
        'scanner_capacity': s_capacity,
    }


def solve_varying_data(data, varying, values, solver='gurobi'):
    o_data = copy(data[varying])
    for val in values:
        data[varying] = o_data * val
        yield solve(data, solver)

def solve_noisy_data(data, varying, stdev, replications, solver='gurobi'):
    o_data = copy(data[varying])
    for i in range(0, replications):
        data[varying] = o_data.add(np.random.randn(*o_data.shape) * stdev)
        yield solve(data, solver)