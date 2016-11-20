def flatten(data):
    vector = []
    for i in data:
        for j in i:
            vector.append(j)
    return vector

def reshape(vector, rows, cols):
    data = []
    for i in range(0, rows):
        data.append([])
        for j in range(0, cols):
            data[i].append(vector[j + i*cols])
    return data
