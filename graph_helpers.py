import networkx as nx


def df_to_edges(df):
    edges = []
    for source in df.index.values:
        for dest in df.index.values:
            if df[source][dest] > 0:
                edges.append((source, dest, {'cost': df[source][dest]}))
    return edges


def scanning_path(G, source, scanning_ports):
    min_path = None
    min_cost = None
    cost, path = nx.single_source_dijkstra(G, source, weight="cost",
                                           cutoff=min_cost)
    for sp, sc in scanning_ports.itertuples():
        cost[sp] += sc
        if not min_cost or min_cost > cost[sp]:
            min_cost = cost[sp]
            min_path = path[sp]
    return min_path, min_cost


def total_container_cost(G, containers_sent, scanning_ports):
    total_cost = 0
    for port, num in containers_sent.itertuples():
        total_cost += scanning_path(G, port, scanning_ports)[1] * num
    return total_cost
