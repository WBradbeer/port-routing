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
        for j in range(0, len(d1[i])):
            combined[i].append([])
            for k in range(0, len(d2[j])):
                combined[i][j].append(d2[j][k])
    return combined


def sum_on_k(F, D):
    ident = np.identity(F*D)
    return [flatten_2([[y]*F for y in x]) for x in ident]


def scanner_constraints(scanning, F, D):
    scanning = [abs(x - 1) for x in scanning]
    return flatten_2([[x]*D for x in scanning]*F)

