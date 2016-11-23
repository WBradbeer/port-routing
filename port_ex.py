import os

import numpy as np
import pandas as pd

import lp_helpers as lp
import opt_helpers as oh


file_path = os.path.abspath(os.path.dirname(__file__))

containers_sent = pd.read_csv(file_path + "/data/containers_sent.csv",
                                   index_col="Port")
scanning_ports = list(pd.read_csv(file_path + "/data/scanning_ports.csv",
                                  index_col="Port").index)
distances = pd.read_csv(file_path + "/data/port_costs.csv", index_col="Port")

scanner_cost = 10000

result = oh.exhaustive_optimization(distances, containers_sent, scanning_ports,
                                    scanner_cost)

print result[0]

print result[3][str(oh.arrangement_to_decimal(('O1', 'O4', 'O7')))]


oh.plot_frontier(result[3], highlight=('O1', 'O4', 'O8'))
