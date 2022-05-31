import unittest
from overlap_graph import OverlapGraph


class test_OverlapGraph(unittest.TestCase):
    def setUp(self):
        seq = "CAATCATGATG"

    def composition(self):
        self.assertEqual(self.composition(3), ['AAT', 'ATC', 'ATG', 'ATG', 'CAA', 'CAT', 'GAT', 'TCA', 'TGA'])


if __name__ == '__main__':
    unittest.main()
