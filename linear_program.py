from __future__ import division
import copy
import itertools
import math
import os
import time

import numpy as np
import pandas as pd
from scipy import optimize as opt

import lp_helpers as lp


file_path = os.path.abspath(os.path.dirname(__file__))

cost_f = pd.read_csv(file_path + "/data/port_cost_t.csv", index_col="Port")
cost_d = pd.read_csv(file_path + "/data/port_cost_d.csv", index_col="Port")
containers_sent = pd.read_csv(file_path + "/data/containers_sent_lp.csv",
                              index_col="Port")



def setup_fixed(cost_f, cost_d, containers_sent, port_capacities=None, dest_capacities=None,n=None):
    F = len(cost_f)
    D = len(list(cost_d))

    c = lp.flatten_3(lp.combine_matrices(np.array(cost_f), np.array(cost_d)))

    b_eq = lp.flatten_2(np.array(containers_sent))
    A_sum = lp.sum_ij_over_k(F, D)
    b_eq.append(0.0)
    A_ub = np.identity(F * F * D) * -1.0
    b_ub = F * F * D * [0.0]
    A_eqs = []
    combs = lp.gen_scanning_combs(F)
    if n:
        combs = itertools.islice(combs, 0, None, 2**F/n)
    for comb in combs:
        A_eq = copy.copy(A_sum)
        A_eq.append(lp.scanner_constraints(comb[::-1], F, D))
        A_eqs.append(A_eq)
    return F, c, A_eqs, b_eq, A_ub, b_ub


def setup_variable(cost_f, cost_d, containers_sent, port_capacities, dest_capacities, scanner_capacity=10000, n=None):
    F = len(cost_f)
    D = len(list(cost_d))

    c = lp.flatten_2(np.array(cost_f)) + lp.flatten_2(np.array(cost_d))

    # constraint: all containers scanned
    b_eq = containers_sent[0]
    A_eq = np.hstack([lp.row_sums(F,F), np.zeros((F,F*D))])

    # constraint: scanning ports inflow = outflow
    A_eq = np.vstack((A_eq, np.hstack([lp.col_sums(F,F), np.array(lp.row_sums(F,D)) * -1])))
    b_eq = np.concatenate([b_eq, [0] * F])

    # constraint: non negativity
    A_ub = np.identity(F * F + F * D) * -1
    b_ub = (F * F + F * D) * [0]

    # constraint: scanning port capacity
    A_ub = np.vstack([A_ub, np.hstack([lp.col_sums(F, F), np.zeros((F, F * D))])])
    b_ub.extend(port_capacities)

    # constraint: destination port capacity
    A_ub = np.vstack([A_ub, np.hstack([np.zeros((D, F * F)), lp.col_sums(F, D)])])
    b_ub.extend(dest_capacities)

    # constraint: scanner_capacity not exceeded
    A_ub = np.vstack([A_ub, np.hstack([lp.col_sums(F,F), np.zeros((F,F*D))])])
    b_ubs = lp.gen_scanning_bound(lp.gen_scanning_combs(F), scanner_capacity, base=b_ub)

    return F, c, A_eq, b_eq, A_ub, b_ubs

def setup_variable_integer(cost_f, cost_d, containers_sent, port_capacities, dest_capacities,
                           scanner_capacity=10000, n=None):
    F = len(cost_f)
    D = len(list(cost_d))

    port_names = list(cost_f.columns.values)

    c = lp.flatten_2(np.array(cost_f)) + lp.flatten_2(np.array(cost_d)) + (F) * [0]

    # constraint: all containers scanned
    A_eq = np.hstack([lp.row_sums(F, F), np.zeros((F, F * D)), np.zeros((F, F))])
    b_eq = containers_sent

    # constraint: scanning ports inflow = outflow
    A_eq = np.vstack((A_eq, np.hstack([lp.col_sums(F,F), np.array(lp.row_sums(F,D)) * -1, np.zeros((F, F))])))
    b_eq = np.concatenate([b_eq, [0] * F])

    # constraint: sum of scanners = iteration
    min_scan = int(math.ceil(sum(containers_sent.values) / scanner_capacity))
    max_scan = int(sum((math.ceil(x / scanner_capacity) for x in
                        containers_sent.values)))
    scanner_range = range(min_scan, max_scan + 1)
    A_eq = np.vstack((A_eq, np.hstack([ [0] * (F * F), [0] * (F * D), [1] * (F)])))
    b_eq = np.concatenate([b_eq, [0] * (1)])

    # constraint: non negativity
    A_ub = np.identity(F * F + F * D + F) * -1
    b_ub = (F * F + F * D + F) * [0]

    # constraint: scanning port capacity
    A_ub = np.vstack([A_ub, np.hstack([lp.col_sums(F, F), np.zeros((F, F * D)), np.zeros((F, F))])])
    b_ub.extend(port_capacities)

    # constraint: destination port capacity
    A_ub = np.vstack([A_ub, np.hstack([np.zeros((D, F * F)), lp.col_sums(F, D), np.zeros((D, F))])])
    b_ub.extend(dest_capacities)

    # constraint: scanner_capacity not exceeded
    A_ub = np.vstack([A_ub, np.hstack([lp.col_sums(F,F), np.zeros((F,F*D)), np.identity(F) * (-scanner_capacity)])])
    b_ubs = np.concatenate([b_ub, [0] * F])

    return F, c, A_eq, b_eq, A_ub, b_ubs, scanner_range, port_names

