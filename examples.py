import math

import pandas as pd

import linear_program
import opt_helpers as oh

def generate_containers(source_num, dest_num, sent=1):
    cont = {}
    for i in range(0,dest_num):
        cont[i] = []
        for j in range(0, source_num):
            cont[i].append(sent)
    return pd.DataFrame(cont)

def generate_distances(source_num, dest_num, dist=1):
    distances = {}
    for i in range(0,source_num + dest_num):
        distances[i] = []
        for j in range(0, source_num + dest_num):
            if i == j:
                distances[i].append(0)
            else:
                distances[i].append(dist)
    return pd.DataFrame(distances)

def run_exhaustive_n(n, scanner_cost=100):
    source = n
    dest = int(math.ceil(n / 4.0))
    containers = generate_containers(source, dest)
    distances = generate_distances(source, dest)
    sps = list(containers.index)
    return oh.exhaustive_optimization(distances, containers, sps,
                               scanner_cost)

def run_setup_n(n, scanner_cost=100):
    source = n
    dest = int(math.ceil(n / 4.0))
    containers = generate_containers(source, dest)
    distances = generate_distances(source, dest)


    sps = range(0, source)
    dp = range(source, source + dest)
    return linear_program.setup(distances[sps][:-dest], distances[dp], containers)
