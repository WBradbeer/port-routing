import json
import os
import unittest

import pandas as pd

import linear_program


FILE_PATH = os.path.abspath(os.path.dirname(__file__))


class VariableTestCase(unittest.TestCase):
    def setUp(self):
        def setUpTC(case=1, prob_num=1):
            case_path = "/../data/variable_test_cases/tc{}/".format(case)

            port_info = pd.read_csv(FILE_PATH + case_path + "foreign_port_info.csv",
                                      index_col="Port")
            self.c_sent = port_info["Containers"]
            self.p_capacity = port_info["Capacity"]
            self.c_received = pd.read_csv(FILE_PATH + case_path + "containers_received.csv",
                                      index_col="Port")["Containers"]
            self.s_ports = list(port_info.index)

            distances = pd.read_csv(FILE_PATH + case_path + "port_costs.csv",
                                         index_col="Port")
            source = len(self.s_ports)
            dest = len(self.c_received)
            sps = range(0, source)
            dp = range(source, source + dest)
            self.cost_t = distances[sps][:-dest]
            self.cost_d = distances[dp][:-dest]

            problem = json.load(open(FILE_PATH + case_path + "problem{}.json".format(prob_num)))

            self.s_capacity = problem['scanner_capacity']
            self.solution = problem["solution"]

        self.testcase = setUpTC

        def run_test(setup, run):
            setup = setup(self.cost_t, self.cost_d, self.c_sent, self.p_capacity, self.c_received,
                          self.s_capacity)
            self.results = run(*setup)

        self.run_test = run_test

    def test_case_1_gurobi(self):
        self.testcase(1)
        self.run_test(linear_program.setup_gurobi, linear_program.run_gurobi)
        self.assertDictEqual(self.results,self.solution)

    def test_case_2_gurobi(self):
        self.testcase(2)
        self.run_test(linear_program.setup_gurobi, linear_program.run_gurobi)
        self.assertDictEqual(self.results,self.solution)

    def test_case_3_gurobi(self):
        self.testcase(3)
        self.run_test(linear_program.setup_gurobi, linear_program.run_gurobi)
        self.assertDictEqual(self.results,self.solution)

    def test_case_4_1_gurobi(self):
        self.testcase(4, 1)
        self.run_test(linear_program.setup_gurobi, linear_program.run_gurobi)
        self.assertDictEqual(self.results,self.solution)

    def test_case_4_2_gurobi(self):
        self.testcase(4, 2)
        self.run_test(linear_program.setup_gurobi, linear_program.run_gurobi)
        self.assertDictEqual(self.results,self.solution)

    def test_case_4_3_gurobi(self):
        self.testcase(4, 3)
        self.run_test(linear_program.setup_gurobi, linear_program.run_gurobi)
        self.assertDictEqual(self.results,self.solution)

    def test_case_5_gurobi(self):
        self.testcase(5)
        self.run_test(linear_program.setup_gurobi, linear_program.run_gurobi)
        self.assertDictEqual(self.results,self.solution)

    def test_case_6_gurobi(self):
        self.testcase(6)
        self.run_test(linear_program.setup_gurobi, linear_program.run_gurobi)
        self.assertDictEqual(self.results,self.solution)

    def test_case_7_gurobi(self):
        self.testcase(7)
        self.run_test(linear_program.setup_gurobi, linear_program.run_gurobi)
        self.assertDictEqual(self.results,self.solution)

    def test_case_8_gurobi(self):
        self.testcase(8)
        self.run_test(linear_program.setup_gurobi, linear_program.run_gurobi)
        self.assertDictEqual(self.results,self.solution)

    def test_case_9_gurobi(self):
        self.testcase(9)
        self.run_test(linear_program.setup_gurobi, linear_program.run_gurobi)
        self.assertDictEqual(self.results,self.solution)

    def test_case_10_gurobi(self):
        self.testcase(10)
        self.run_test(linear_program.setup_gurobi, linear_program.run_gurobi)
        self.assertDictEqual(self.results,self.solution)

    def test_case_11_gurobi(self):
        self.testcase(11)
        self.run_test(linear_program.setup_gurobi, linear_program.run_gurobi)
        self.assertDictEqual(self.results,self.solution)

    def test_case_12_gurobi(self):
        self.testcase(12)
        self.assertRaises(OverflowError, self.run_test, *[linear_program.setup_gurobi, linear_program.run_gurobi])