def setup_times(cost_f, cost_d, containers_sent, port_capacities=None, dest_capacities=None, n=None):
    F = len(cost_f)
    D = len(list(cost_d))
    t = time.clock()
    x = lp.generate_x(F, D)
    t1 = time.clock() - t
    t = time.clock()
    c = lp.flatten_3(lp.combine_matrices(np.array(cost_f), np.array(cost_d)))
    t2 = time.clock() - t
    t = time.clock()
    b_eq = lp.flatten_2(np.array(containers_sent))
    t3 = time.clock() - t
    t = time.clock()
    A_sum = lp.sum_ij_over_k(F, D)
    t4 = time.clock() - t
    t = time.clock()
    b_eq.append(0)
    A_ub = np.identity(F * F * D) * -1
    b_ub = F * F * D * [0]
    A_eqs = []
    t5 = time.clock() - t
    t = time.clock()
    for comb in lp.gen_scanning_combs(F):
        A_eq = A_sum[:]
        A_eq.append(lp.scanner_constraints(comb[::-1], F, D))
        A_eqs.append(A_eq)
    t6 = time.clock() - t
    return t1, t2, t3, t4, t5, t6


def setup_gurobi(cost_f, cost_d, containers_sent, port_capacities,
                 dest_capacities, scanner_capacity):
    import gurobipy as gb
    cost_foreign = {(x,y): cost_f[y][x] for x in cost_f.index for y in
                    cost_f.columns}
    cost_dest = {(x, y): cost_d[y][x] for x in cost_d.index for y in
                 cost_d.columns}
    m = gb.Model('solver')
    f_ship = m.addVars(cost_foreign.keys(), obj=cost_foreign,
                             name="foreign_ship")
    d_ship = m.addVars(cost_dest.keys(), obj=cost_dest,
                          name="dest_ship")
    scanners = m.addVars(cost_f.columns, obj=[0.0]*len(cost_f.columns),
                          vtype=gb.GRB.INTEGER, name="scanners")

    # constraint: all containers scanned
    m.addConstrs((f_ship.sum(i, '*') == containers_sent[i] for i in cost_f.columns),
                 "all_scanned")

    # constraint: scanning ports inflow = outflow
    m.addConstrs((f_ship.sum('*', i) == d_ship.sum(i, '*') for i in cost_f.columns),
                 "inflow=outflow")

    # constraint: scanning capacity
    m.addConstrs((f_ship.sum('*', i) <= scanner_capacity * scanners[i] for i in
                  cost_f.columns), "scanning_capacity")

    # constraint: foreign port capacity not exceeded
    m.addConstrs((f_ship.sum('*', i) <= port_capacities[i] for i in
                  cost_f.columns), "foreign_capacity")

    # constraint: destination port capacity
    m.addConstrs((d_ship.sum('*', i) <= dest_capacities[i] for i in
                  cost_d.columns), "dest_capacity")

    # constraint: # of scanners
    min_scan = int(math.ceil(sum(containers_sent.values) / scanner_capacity))
    max_scan = int(sum((math.ceil(x/scanner_capacity) for x in
                    containers_sent.values)))
    combs = range(min_scan, max_scan + 1)
    m.addConstr(scanners.sum('*') == 0, "scanner_number")

    return m, combs, len(cost_f.columns)


def run_gurobi(m, combs, F):
    results = {}
    m.params.OutputFlag = 0
    m.update()
    for i in combs:
        c = m.getConstrByName("scanner_number")
        c.setAttr("rhs", i)
        m.optimize()
        if m.SolCount:
            res = {
                'scanner': {x.varName: x.X for x in m.getVars()[-F:]},
                'obj': round(m.objVal),
            }
        else: res = {'obj': -1}
        results[str(i)] = res
    return results


def run_fixed(F, c, A_eqs, b_eq, A_ub, b_ub):
    results = [None] * 2 ** F
    i = 0
    for A_eq in A_eqs:
        results[i] = opt.linprog(c, A_eq=A_eq, b_eq=b_eq, A_ub=A_ub, b_ub=b_ub)
        i += 1
    return results


def run_variable(F, c, A_eq, b_eq, A_ub, b_ubs):
    results = [None] * 2 ** F
    i = 0
    for b_ub in b_ubs:
        results[i] = opt.linprog(c, A_eq=A_eq, b_eq=b_eq, A_ub=A_ub, b_ub=b_ub)
        i += 1
    return results


