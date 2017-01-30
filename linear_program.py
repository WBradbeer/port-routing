import copy
import itertools
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

def setup_fixed(cost_f, cost_d, containers_sent, n=None):
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


def setup_variable(cost_f, cost_d, containers_sent, scanner_capacity=10000, n=None):
    F = len(cost_f)
    D = len(list(cost_d))

    c = lp.flatten_2(np.array(cost_f)) + lp.flatten_2(np.array(cost_d))

    # constraint: all containers scanned
    b_eq = np.array([sum(x) for x in np.array(containers_sent)])
    A_eq = np.hstack([lp.row_sums(F,F), np.zeros((F,F*D))])

    # constraint: scanning ports inflow = outflow

    A_eq = np.vstack((A_eq, np.hstack([lp.col_sums(F,F), np.array(lp.row_sums(F,D)) * -1])))
    b_eq = np.concatenate([b_eq, [0] * F])

    # constraint: non negativity
    A_ub = np.identity(F * F + F * D) * -1
    b_ub = (F * F + F * D) * [0]

    # constraint: scanner_capacity not exceeded
    A_ub = np.vstack([A_ub, np.hstack([lp.col_sums(F,F), np.zeros((F,F*D))])])
    b_ubs = lp.gen_scanning_bound(lp.gen_scanning_combs(F), scanner_capacity, base=b_ub)

    return F, c, A_eq, b_eq, A_ub, b_ubs

def setup_times(cost_f, cost_d, containers_sent, n=None):
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


def run(F, c, A_eqs, b_eq, A_ub, b_ub):
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


def run_matlab(F, c, A_eqs, b_eq, A_ub, b_ub):
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
