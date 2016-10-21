import networkx as nx


def df_to_edges(cost_df):
    edges = []
    for port in cost_df.index.values:
        for dest in cost_df.index.values:
            if cost_df[port][dest] > 0:
                edges.append((port,dest,{'cost': cost_df[port][dest]}))
    return edges


def scanning_path(G,source, scanning_ports):
    min_path = None
    min_cost = None
    cost, path = nx.single_source_dijkstra(G, source, weight="cost",
                                           cutoff=min_cost)
    for sp, sc in scanning_ports:
        cost[sp] += sc
        if not min_cost or min_cost > cost[sp]:
            min_cost = cost[sp]
            min_path = path[sp]
    return min_path, min_cost