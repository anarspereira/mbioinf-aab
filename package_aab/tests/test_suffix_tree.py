import unittest
from suffix_tree import SuffixTree

class test_SuffixTree(unittest.TestCase):
    def setUp(self):
        self.seq = "TACTA"
        self.suffixtree = SuffixTree()
        self.suffixtree.suffix_tree_from_seq(self.seq)


class test_SuffixTreeMethods(test_SuffixTree):
    # def test_printSuffixTree(self):
    # x = self.suffixtree.print_trie()
    #     y = ["0 -> {'T': 1, 'A': 7, 'C': 12, '$': 18}",
    #          "1 -> {'A': 2}",
    #          "2 -> {'C': 3, '$': 16}",
    #          "3 -> {'T': 4}",
    #          "4 -> {'A': 5}",
    #          "5 -> {'$': 6}",
    #          "6 : 0",
    #          "7 -> {'C': 8, '$': 17}",
    #          "8 -> {'T': 9}",
    #          "9 -> {'A': 10}",
    #          "10 -> {'$': 11}",
    #          "11 : 1",
    #          "12 -> {'T': 13}",
    #          "13 -> {'A': 14}",
    #          "14 -> {'$': 15}",
    #          "15 : 2",
    #          "16 : 3",
    #          "17 : 4",
    #          "18 : 5"]
    #     self.assertEqual(x, y)


    def test_findPattern(self):
        x = self.suffixtree.find_pattern("TA")
        y = "[0, 3]"
        self.assertEqual(str(x), y)


if __name__ == '__main__':
    unittest.main()