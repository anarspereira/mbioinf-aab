# -*- coding: utf-8 -*-
"""
Package dos algoritmos implementados em aula
Algoritmos Avançados de Bioinformática
"""

"""
Class: Automata
"""

class Automata:

    def __init__(self, alphabet: str, pattern: str):
        """
        Método que guarda os valores utilizados nos restantes métodos

        :param alphabet: guarda todos os caractéres presentes na sequência
        :param pattern: padrão que queremos procurar
        """
        self.numstates = len(pattern) + 1 #guarda o comprimento do padrão
        self.alphabet = alphabet #todos os caractéres presentes na nossa sequência
        self.transitionTable = {} #dicionário da tabela de transição
        self.buildTransitionTable(pattern) #guarda a tabela de transição

    def buildTransitionTable(self, pattern: str):
        """
        Método que constroi a tabela de transição. A tabela de transição devolve o próximo
        estado da máquima automata a partir do estado atual e estados anteriores.
        :param pattern: padrão que queremos procurar na sequência
        """
        for char_p in range(self.numstates): #for loop para leitura de todos os caractéres do padrão
            for char in self.alphabet: #for loop para leitura dos caractéres do alfabeto
                possible_pattern = pattern[:char_p] + char #determina todos os padrões possíveis
                match_next_state = overlap(possible_pattern, pattern)
                #guarda a sequência que deu match entre o padrão e os possíveis padrões
                self.transitionTable[(char_p, char)] = match_next_state
                #guarda um dicionário em que cada linha é um tuplo com o valor de q e char

    def printAutomata(self):
        """
        Método que imprime os resultados.
        """
        print("States: ", self.numstates)
        print("Alphabet: ", self.alphabet)
        print("Transition table:")
        for keys in self.transitionTable.keys():
            print("[", keys[0], "|", keys[1], " -> ", self.transitionTable[keys], "]")

    def nextState(self, current: int, char: str) -> int:
        """
        Método que devolve o próximo estado.
        :param current: estado atual
        :param char: caractér do padrão a procurar
        :return: o próximo estado
        """
        return self.transitionTable.get((current, char))

    def applyNextState(self, seq: str) -> list:
        """
        Método que devolve uma lista de todos os próximos estados.
        :param seq: sequência introduzida
        :return: lista dos próximos estados
        """
        state = 0  # determina o estado zero
        next_state_list = [state]  # cria uma lista para guardar todas os próximos estados
        for char in seq:  # for loop para a leitura de todos os caractéres da sequência
            state = self.nextState(state, char)
            # determina o próximo estado a partir do estado atual e do caractér atual
            next_state_list.append(state)  # adiciona à lista next_state_list todas os próximos estados
        return next_state_list

    def patternSeqPosition(self, seq: str) -> list:
        """
        Método que devolve a lista das posições onde se inicia uma ocorrência do padrão na sequência.
        :param seq: sequência introduzida
        :return: lista das posições onde se inicia uma ocorrência do padrão na sequência
        """
        state = 0 # determina o estado zero
        ocurences_list = [] # cria uma lista para guardar as posições de ocorrências
        for i in range(len(seq)): #for loop para leitura de todas as posições da sequência
            state = self.nextState(state, seq[i])
            # determina o próximo estado a partir do estado atual e da posição do caractér da sequência
            if state == self.numstates - 1:
                #determina se o último estado é igual ao comprimento do padrão
                ocurences_list.append(i - self.numstates + 2)
                #adiciona à lista as posições em que inicia uma correspondência do padrão
                #estes cálculos são necessários para obter a posição inicial do padrão encontrado
        return ocurences_list

def overlap(seq1: str, seq2: str) -> int:
    """
    Método que sobrepõe duas sequências e verifica a correspondência
    :param seq1: primeira sequência
    :param seq2: segunda sequência
    :return: última posição da sequência mais pequena que corresponde a um match
    """
    overlap_start = min(len(seq1), len(seq2)) #determina qual a sequência mais pequena para começar a sobreposição
    for i in range(overlap_start, 0, -1):
        #for loop para leitura da sequência mais pequena a partir da última posição
        #acaba o loop na primeira posição e incrementa um valor de -1
        #ou seja, lê a sequência de trás para a frente
        if seq1[-i:] == seq2[:i]:
            # verifica se há correspondência entre o último caractér da primeira sequência
            # e o primeiro caractér da segunda sequência
            return i
    return 0 #se não houver match devolve um zero

class testAutomata(unittest.TestCase):
    def setUp(self):
        self.automata = Automata("AC", "ACA")

class testAutomataMethods(testAutomata):
    def runTest(self):
        self.assertEqual(self.automata.patternSeqPosition("CACAACAA"), [1, 4],"lista de posições errada" )
        self.assertEqual(self.automata.applyNextState("CACAACAA"), [0, 0, 1, 2, 3, 1, 2, 3, 1],
                         "lista de próximos estados errada")

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



