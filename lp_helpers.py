import numpy as np

def flatten_2(data):
    vector = []
    for i in data:
        for j in i:
            vector.append(j)
    return vector

def flatten_3(data):
    return flatten_2(flatten_2(data))


def reshape(vector, rows, cols):
    data = []
    for i in range(0, rows):
        data.append([])
        for j in range(0, cols):
            data[i].append(vector[j + i*cols])
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
    return [flatten_2([[y]*D for y in x]) for x in ident]

