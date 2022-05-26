import unittest
from trie import Trie


class test_Trie(unittest.TestCase):
    def setUp(self) -> None:
        self.pat = ["AGAGAT", "AGC", "AGTCC", "CAGAT", "CCTA", "GAGAT", "GAT", "TC"]
        self.trie = Trie()


class test_TrieMethods(test_Trie):
    def test_trieFromPattern(self):
        x = self.trie.trie_from_patterns(self.pat)
        y = {[0: {'G': 1, 'C': 4}
1 -> {'A': 2}
2 -> {'T': 3, 'G': 7}
3 -> {}
4 -> {'C': 5}
5 -> {'T': 6}
6 -> {}
7 -> {}}


if __name__ == '__main__':
    unittest.main()