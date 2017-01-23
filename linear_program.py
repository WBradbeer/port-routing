import copy
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


def setup(cost_f, cost_d, containers_sent):
    F = len(cost_f)
    D = len(list(cost_d))

    c = lp.flatten_3(lp.combine_matrices(np.array(cost_f), np.array(cost_d)))

    b_eq = lp.flatten_2(np.array(containers_sent))
    A_sum = lp.sum_ij_over_k(F, D)
    b_eq.append(0.0)
    A_ub = np.identity(F * F * D) * -1.0
    b_ub = F * F * D * [0.0]
    A_eqs = []
    for comb in lp.gen_scanning_combs(F):
        A_eq = copy.copy(A_sum)
        A_eq.append(lp.scanner_constraints(comb[::-1], F, D))
        A_eqs.append(A_eq)
    return F, c, A_eqs, b_eq, A_ub, b_ub


def run(F, c, A_eqs, b_eq, A_ub, b_ub):
    results = [None] * 2 ** F
    i = 0
    for A_eq in A_eqs:
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


# linear_prog(cost_f, cost_d, containers_sent)
