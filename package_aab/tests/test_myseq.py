import unittest
from my_seq import MySeq


class test_MySeq(unittest.TestCase):
    def setUp(self):
        self.seq_dna1 = MySeq("ACTGCCAT", "dna")
        self.seq_dna2 = MySeq("ATGCATGAAT", "dna")
        self.seq_dna3 = MySeq("ATGCCCGCTTT", "dna")
        self.seq_rna1 = MySeq("ACUGCCGUCAUA", "rna")
        self.seq_rna2 = MySeq("AGAAUGACGACCUAG", "rna")
        self.seq_prot1 = MySeq("MFLSP_AHMGREQTG_", "prot")

    def test_transcricao(self):
        X = self.seq_dna1.transcription()
        Y = "ACUGCCAU"
        self.assertEqual(str(X), Y)


    def test_reverseComplement(self):
        X = self.seq_dna1.reverseComplement()
        Y = "ATGGCAGT"
        self.assertEqual(str(X), Y)

    def test_rnaCodon(self):
        X = self.seq_rna1.rnaCodon()
        Y = ["ACU", "GCC", "GUC", "AUA"]
        self.assertEqual(X, Y)

    def test_seqTranslation(self):
        X = self.seq_dna3.seqTranslation()
        Y = "MPA"
        self.assertEqual(str(X), Y)

    def test_orfs(self):
        X = self.seq_dna2.orfs()
        Y = ["MHE", "CMN", "A_", "IHA", "FMH", "SC"]
        for test, truth in zip(X, Y):
            self.assertEqual(str(test), truth)

    def test_allProtein(self):
        X = self.seq_prot1.allProtein()
        Y = ["MFLSP", "MGREQTG"]
        for test, truth in zip(X, Y):
            self.assertEqual(str(test), truth)

    def test_longestProteinSeq(self):
        X = self.seq_prot1.longestProteinSeq()
        Y = "MGREQTG"
        self.assertEqual(str(X), Y)


if __name__ == '__main__':
    unittest.main()
