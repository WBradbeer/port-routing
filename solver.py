import copy
import json
import time

import numpy as np
import pandas as pd

import linear_program as lp


SOLVERS = {
    'gurobi': (lp.setup_gurobi, lp.run_gurobi),
    'gurobi_set': (lp.setup_gurobi, lp.run_gurobi_set_scanners),
    'matlab': (lp.setup_variable_integer, lp.run_variable_integer),
}


def solve(data, solver='gurobi'):
    setup = SOLVERS[solver][0]
    run = SOLVERS[solver][1]
    return [run(*setup(**data))]


def solve_set_scanners(data, scanner_set, solver='gurobi_set'):
    setup = list(SOLVERS[solver][0](**data))
    setup.append(scanner_set)
    run = SOLVERS[solver][1]
    return [run(*setup)]


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
    cost_f = distances[sps][:source]
    cost_d = distances[dp][:source]

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
    o_data = copy.copy(data[varying])
    for val in values:
        data[varying] = o_data * val
        yield solve(data, solver)


def solve_noisy_data(data, varying, stdev, replications, solver='gurobi'):
    o_data = copy.copy(data[varying])
    for i in range(0, replications):
        data[varying] = o_data.add(np.random.randn(*o_data.shape) * stdev)
        yield solve(data, solver)


def leave_one_out(data, solver='gurobi'):
    for port in data['cost_f'].index:
        data_minus = {}
        data_minus['cost_f'] = data['cost_f'].drop(port, 0).drop(port, 1)
        data_minus['cost_d'] = data['cost_d'].drop(port, 0)
        data_minus['containers_sent'] = data['containers_sent'].drop(port, 0)
        data_minus['port_capacities'] = data['port_capacities'].drop(port, 0)
        data_minus['dest_capacities'] = data['dest_capacities']
        data_minus['scanner_capacity'] = data['scanner_capacity']
        yield solve(data_minus, solver)


def one_non_scanner(data, ports=None, solver='gurobi'):
    o_data = copy.deepcopy(data['port_capacities'])
    if not ports:
        ports = data['cost_f'].index
    for port in ports:
        data['port_capacities'] = copy.deepcopy(o_data)
        data['port_capacities'][port] = 0
        yield solve(data, solver)


def output_test_results(test, args, solver='gurobi'):
    file_name = time.strftime("%a%d%b%Y%H%M%S", time.localtime()) + '.txt'
    for result in test(*args, solver=solver):
        res_file = open(file_name, mode='a')
        res_file.write(json.dumps(result))
        res_file.write('\n')
        res_file.flush()
        res_file.close()
