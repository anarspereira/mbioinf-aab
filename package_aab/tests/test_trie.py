import unittest
from trie import Trie


class test_Trie(unittest.TestCase):
    def setUp(self):
        patterns = ["AGAGAT", "AGC", "AGTCC", "CAGAT", "CCTA", "GAGAT", "GAT", "TC"]
        self.trie = Trie(patterns)


class test_TrieMethods(test_Trie):
    def test_runTest(self):
        self.assertEqual(self.trie.trie_from_patterns("GAGATCCTA"), "erro")
        self.assertEqual(self.trie.trie_matches("GAGATCCTA"), "erro")


if __name__ == '__main__':
    unittest.main()