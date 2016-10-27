def travel_cost(T, C, n):
    """

    :param T: k*i*j matrix of containers shipped from i to j and scanned at k
    :param C: i*j matrix of cost to travel from i to j
    :param n: number of source ports
    :return: sum of travel cost
    """
    cost = 0
    for k in range(n):
        cost += sum(C.multiply(T[k]))
    return cost


def scanner_cost(s, Y):
    return sum(s*Y)


def total_cost(T, C, n, s, Y):
    return travel_cost(T, C, n) + scanner_cost(s, Y)


def generate_T(n, m, lda):
    T = []
    for k in range(0, n):
        for i in range(0, n):
            row = []
            for j in range(0,m):
                col = []
                col.append(lda[i][j])
            row.append(col)
        T.append(row)   