import unittest
from automata import Automata


class test_Automata(unittest.TestCase):
    def setUp(self):
        self.automata = Automata("AC", "ACA")


class test_AutomataMethods(test_Automata):
    def test_runTest(self):
        self.assertEqual(self.automata.patternSeqPosition("CACAACAA"), [1, 4], "lista de posições errada")
        self.assertEqual(self.automata.applyNextState("CACAACAA"), [0, 0, 1, 2, 3, 1, 2, 3, 1],
                         "lista de próximos estados errada")


if __name__ == '__main__':
    unittest.main()

# States:  4
# Alphabet:  AC
# Transition table:
# 0 , A  ->  1
# 0 , C  ->  0
# 1 , A  ->  1
# 1 , C  ->  2
# 2 , A  ->  3
# 2 , C  ->  0
# 3 , A  ->  1
# 3 , C  ->  2
# [0, 0, 1, 2, 3, 1, 2, 3, 1]
# [1, 4]
