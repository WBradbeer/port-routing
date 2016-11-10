import os

import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd


def df_to_edges(cost_df):
    edges = []
    for port in cost_df.index.values:
        for dest in cost_df.index.values:
            if cost_df[port][dest] > 0:
                edges.append((port,dest,{'cost': cost_df[port][dest]}))
    return edges

G = nx.DiGraph()

file_path = os.path.abspath(os.path.dirname(__file__))
edge_costs = pd.read_csv(file_path + "/data/port_costs.csv",
                         index_col="Port")
port_pos = {x[0]: [x[1], x[2]] for x in pd.read_csv(file_path +
                                                    "/data/port_pos.csv",
                                                    index_col="Port").itertuples()}
ports = edge_costs.index.values
edges = df_to_edges(edge_costs)

G.add_nodes_from(ports)
G.add_edges_from(edges)

edge_labels = {(x[0], x[1]): x[2]['cost'] for x in edges}
print edge_labels
nx.draw(G, pos=port_pos, node_size=1000, node_color=['k','b','b','r','k'])
nx.draw_networkx_labels(G, port_pos, font_size=18, font_color='white')
nx.draw_networkx_edge_labels(G, port_pos, font_size=12, edge_labels=edge_labels)
plt.show()



