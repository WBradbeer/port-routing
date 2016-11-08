from itertools import chain, combinations


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
    total_cost = 0
    if not scanning_ports:
        return None
    explicit_destinations = containers_sent.columns.values
    for d in explicit_destinations:
        dest = destinations or [d]
        for p in containers_sent.index:
            total_cost += scanning_path(p, scanning_ports, distances,
                                        dest)[1] * containers_sent[d][p]
    return total_cost


def exhaustive_optimization(distances, containers_sent, scanning_ports,
                            scanner_cost, destinations=None):
    sp_combs = powerset(scanning_ports)
    min_cost = None
    min_sp = None
    for sp in sp_combs:
        cost = total_container_cost(distances, containers_sent, sp, destinations)
        cost = cost and cost + scanner_cost * len(sp)
        if not min_cost or cost < min_cost:
            min_cost = cost
            min_sp = sp
    return min_sp, min_cost
