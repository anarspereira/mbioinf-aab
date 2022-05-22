# -*- coding: utf-8 -*-
"""
Package de Métodos implementados nas aulas?
Algoritmos Avançados de Bioinformática
Grupo ?
"""

"""
Class: Automata
"""
class Automata:

    def __init__(self, alphabet: str, pattern: str):
        """
        Método que guarda os valores utilizados nos restantes métodos

        :param alphabet: guarda todos os caractéres presentes no texto
        :param pattern: padrão que queremos procurar
        """
        self.numstates = len(pattern) + 1 #guarda o comprimento do padrão
        self.alphabet = alphabet #todos os caractéres presentes no nosso texto
        self.transitionTable = {} #dicionário da tabela de transição
        self.buildTransitionTable(pattern) #guarda a tabela de transição

    def buildTransitionTable(self, pattern: str):
        """
        Método que constroi a tabela de transição. A tabela de transição devolve o próximo
        estado da máquima automata a partir do estado atual e estados anteriores.
        :param pattern: padrão que queremos procurar no text
        """
        for q in range(self.numstates):
            for a in self.alphabet:
                possible_pattern = pattern[0:q] + a #determina todos os padrões possíveis



        # ...

    def printAutomata(self):
        print("States: ", self.numstates)
        print("Alphabet: ", self.alphabet)
        print("Transition table:")
        for k in self.transitionTable.keys():
            print(k[0], ",", k[1], " -> ", self.transitionTable[k])

    def nextState(self, current, symbol):
        #return self.transitionTable.get((current, symbol)) #

    # return ...

    def applySeq(self, seq):
        q = 0
        res = [q]
        # ...
        return res

    def occurencesPattern(self, text):
        q = 0
        res = []
        # ....
        return res


def overlap(s1, s2):
    overlap_start = min(len(s1), len(s2)) #determina qual a sequência mais pequena para começar a sobreposição
    for i in range(overlap_start, 0, -1):
        if s1[-i:] == s2[:i]: return i
    return 0


def test():
    auto = Automata("AC", "ACA")
    auto.printAutomata()
    print(auto.applySeq("CACAACAA"))
    print(auto.occurencesPattern("CACAACAA"))


test()

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



