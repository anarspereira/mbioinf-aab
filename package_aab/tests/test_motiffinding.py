import unittest
from my_seq import MySeq
from my_motif import MyMotifs
from random import randint
from random import random
from motif_finding import MotifFinding


class test_MotifFinding(unittest.TestCase):
    def setUp(self):
        self.seq1 = MySeq("ATAGAGCTGA", "dna")
        self.seq2 = MySeq("ACGTAGATGA", "dna")
        self.seq3 = MySeq("AAGATAGGGG", "dna")
        self.mf = MotifFinding(3, [self.seq1, self.seq2, self.seq3])

    def test_exhaustiveSearch(self):
        x = self.mf.exhaustiveSearch()
        y = "[1, 3, 4]"
        self.assertEqual(str(x), y)

    def test_score(self):
        sol = [1, 3, 4]
        x = self.mf.score(sol)
        y = "9"
        self.assertEqual(str(x), y)

    def test_consensus(self):
        sol = [1, 3, 4]
        x = self.mf.createMotifFromIndexes(sol).consensus()
        y = "TAG"
        self.assertEqual(str(x), y)

    def test_heuristicConsensus(self):
        sol = self.mf.heuristicConsensus()
        x = self.mf.score(sol)
        y = "9"
        self.assertEqual(str(x),y)

if __name__ == '__main__':
    unittest.main()
