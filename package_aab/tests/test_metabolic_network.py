import unittest
from my_graph import MyGraph
from metabolic_network import MetabolicNetwork

class test_MetabolicNetwork(unittest.TestCase):
    def setUp(self):
        self.met_net = MetabolicNetwork("metabolite-reaction")
        self.v1 = m.add_vertex_type("R1", "reaction")
        self.v2 = m.add_vertex_type("R2", "reaction")
        self.v3 = m.add_vertex_type("R3", "reaction")
        self.v4 = m.add_vertex_type("M1", "metabolite")
        self.v5 = m.add_vertex_type("M2", "metabolite")
        self.v6 = m.add_vertex_type("M3", "metabolite")
        self.v7 = m.add_vertex_type("M4", "metabolite")
        self.v8 = m.add_vertex_type("M5", "metabolite")
        self.v9 = m.add_vertex_type("M6", "metabolite")
        self.e1 = m.add_edge("M1", "R1")
        self.e2 = m.add_edge("M2", "R1")
        self.e3 = m.add_edge("R1", "M3")
        self.e4 = m.add_edge("R1", "M4")
        self.e5 = m.add_edge("M4", "R2")
        self.e6 = m.add_edge("M6", "R2")
        self.e7 = m.add_edge("R2", "M3")
        self.e8 = m.add_edge("M4", "R3")
        self.e9 = m.add_edge("M5", "R3")
        self.e10 = m.add_edge("R3", "M6")
        self.e11 = m.add_edge("R3", "M4")
        self.e12 = m.add_edge("R3", "M5")
        self.e13 = m.add_edge("M6", "R3")


class test_MetabolicNetworkMethods(test_Metabolic_Network):
    def test_runTest(self):


if __name__ == '__main__':
    unittest.main()