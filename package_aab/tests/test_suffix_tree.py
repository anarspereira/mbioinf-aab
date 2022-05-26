import unittest
from suffix_tree import SuffixTree

class test_SuffixTree(unittest.TestCase):
    def setUp(self):
        self.suffixtree = SuffixTree()
        #suffix_tree_from_seq("TACTA")


class test_SuffixTreeMethods(test_SuffixTree):
    def test_findPattern(self):
        x = self.suffixtree.find_pattern("TA")
        y = None
        self.assertEqual(x, y)


if __name__ == '__main__':
    unittest.main()