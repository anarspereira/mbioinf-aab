import unittest
from my_graph import MyGraph
from debrujin import DeBruijnGraph


class test_DeBruijnGraph(unittest.TestCase):
    def setUp(self):
        self.debruijn = DeBruijnGraph(MyGraph)


class test_ DeBruijnGraphMethods(test_ DeBruijnGraph):
    def test_runTest(self):
        self.assertEqual(self.debrujin.



if __name__ == '__main__':
    unittest.main()