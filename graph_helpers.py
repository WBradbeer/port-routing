from itertools import chain, combinations

import networkx as nx


def powerset(iterable):
    """powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)
       from itertools recipes https://docs.python.org/3/library/itertools.html
    """
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s)+1))


def df_to_edges(df):
    edges = []
    for source in df.index.values:
        for dest in df.index.values:
            if df[source][dest] > 0:
                edges.append((source, dest, {'cost': df[source][dest]}))
    return edges


def scanning_path(G, source, scanning_ports):
    """
    Calculates the shortest path based on edge weight cost by checking
    all
    :param G: graph model with edge weights "cost"
    :param source: port to start from
    :param scanning_ports: iterable of tuples containing scanning ports
           and costs
    :return: tuple (sequence of nodes, cost of path)
    """
    min_path = None
    min_cost = None
    cost, path = nx.single_source_dijkstra(G, source, weight="cost")
    for sp, sc in scanning_ports:
        cost[sp] += sc
        if not min_cost or min_cost > cost[sp]:
            min_cost = cost[sp]
            min_path = path[sp]
    return min_path, min_cost


def total_container_cost(G, containers_sent, scanning_ports):
    """
    Calculates cost of sending all containers along shortest paths
    :param G: graph model with edge weights "cost"
    :param containers_sent: iterable of tuples containing source ports
           and number of containers
    :param scanning_ports: iterable of tuples containing scanning ports
           and costs
    :return: cost of shipping all containers
    """
    total_cost = 0
    if not scanning_ports:
        return None
    for port, num in containers_sent:
        total_cost += scanning_path(G, port, scanning_ports)[1] * num
    return total_cost


def exhaustive_optimization(G, containers_sent, scanning_ports, scanner_cost):
    """

    :param G: graph model with edge weights "cost"
    :param containers_sent: containers_sent: iterable of tuples containing source ports
           and number of containers
    :param scanning_ports: iterable of tuples containing scanning ports
           and costs
    :param scanner_cost: cost of adding a scanner to an additional port
    :return: (optimal arrangement of scanners, cost of arrangement)
    """
    sp_combs = powerset(scanning_ports)
    min_cost = None
    min_sp = None
    for sp in sp_combs:
        cost = total_container_cost(G, containers_sent, sp)
        cost = cost and cost + scanner_cost * len(sp)
        if not min_cost or cost < min_cost:
            min_cost = cost
            min_sp = sp
    return min_sp, min_cost
