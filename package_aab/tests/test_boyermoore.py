import unittest
from src.boyermoore import BoyerMoore

class test_BoyerMoore(unittest.TestCase):

    def setUp(self):
        alfabeto = 'ACTG'
        padrao = 'ACCA'
        self.boyermoore = BoyerMoore(alfabeto, padrao)

    def test_search_pattern(self):
        x = self.boyermoore.search_pattern("ATAGAACCAATGAACCATGATGAACCATGGATACCCAACCACC")
        y = [5, 13, 23, 37]
        self.assertEqual(x, y)


if __name__ == '__main__':
    unittest.main()

