import os

import numpy as np
import pandas as pd
from scipy import optimize as opt

import lp_helpers as lp


file_path = os.path.abspath(os.path.dirname(__file__))

cost_f = pd.read_csv(file_path + "/data/port_cost_t.csv", index_col="Port")
cost_d = pd.read_csv(file_path + "/data/port_cost_d.csv", index_col="Port")
containers_sent = pd.read_csv(file_path + "/data/containers_sent.csv",
                              index_col="Port")

F = len(cost_f)
D = len(cost_d)

c = lp.flatten_3(lp.combine_matrices(np.array(cost_f), np.array(cost_d)))

b_eq = lp.flatten_2(containers_sent)
A_eq = lp.sum_on_k(F,D)
