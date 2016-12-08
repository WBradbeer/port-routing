import os
import unittest

import pandas as pd

import opt_helpers as oh


FILE_PATH = os.path.abspath(os.path.dirname(__file__))

class OptTestCase(unittest.TestCase):
    def setUp(self):
        case_path =  "/../data/test_cases/tc1/"

        self.c_sent = pd.read_csv(FILE_PATH + case_path + "containers_sent.csv",
                                  index_col="Port")
        self.s_ports = list(pd.read_csv(FILE_PATH + case_path + "scanning_ports.csv",
                                        index_col="Port").index)
        self.distances = pd.read_csv(FILE_PATH + case_path + "port_costs.csv",
                                     index_col="Port")
        self.s_cost = 10000

    def test_powerset(self):
        result = set(oh.powerset([1, 2, 3]))
        pset = {(), (1,),(2, ),(3, ),(1, 2),(1, 3),(2, 3),(1, 2, 3)}
        self.assertEqual(result, pset)

    def test_scanning_path(self):
        path, cost = oh.scanning_path(self.s_ports[0], self.s_ports, self.distances,
                         [self.c_sent.columns.values[0]])
        self.assertEqual(path, ('F1', 'D1'))
        self.assertEqual(cost, 10)

    def test_total_container_cost(self):
        cost, matrix = oh.total_container_cost(self.distances, self.c_sent, self.s_ports, None)
        self.assertEqual(cost, 500)
        self.assertEqual(matrix, {'D2': [100, 50, 100], 'D1': [100, 50, 100]})

    def test_exhaustive_optimization(self):
        sp, cost, costdf, sp_costs = oh.exhaustive_optimization(self.distances,
                                                                self.c_sent,
                                                                self.s_ports,
                                                                self.s_cost)
        matrix = [[150, 150, 0, 300],
                  [50, 50, 10000, 10100],
                  [150, 150, 0, 300]]
        self.assertEqual(sp, ('F2',))
        self.assertEqual(cost, 10700)
        self.assertEqual(sp_costs, {'1': 1200, '3': 600, '2': 700, '5': 800,
                                    '4': 1200, '7': 500, '6': 600})

    def test_arrangement_to_decimal(self):
        dec = oh.arrangement_to_decimal(("O1", "O2", "O4"))
        self.assertEqual(dec, 11)

    def test_decimal_to_arrangement(self):
        arr = oh.decimal_to_arrangement(11)
        self.assertEqual(arr, set(("O1", "O2", "O4")))

    def test_highlight_point(self):
        self.assertEqual(oh.highlight_point({'1': 1}, ('O1',)), (1,1))