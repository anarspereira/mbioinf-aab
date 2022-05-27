import unittest
from src.indiv import *


class TestIndiv(unittest.TestCase):

    def setUp(self):
        genes = []
        size = 2
        self.indiv = Indiv(size, genes)

    def test_crossover(self):
        x = self.indiv.crossover([0, 1])
        y = any, any
        self.assertEqual(x, y)


if __name__ == '__main__':
    unittest.main()
