# -*- coding: utf-8 -*-
"""
Package dos algoritmos implementados em aula
Algoritmos Avançados de Bioinformática
"""

"""
Class: MyMotifs
"""


def createMatZeros(line_num: int, col_num: int) -> list:
    """
    Método para criar uma matriz de zeros
    :param line_num: número de linhas da matriz
    :param col_num: número de colunas da matriz
    :return: matriz de zeros
    """
    mat_z = [] #lista vazia para criar a matriz de zeros
    for i in range(0, line_num): #por cada linha de zero ao número de linhas desejado
        mat_z.append([0]*col_num) #adiciona um zero col_num vezes
    return mat_z


def printMat(mat: list):
    """
    Método utilizado para imprimir a matriz.
    :param mat: matriz a imprimir
    """
    for i in range(0, len(mat)): #por cada índice da lista da matriz
        print(mat[i]) #imprime o valor correspondente


class MyMotifs:
    """
    Classe que apresenta os métodos que permitem a manipulação e procura de padrões recorrentes (motifs) em sequências biológicas,
    matrizes de padrões probabilísticos (PWM).
    """

    def __init__(self, seqs: list = [], pwm: list = [], alphabet: str = None):
        """
        Método que guarda os valores utilizados nos restantes métodos.
        :param seqs: lista de sequências introduzidas
        :param pwm: matriz de probabilidades
        :param alphabet: tipo de caracteres da sequência introduzida
        """
        if seqs: #se o parâmetro introduzido for uma sequência, tem de ter as seguintes instâncias.
            self.size = len(seqs[0]) #comprimento das sequências
            self.seqs = seqs  #objetos da classe MySeq
            self.alphabet = seqs[0].checkSeqType() #objeto da classe Myseq, verifica o tipo
            self.doCounts() #cria a matriz de contagens dos caractéres das sequências
            self.createPWM() #cria a matriz de PWN (matriz de probabilidades)
        else: #se o parâmetro introduzido não for uma sequência é uma PWM
            self.pwm = pwm
            self.size = len(pwm[0]) #comprimento do primeiro valor da lista
            self.alphabet = alphabet #tipo de caracteres da sequência introduzida

    def __len__(self):
        """
        Método que devolve o comprimento das sequências.
        """
        return self.size

    def doCounts(self):
        """
        Método que implementa as matrizes de contagens.
        """
        self.mat_count = createMatZeros(len(self.alphabet), self.size) #define uma instância correspondente
        #à matriz probabilística, em que o número de linhas é o número de caracteres do alfabeto e o número
        #de colunas é o comprimento da sequência.
        for char in self.seqs: #para cada caractér na sequência
            for i in range(self.size): #
                lin = self.alphabet.index(char[i])
                self.mat_count[lin][i] += 1

    def createPWM(self):
        if self.mat_count == None:
            self.doCounts()
        self.pwm = createMatZeros(len(self.alphabet), self.size)
        for i in range(len(self.alphabet)):
            for j in range(self.size):
                self.pwm[i][j] = float(self.mat_count[i][j]) / len(self.seqs)

    def consensus(self):
        res = ""
        for j in range(self.size):
            maxcol = self.mat_count[0][j]
            maxcoli = 0
            for i in range(1, len(self.alphabet)):
                if self.mat_count[i][j] > maxcol:
                    maxcol = self.mat_count[i][j]
                    maxcoli = i
            res += self.alphabet[maxcoli]
        return res

    def maskedConsensus(self):
        res = ""
        for j in range(self.size):
            maxcol = self.mat_count[0][j]
            maxcoli = 0
            for i in range(1, len(self.alphabet)):
                if self.mat_count[i][j] > maxcol:
                    maxcol = self.mat_count[i][j]
                    maxcoli = i
            if maxcol > len(self.seqs) / 2:
                res += self.alphabet[maxcoli]
            else:
                res += "-"
        return res

    def probabSeq(self, seq):
        res = 1.0
        for i in range(self.size):
            lin = self.alphabet.index(seq[i])
            res *= self.pwm[lin][i]
        return res

    def probAllPositions(self, seq):
        res = []
        for _ in range(len(seq)-self.size+1):
            res.append(self.probabSeq(seq))
        return res

    def mostProbableSeq(self, seq):
        maximo = -1.0
        maxind = -1
        for k in range(len(seq)-self.size):
            p = self.probabSeq(seq[k:k + self.size])
            if(p > maximo):
                maximo = p
                maxind = k
        return maxind


def test():
    # test
    from my_seq import MySeq
    seq1 = MySeq("AAAGTT", "dna")
    seq2 = MySeq("CACGTG", "dna")
    seq3 = MySeq("TTGGGT", "dna")
    seq4 = MySeq("GACCGT", "dna")
    seq5 = MySeq("AACCAT", "dna")
    seq6 = MySeq("AACCCT", "dna")
    seq7 = MySeq("AAACCT", "dna")
    seq8 = MySeq("GAACCT", "dna")
    lseqs = [seq1, seq2, seq3, seq4, seq5, seq6, seq7, seq8]
    motifs = MyMotifs(lseqs)
    printMat(motifs.counts)
    printMat(motifs.pwm)
    print(motifs.alphabet)

    print(motifs.probabSeq("AAACCT"))
    print(motifs.probabSeq("ATACAG"))
    print(motifs.mostProbableSeq("CTATAAACCTTACATC"))

    print(motifs.consensus())
    print(motifs.maskedConsensus())


if __name__ == '__main__':
    test()