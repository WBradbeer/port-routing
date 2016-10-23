import os

import networkx as nx
import pandas as pd

import graph_helpers as gh


file_path = os.path.abspath(os.path.dirname(__file__))

containers_sent = list(pd.read_csv(file_path + "/data/containers_sent.csv",
                                   index_col="Port").itertuples())
scanning_ports = list(pd.read_csv(file_path + "/data/scanning_ports.csv",
                                  index_col="Port").itertuples())
edge_costs = pd.read_csv(file_path + "/data/port_costs.csv", index_col="Port")
ports = edge_costs.index.values
edges = gh.df_to_edges(edge_costs)

G = nx.DiGraph()
G.add_nodes_from(ports)
G.add_edges_from(edges)

scanner_cost = 1000

print gh.exhaustive_optimization(G, containers_sent, scanning_ports,
                                 scanner_cost)
