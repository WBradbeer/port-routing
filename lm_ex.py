import os

import pandas as pd

import linear_model as lm

# file_path = os.path.abspath(os.path.dirname(__file__))
#
# containers_sent = list(pd.read_csv(file_path + "/data/containers_sent.csv",
#                                    index_col="Port").itertuples())
# costs = pd.read_csv(file_path + "/data/port_costs.csv", index_col="Port")

lm.generate_T(3,3,[[1,1,1], [1,1,1],[1,1,1]])