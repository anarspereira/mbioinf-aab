# -*- coding: utf-8 -*-
"""
Package dos algoritmos implementados em aula
Algoritmos Avançados de Bioinformática
"""

"""
Class: MotifFinding
"""

from my_seq import MySeq
from my_motif import MyMotifs
from random import randint
from random import random


class MotifFinding:
    """
    Classe implementada para a procura de padrões recorrentes numa sequência biológica,
    que pode ser de DNA ou proteinas.
    O padrão a procurar pode ser uma sequência exata ou um consensus degenerado em que existem
    caractéres ambíguos.
    """

    def __init__(self, size: int = 8, seqs = None) -> None:
        """
        Método que guarda os valores utilizados nos restantes métodos.
        :param size: tamanho dos motifs a procurar
        :param seqs: lista de sequências a procurar
        """
        self.motifSize = size #guarda o tamanho
        if (seqs != None): #se a lista de sequências tiver sequências
            self.seqs = seqs
            self.alphabet = seqs[0].alphabet() #guarda o tipo de caracteres da sequência
        else:
            self.seqs = [] #lista das sequências

    def __len__(self) -> int:
        """
        Método que devolve o comprimento das sequências.
        :return: devolve o comprimento das sequências.
        """
        return len(self.seqs)

    def __getitem__(self, n: int) -> None:
        """
        Método que permite devolver um item a partir da indexação de uma instância.
        :param n: posição do valor que queremos devolver.
        :return: caractér da posição introduzida
        """
        return self.seqs[n]

    def seqSize(self, i: int) -> int:
        """
        Método que devolve o comprimento da sequência.
        :param i: index da sequência na lista de sequências.
        :return: comprimento da sequência com index i da lista de sequências.
        """
        return len(self.seqs[i])

    def readFile(self, file: str, type: str) -> None:
        """
        Método que lê o ficheiro de sequências.
        :param file: ficheiro das sequências.
        :param type: tipo das sequências
        """
        for seq in open(file, "r"): #por cada sequência no ficheiro
            self.seqs.append(MySeq(seq.strip().upper(), type)) #adiciona à lista de sequências da classe
        self.alphabet = self.seqs[0].alphabet() #identifica o tipo de sequências

    def createMotifFromIndexes(self, indexes: list):
        """
        Método que implementa motifs probabilísticos do tipo MyMotif.
        :param indexes: lista dos índices das posições iniciais dos motif
        das sub-sequências utilizadas para criar o motif.
        :return:
        """
        motif_subseq = [] #lista vazia para guardar as subsequências onde começam e acabam os motifs.
        for i, ind in enumerate(indexes): #por cada sequência correspondente ao motif a iniciar no index (ind)
            motif_subseq.append(MySeq(self.seqs[i][ind:(ind+self.motifSize)],
                               self.seqs[i].type))
            #adiciona à lista a sequência correspondente ao motid mais o tipo da sequência
        return MyMotifs(motif_subseq) #corre o método MyMotifs para a lista de

    def score(self, s: list) -> int:
        """
        Método implementado para a função de scoring.
        A função de scoring faz iterações de todas as posições do motif e determina o valor máximo
        do score do motif.
        :param s: lista de índices dos motifs nas sequências introduzidas.
        :return: score máximo do score do motif.
        """
        score = 0 #define o score inicial como zero
        motif = self.createMotifFromIndexes(s) #define o motif como o criando no método anterior
        motif.doCounts() #realiza a matriz de contagens dos motifs
        mat = motif.mat_count #define a matriz de contagens
        for j in range(len(mat[0])): #percorre as colunas da matriz
            maxcol = mat[0][j] #guarda o valor da primeira linha da coluna j
            for i in range(1, len(mat)): #percorre a coluna da matriz a partir do segundo elemento
                if mat[i][j] > maxcol: #verifica se o valor da célula é superior ao definido como o máximo da coluna
                    maxcol = mat[i][j] #se for, define um novo máximo
            score += maxcol #adiciona os scores máximos ao score total
        return score

    def scoreMult(self, s):
        """
        Método implementado para a multiplicação dos scores máximos do motif.
        :param s: lista de índices dos motifs nas sequências introduzidas.
        :return: multiplicação dos scores máximos
        """
        score = 1.0 #define o score inicial como 1
        motif = self.createMotifFromIndexes(s)
        motif.createPWM() #cria a PWM para o motif
        mat = motif.pwm #define a matriz
        for j in range(len(mat[0])):
            maxcol = mat[0][j]
            for i in range(1, len(mat)):
                if mat[i][j] > maxcol:
                    maxcol = mat[i][j]
            score *= maxcol #comparativamente ao último método, nesta linha o operador é de multiplicação em vez de soma

        return score

    def nextSol(self, s: list) -> list:
        """
        Método implementado para iterar sobre todos os possiveís valores da posição do motif na sequência introduzida.
        :param s: lista de índices dos motifs nas sequências introduzidas.
        :return: lista de todos os possíveis valores da posição do motif na sequência introduzida
        """
        nextS = [0]*len(s) #define a lista dos valores da próxima solução com valores de zeros
        #do comprimento dos índices já introduzidos
        pos = len(s) - 1 #define posição como o comprimento da lista de índices menos um
        while pos >= 0 and s[pos] == self.seqSize(pos) - self.motifSize: #enquanto a posição
            # for superior ou igual a zero e o index correspondente na lista de indices for igual ao tamanho
            #da sequência na posição pos menos o tamanho do motif
            pos -= 1 #decresce um index
        if (pos < 0): #se a posição for inferior a zero
            nextS = None #não existem possivéis valores da próxima solução
        else: #se a posição não for inferior a zerp
            for i in range(pos): #percorre os possiveís valores
                nextS[i] = s[i] #
            nextS[pos] = s[pos]+1
            for i in range(pos+1, len(s)):
                nextS[i] = 0
        return nextS

    def exhaustiveSearch(self):
        melhorScore = -1
        res = []
        s = [0] * len(self.seqs)
        while (s != None):
            sc = self.score(s)
            if (sc > melhorScore):
                melhorScore = sc
                res = s
            s = self.nextSol(s)
        return res

    # BRANCH AND BOUND

    def nextVertex(self, s):
        res = []
        if len(s) < len(self.seqs):  # internal node -> down one level
            for i in range(len(s)):
                res.append(s[i])
            res.append(0)
        else:  # bypass
            pos = len(s)-1
            while pos >= 0 and s[pos] == self.seqSize(pos) - self.motifSize:
                pos -= 1
            if pos < 0:
                res = None  # last solution
            else:
                for i in range(pos):
                    res.append(s[i])
                res.append(s[pos]+1)
        return res

    def bypass(self, s):
        res = []
        pos = len(s) - 1
        while pos >= 0 and s[pos] == self.seqSize(pos) - self.motifSize:
            pos -= 1
        if pos < 0:
            res = None
        else:
            for i in range(pos):
                res.append(s[i])
            res.append(s[pos]+1)
        return res

    def branchAndBound(self):
        melhorScore = -1
        melhorMotif = None
        size = len(self.seqs)
        s = [0]*size
        while s != None:
            if len(s) < size:
                optimScore = self.score(s) + (size-len(s)) * self.motifSize
                if optimScore < melhorScore:
                    s = self.bypass(s)
                else:
                    s = self.nextVertex(s)
            else:
                sc = self.score(s)
                if sc > melhorScore:
                    melhorScore = sc
                    melhorMotif = s
                s = self.nextVertex(s)
        return melhorMotif

    # Consensus (heuristic)

    def heuristicConsensus(self):
        """ Procura as posições para o motif nas duas primeiras sequências """
        mf = MotifFinding(self.motifSize, self.seqs[:2])
        s = mf.exhaustiveSearch()
        for a in range(2,
                       len(self.seqs)):
            s.append(0)
            melhorScore = -1
            melhorPosition = 0
            for b in range(self.seqSize(a) - self.motifSize + 1):
                s[a] = b
                scoreatual = self.score(s)
                if scoreatual > melhorScore:
                    melhorScore = scoreatual
                    melhorPosition = b
                s[a] = melhorPosition
        return s


    def heuristicStochastic(self):
        s = [0] * len(self.seqs)
        for i in range(len(self.seqs)):
            s[i] = randint(0, self.seqSize(
                i) - self.motifSize)
        melhorscore = self.score(s)
        improve = True
        while improve:
            motif = self.createMotifFromIndexes(s)
            motif.createPWM()
            for i in range(len(self.seqs)):
                s[i] = motif.mostProbableSeq(self.seqs[i])
            scr = self.score(s)
            if scr > melhorscore:
                melhorscore = scr
            else:
                improve = False
        return s

    def gibbs(self, num_iterations :int):
        s = []
        for i in range(len(self.seqs)):
            s.append(randint(0, len(
                self.seqs[i]) - self.motifSize - 1))
        melhorscore = self.score(s)
        bests = list(s)
        for it in range(num_iterations):
            seq_idx = randint(0, len(self.seqs) - 1)
            seq = self.seqs[seq_idx]
            s.pop(seq_idx)
            removed = self.seqs.pop(seq_idx)
            motif = self.createMotifFromIndexes(s)
            motif.createPWM()
            self.seqs.insert(seq_idx,removed)
            r = motif.probAllPositions(seq)
            pos = self.roulette(r)
            s.insert(seq_idx, pos)
            score = self.score(s)
            if score > melhorscore:
                melhorscore = score
                bests = list(s)
        return bests

    def roulette(self, f):
        tot = 0.0
        for x in f:
            tot += (0.01+x)
        val = random() * tot
        acum = 0.0
        ind = 0
        while acum < val:
            acum += (f[ind] + 0.01)
            ind += 1
        return ind-1


