from itertools import chain, combinations

import matplotlib.pyplot as plt
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
    sp_costs = {}

    for sp in sp_combs:
        cost, cost_matrix = total_container_cost(distances, containers_sent, sp, destinations)
        cost = cost
        if cost:
            sp_costs[str(arrangement_to_decimal(sp))] = cost
            cost += scanner_cost * len(sp)
        if not min_cost or cost < min_cost:
            min_cost = cost
            min_sp = sp
            min_cost_matrix = cost_matrix
    
    costdf = pd.DataFrame(min_cost_matrix, index=scanning_ports)
    costdf['Scanner_cost'] = [(x in min_sp)*scanner_cost for x in costdf.index]
    costdf['Total'] = [sum(x) for x in costdf.itertuples(index=False)]

    return min_sp, min_cost, costdf, sp_costs


def arrangement_to_decimal(arrangement, pref_len=1, offset=1):
    decimal = 0
    for sp in arrangement:
        try:
            decimal += 2**(int(sp[pref_len:])-offset)
        except IndexError:
            decimal += 2 ** (sp-offset)
    return decimal


def decimal_to_arrangement(decimal, pref='O'):
    arrangement = set()
    i = 1
    while decimal > 0:
        if decimal % 2:
            arrangement.add('{}{}'.format(pref, i))
            decimal -= 1
        decimal /= 2
        i += 1
    return arrangement


def plot_frontier(sp_costs, highlight=None):
    trans_costs = []
    sp_count = []
    for dec, cost in sp_costs.iteritems():
        if cost:
            trans_costs.append(cost)
            sp_count.append(len(decimal_to_arrangement(int(dec))))
    plt.scatter(trans_costs, sp_count)
    plt.xlabel("Trans-shipment cost")
    plt.ylabel("Number of Scanners")
    if highlight:
        plt.scatter(*highlight_point(sp_costs, highlight), s=50.0, color='red')
    plt.show()


def highlight_point(sp_costs, highlight):
    return sp_costs[str(arrangement_to_decimal(highlight))], len(highlight)
