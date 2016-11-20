import os

import numpy as np
import pandas as pd
from scipy import optimize as opt

import lp_helpers as lp


file_path = os.path.abspath(os.path.dirname(__file__))

cost_t = pd.read_csv(file_path + "/data/port_cost_t.csv", index_col="Port")
cost_d = pd.read_csv(file_path + "/data/port_cost_d.csv", index_col="Port")

c = lp.flatten(cost_t).append(lp.flatten(cost_d))




