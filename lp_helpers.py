import itertools
import numpy as np


def flatten_2(data):
    vector = []
    for i in data:
        for j in i:
            vector.append(j)
    return vector


def flatten_3(data):
    return flatten_2(flatten_2(data))


def reshape_2D(vector, rows, cols):
    data = []
    for i in range(0, rows):
        data.append([])
        for j in range(0, cols):
            data[i].append(vector[j + i*cols])
    return data


def reshape_3D(vector, F, D):
    data = []
    for i in range(0, F):
        data.append([])
        for j in range(0, F):
            data[i].append([])
            for k in range(0, D):
                data[i][j].append(vector[k + j*D + i*F*D])
    return data


def combine_matrices(d1, d2):
    combined = []
    for i in range(0, len(d1)):
        combined.append([])
        for k in range(0, len(d1[i])):
            combined[i].append([])
            for j in range(0, len(d2[k])):
                combined[i][k].append(d1[i][k] + d2[k][j])
    return combined


def sum_ij_over_k(F, D):
    block = np.tile(np.identity(D), F)
    zeros = np.zeros_like(block)
    id_f = np.identity(F)
    return flatten_2([np.hstack((block if col == 1 else zeros for col in row)
                                ) for row in id_f])


def scanner_constraints(scanning, F, D):
    scanning = [abs(x - 1) for x in scanning]
    return flatten_2([[x]*D for x in scanning]*F)


def generate_x(F, D):
    x = []
    for i in range(0, F):
        for k in range(0, F):
            for j in range(0, D):
                x.append("X({},{},{})".format(i+1, k+1, j+1))
    return x


def show_eq(x, coefs, b):
    eq = ""
    for i in range(0, len(x)):
        eq += str(coefs[i]) + "*" + x[i] + " "
    return eq + "= " + str(b)


def gen_scanning_combs(F):
    for comb in itertools.product([0,1], repeat=F):
        yield comb
