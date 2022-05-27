# -*- coding: utf-8 -*-
"""
Package dos algoritmos implementados em aula
Algoritmos Avançados de Bioinformática
"""

"""
Unit test: EA Motifs
"""

import unittest
from EA_motifs import EAMotifsInt
from EA_motifs import EAMotifsReal


class test_EAMotifs(unittest.TestCase):
    def setUp(self):
        self.ea_motifs = EA_motifs()

class test_EAMotifsMethods(test_SuffixTree):

    def test_EAMotifsInt(self):
        x = self.EAMotifsInt(100, 1000, 50, "exemploMotifs.txt") # pedem um ficheiro .txt, está na pasta dos scripts
        #y =
        self.assertEqual(x, y)


if __name__ == '__main__':
    unittest.main()
