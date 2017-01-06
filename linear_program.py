import copy
import os

import numpy as np
import pandas as pd
from scipy import optimize as opt

import lp_helpers as lp


file_path = os.path.abspath(os.path.dirname(__file__))

cost_f = pd.read_csv(file_path + "/data/port_cost_t.csv", index_col="Port")
cost_d = pd.read_csv(file_path + "/data/port_cost_d.csv", index_col="Port")
containers_sent = pd.read_csv(file_path + "/data/containers_sent_lp.csv",
                              index_col="Port")


def linear_prog(cost_f, cost_d, containers_sent):
    F = len(cost_f)
    D = len(list(cost_d))

    x = lp.generate_x(F, D)
    c = lp.flatten_3(lp.combine_matrices(np.array(cost_f), np.array(cost_d)))

    b_eq = lp.flatten_2(np.array(containers_sent))
    A_sum = lp.sum_ij_over_k(F, D)
    b_eq.append(0)
    A_ub = np.identity(F * F * D) * -1
    b_ub = F * F * D * [0]
    results = [None] * 2 ** F
    i = 0
    for comb in lp.gen_scanning_combs(F):
        A_eq = copy.copy(A_sum)
        A_eq.append(lp.scanner_constraints(comb[::-1], F, D))
        results[i] = opt.linprog(c, A_eq=A_eq, b_eq=b_eq, A_ub=A_ub, b_ub=b_ub)
        i += 1

    return results


# linear_prog(cost_f, cost_d, containers_sent)
