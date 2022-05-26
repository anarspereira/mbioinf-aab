import unittest
from my_graph import MyGraph
from metabolic_network import MetabolicNetwork

class test_MetabolicNetwork(unittest.TestCase):
    def setUp(self):
        self.met_net = MetabolicNetwork(MyGraph)


class test_MetabolicNetworkMethods(test_Metabolic_Network):
    def test_runTest(self):
        self.assertEqual(self.metabolic_network.



if __name__ == '__main__':
    unittest.main()