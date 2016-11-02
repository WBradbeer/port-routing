import os

import pandas as pd

import opt_helpers as oh


file_path = os.path.abspath(os.path.dirname(__file__))

containers_sent = pd.read_csv(file_path + "/data/containers_sent.csv",
                                   index_col="Port")
scanning_ports = list(pd.read_csv(file_path + "/data/scanning_ports.csv",
                                  index_col="Port").index)
distances = pd.read_csv(file_path + "/data/port_costs.csv", index_col="Port")
destinations = ['NY']

scanner_cost = 150

print oh.exhaustive_optimization(distances, containers_sent, scanning_ports,
                                 scanner_cost)
