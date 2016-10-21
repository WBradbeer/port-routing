import networkx as nx
import pandas as pd

import graph_helpers as gh

G = nx.DiGraph()

edge_costs = pd.read_csv("port_costs.csv", index_col="Ports")
ports = edge_costs.index.values
edges = gh.df_to_edges(edge_costs)

G.add_nodes_from(ports)
G.add_edges_from(edges)

scanning_ports = [("Halifax", 5)]


path = gh.scanning_path(G, ports[1], scanning_ports)
print path
