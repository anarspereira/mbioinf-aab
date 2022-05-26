import unittest
from boyermoore import BoyerMoore

class test_BoyerMoore(unittest.TestCase):

    def setUp(self):
        alphabet = 'ACTG'
        pattern = 'ACCA'
        self.boyermoore = BoyerMoore(alphabet, pattern)

    def test_search_pattern(self):
        x = self.boyermoore.search_pattern("ATAGAACCAATGAACCATGATGAACCATGGATACCCAACCACC")
        y = [5, 13, 23, 37]
        self.assertEqual(x, y)


if __name__ == '__main__':
    unittest.main()

