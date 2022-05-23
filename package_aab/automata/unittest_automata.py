import unittest
from automata import Automata


class testAutomata(unittest.TestCase):
    def setUp(self):
        self.automata = Automata("AC", "ACA")


class testAutomataMethods(testAutomata):
    def runTest(self):
        self.assertEqual(self.automata.patternSeqPosition("CACAACAA"), [1, 4], "lista de posições errada")
        self.assertEqual(self.automata.applyNextState("CACAACAA"), [0, 0, 1, 2, 3, 1, 2, 3, 1],
                         "lista de próximos estados errada")


if __name__ == '__main__':
    unittest.main()