# tests

def test1():
    sm = MotifFinding()
    sm.readFile("exemploMotifs.txt", "dna")
    sol = [25, 20, 2, 55, 59]
    sa = sm.score(sol)
    print(sa)
    scm = sm.scoreMult(sol)
    print(scm)


def test2():
    print("Test exhaustive:")
    seq1 = MySeq("ATAGAGCTGA", "dna")
    seq2 = MySeq("ACGTAGATGA", "dna")
    seq3 = MySeq("AAGATAGGGG", "dna")
    mf = MotifFinding(3, [seq1, seq2, seq3])
    sol = mf.exhaustiveSearch()
    print("Solution", sol)
    print("Score: ", mf.score(sol))
    print("Consensus:", mf.createMotifFromIndexes(sol).consensus())

    print("Branch and Bound:")
    sol2 = mf.branchAndBound()
    print("Solution: ", sol2)
    print("Score:", mf.score(sol2))
    print("Consensus:", mf.createMotifFromIndexes(sol2).consensus())

    print("Heuristic consensus: ")
    sol1 = mf.heuristicConsensus()
    print("Solution: ", sol1)
    print("Score:", mf.score(sol1))


def test3():
    mf = MotifFinding()
    mf.readFile("exemploMotifs.txt", "dna")
    print("Branch and Bound:")
    sol = mf.branchAndBound()
    print("Solution: ", sol)
    print("Score:", mf.score(sol))
    print("Consensus:", mf.createMotifFromIndexes(sol).consensus())


def test4():
    mf = MotifFinding()
    mf.readFile("exemploMotifs.txt", "dna")
    print("Heuristic stochastic")
    sol = mf.heuristicStochastic()
    print("Solution: ", sol)
    print("Score:", mf.score(sol))
    print("Score mult:", mf.scoreMult(sol))
    print("Consensus:", mf.createMotifFromIndexes(sol).consensus())

    sol2 = mf.gibbs(1000)
    print("Score:", mf.score(sol2))
    print("Score mult:", mf.scoreMult(sol2))