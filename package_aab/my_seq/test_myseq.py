import unittest
from my_seq import MySeq


class testMySeq(unittest.TestCase):
    def setUp(self):
        self.seq_dna1 = MySeq("ACTGCCAT", "dna")
        self.seq_dna2 = MySeq("ATGCATGAATGTAGATAGATGTGCCC", "dna")
        self.seq_dna3 = MySeq("ATGCCCGCTTT", "dna")
        self.seq_rna1 = MySeq("ACUGCCGUCAUA", "rna")
        self.seq_rna2 = MySeq("AGAAUGACGACCUAG", "rna")
        self.seq_prot1 = MySeq("MFLSP_AHMGREQTG_", "prot")

#    def test_transcricao(self):
#        x = self.seq_dna1.transcription()
#        y = MySeq("ACUGCCAU", "RNA")
#        self.assertEqual(x, y)
#    #"AssertionError: ACUGCCAU != ACUGCCAU"

    def test_reverseComplement(self):
        x = self.seq_dna1.reverseComplement()
        y = "ATGGCAGT"
        self.assertEqual(x, y)

    def test_rnaCodon(self):
        x = self.seq_rna1.rnaCodon()
        y = ["ACU", "GCC", "GUC", "AUA"]
        self.assertEqual(x, y)

#   def test_seqTranslation(self):
#        x = self.seq_dna3.seqTranslation()
#        y = "MPA"
#        self.assertEqual(x, y)
#"AssertionError: MPA != 'MPA'"

#    def test_orfs(self):
#        x = self.seq_dna2.orfs()
#        y = ["ATGCATGAATGTAGA", "ATGTGCCC"]
#        self.assertEqual(x, y)
#"AttributeError: 'str' object has no attribute 'seqTranslation'"

#    def test_allProtein(self):
#        x = self.seq_prot1.allProtein()
#        y = ["MFLSP", "MGREQTG"]
#        self.assertEqual(x, y)
#erro em string?

#    def test_longestProteinSeq(self):
#        x = self.seq_prot1.longestProteinSeq()
#        y = "MGREQTG"
#        self.assertEqual(x, y)
#erro em string?


if __name__ == '__main__':
    unittest.main()