def run_octave(F, c, A_eqs, b_eq, A_ub, b_ub):
    import oct2py
    oc = oct2py.Oct2Py()
    results = [None] * 2 ** F
    ctype = 'S' * len(b_eq) + 'U' * len(b_ub)
    b = copy.copy(b_eq)
    b.extend(b_ub)
    lb = [0] * len(c)
    ub = [2**12] * len(c)
    i = 0
    for A_eq in A_eqs:
        A_eq.extend(A_ub)
        A_eq = [list(row) for row in A_eq]
        results[i] = oc.glpk(c, A_eq, b, lb, ub, ctype)
        i += 1
    return results


def run_fixed_matlab(F, c, A_eqs, b_eq, A_ub, b_ub):
    import matlab.engine
    eng = matlab.engine.start_matlab()
    lb = matlab.double([0] * len(c))
    results = [None] * 2 ** F
    b_eq = matlab.double(initializer=b_eq)
    b_ub = matlab.double(initializer=b_ub)
    c = matlab.double(initializer=c)
    A_ub = [list(row) for row in A_ub]
    A_ub = matlab.double(initializer=A_ub)

    i = 0
    for A_eq in A_eqs:
        A_eq = [list(row) for row in A_eq]
        A_eq = matlab.double(initializer=A_eq)
        results[i] = eng.linprog(c, A_ub, b_ub, A_eq, b_eq, lb)
        i += 1
    return results


def run_variable_matlab(F, c, A_eq, b_eq, A_ub, b_ubs):
    import matlab.engine
    eng = matlab.engine.start_matlab()
    lb = matlab.double([0] * len(c))
    results = [None] * 2 ** F
    b_eq = list(b_eq)
    b_eq = matlab.double(initializer=b_eq)
    c = matlab.double(initializer=c)
    A_eq = [list(row) for row in A_eq]
    A_eq = matlab.double(initializer=A_eq)
    A_ub = [list(row) for row in A_ub]
    A_ub = matlab.double(initializer=A_ub)
    
    i = 0
    for b_ub in b_ubs:
        b_ub = list(b_ub)
        b_ub = matlab.double(initializer=b_ub)
        results[i] = eng.linprog(c, A_ub, b_ub, A_eq, b_eq, lb)
        i += 1
    return results


def run_variable_integer(F, c, A_eq, b_eq, A_ub, b_ub, scanner_range, port_names):
    import matlab.engine
    eng = matlab.engine.start_matlab()
    lb = matlab.double([0] * len(c))
    b_eq = list(b_eq)
    b_ub = list(b_ub)
    b_ub = matlab.double(initializer=b_ub)
    c = matlab.double(initializer=c)
    A_eq = [list(row) for row in A_eq]
    A_eq = matlab.double(initializer=A_eq)
    A_ub = [list(row) for row in A_ub]
    A_ub = matlab.double(initializer=A_ub)

    int_dec_vars = range(A_eq.size[1] - F + 1, A_eq.size[1] + 1 )
    int_dec_vars = matlab.double(initializer=int_dec_vars)
    results = {}

    for n in scanner_range:
        b_eq[-1] = n
        b_eqs = matlab.double(initializer=b_eq)
        dec_vars = eng.intlinprog(c, int_dec_vars, A_ub, b_ub, A_eq, b_eqs, lb)
        if dec_vars:
            res = {
                'scanner':{"scanner[{}]".format(x): round(float(y[0])) for x, y in zip(port_names, dec_vars[-F:])},
                'obj': round(float(np.array(c).dot(np.array(dec_vars))[0][0]))
            }
        else: res = {'obj': -1}
        results[str(n)] = res
    return results


def run_times_matlab(F, c, A_eqs, b_eq, A_ub, b_ub):
    import matlab.engine
    eng = matlab.engine.start_matlab()
    lb = matlab.double([0] * len(c))
    results = [None] * 2 ** F
    b_eq = matlab.double(initializer=b_eq)
    b_ub = matlab.double(initializer=b_ub)
    c = matlab.double(initializer=c)
    A_ub = [list(row) for row in A_ub]
    A_ub = matlab.double(initializer=A_ub)

    i = 0
    for A_eq in A_eqs:
        A_eq = [list(row) for row in A_eq]
        A_eq = matlab.double(initializer=A_eq)
        t = time.clock()
        eng.linprog(c, A_ub, b_ub, A_eq, b_eq, lb)
        results[i] = time.clock() - t
        i += 1
    return results


def run_times(F, c, A_eqs, b_eq, A_ub, b_ub, n=None):
    times = [None] * 2 ** F
    i = 0
    if n:
        A_eqs = A_eqs[::len(A_eqs)/n]
    for A_eq in A_eqs:
        t = time.clock()
        opt.linprog(c, A_eq=A_eq, b_eq=b_eq, A_ub=A_ub, b_ub=b_ub)
        times[i] = time.clock() - t
        i += 1
    return times
