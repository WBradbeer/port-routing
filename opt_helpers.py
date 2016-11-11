from itertools import chain, combinations

import pandas as pd


def powerset(iterable):
    """powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)
       from itertools recipes https://docs.python.org/3/library/itertools.html
    """
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s)+1))


def scanning_path(source, scanning_ports, distances, destinations):
    min_path = None
    min_cost = None
    for d in destinations:
        for sp in scanning_ports:
            cost = distances[source][sp] + distances[sp][d]
            if not min_cost or min_cost > cost:
                min_cost = cost
                min_path = (sp, d)
    return min_path, min_cost


def total_container_cost(distances, containers_sent, scanning_ports,
                         destinations):
    cost_matrix = {}
    total_cost = 0
    if not scanning_ports:
        return None, None
    explicit_destinations = containers_sent.columns.values
    for d in explicit_destinations:
        cost_matrix[d] = []
        dest = destinations or [d]
        for p in containers_sent.index:
            cost = scanning_path(p, scanning_ports, distances,
                                        dest)[1] * containers_sent[d][p]
            total_cost += cost
            cost_matrix[d].append(cost)
    return total_cost, cost_matrix


def exhaustive_optimization(distances, containers_sent, scanning_ports,
                            scanner_cost, destinations=None):
    sp_combs = powerset(scanning_ports)
    min_cost = None
    min_sp = None
    min_cost_matrix = None

    for sp in sp_combs:
        cost, cost_matrix = total_container_cost(distances, containers_sent, sp, destinations)
        cost = cost and cost + scanner_cost * len(sp)
        if not min_cost or cost < min_cost:
            min_cost = cost
            min_sp = sp
            min_cost_matrix = cost_matrix
    
    costdf = pd.DataFrame(min_cost_matrix, index=scanning_ports)

    return min_sp, min_cost, costdf
