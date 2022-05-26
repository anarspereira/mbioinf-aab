import unittest
from src.boyermoore import BoyerMoore

class test_BoyerMoore(unittest.TestCase):

    def setUp(self):
        alfabeto = 'ACTG'
        padrao = 'ACCA'
        self.boyermoore = BoyerMoore(alfabeto, padrao)

    def test_search_pattern(self):
        x = self.boyermoore.search_pattern("ATAGAACCAATGAACCATGATGAACCATGGATACCCAACCACC")
        y = '[1, 7, 8, 9, 10, 6, 2, 3, 4, 5, 0]'
        self.assertEqual(x, y)


if __name__ == '__main__':
    unittest.main()

