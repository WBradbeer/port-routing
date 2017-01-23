import os
import unittest

import pandas as pd

import lp_helpers as lp
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
        self.assertEqual(arr, {"O1", "O2", "O4"})

    def test_highlight_point(self):
        self.assertEqual(oh.highlight_point({'1': 1}, ('O1',)), (1,1))


class LPTestCase(unittest.TestCase):
    def test_flatten_2(self):
        self.assertEqual(lp.flatten_2([[1, 2], [3]]), [1,2,3])

    def test_flatten_2_empty(self):
        self.assertEqual(lp.flatten_2([[]]), [])

    def test_flatten_3(self):
        self.assertEqual(lp.flatten_3([[[1], [2]],[[3, 4]]]), [1,2,3,4])

    def test_flatten_3_empty(self):
        self.assertEqual(lp.flatten_3([[[]]]), [])

    def test_reshape_2D(self):
        self.assertEqual(lp.reshape_2D([1,2,3,4],2,2), [[1,2],[3,4]])

    def test_reshape_3D(self):
        self.assertEqual(lp.reshape_3D(range(1,9),2,2),
                         [[[1,2],[3,4]],[[5,6],[7,8]]])

    def test_combine_matrices(self):
        self.assertEqual(lp.combine_matrices([[1,2],[3,4]],[[1],[2]]),
                         [[[2],[4]],[[4],[6]]])

    def test_sum_on_k(self):
        mat = [[1.0,0.0,1.0,0.0,0.0,0.0,0.0,0.0],
               [0.0,1.0,0.0,1.0,0.0,0.0,0.0,0.0],
               [0.0,0.0,0.0,0.0,1.0,0.0,1.0,0.0],
               [0.0,0.0,0.0,0.0,0.0,1.0,0.0,1.0]]
        result = lp.sum_ij_over_k(2,2)
        [self.assertSequenceEqual(mat[i],
                                  list(result[i])) for i in range(0,len(mat))]

    def test_scanner_constraints(self):
        self.assertSequenceEqual(lp.scanner_constraints((1,0),2,2),
                                 [0,0,1,1,0,0,1,1])

    def test_generate_x(self):
        xs = ['X(1,1,1)', 'X(1,1,2)', 'X(1,2,1)', 'X(1,2,2)', 'X(2,1,1)',
              'X(2,1,2)', 'X(2,2,1)', 'X(2,2,2)']
        self.assertEqual(lp.generate_x(2,2),xs)

    def test_show_eq(self):
        xs = ['X(1,1,1)', 'X(1,1,2)', 'X(1,2,1)', 'X(1,2,2)', 'X(2,1,1)',
              'X(2,1,2)', 'X(2,2,1)', 'X(2,2,2)']
        eqn = """1*X(1,1,1) 1*X(1,1,2) 1*X(1,2,1) 1*X(1,2,2) 1*X(2,1,1) 1*X(2,1,2) 1*X(2,2,1) 1*X(2,2,2) = 0"""
        self.assertEqual(lp.show_eq(xs, [1]*len(xs), 0), eqn)