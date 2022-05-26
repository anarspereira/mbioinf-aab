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
    for lin in range(len(mat)):
        for col in range(len(mat[lin])):
            print(mat[lin][col], end=' ')
        print()


class MyMotifs:
    """
    Classe que apresenta os métodos que permitem a manipulação e procura de padrões recorrentes (motifs)
    em sequências biológicas e a realização de matrizes de padrões probabilísticos (PWM).
    """

    def __init__(self, lseqs: list = [], pwm: list = [], alphabet: str = None):
        """
        Método que guarda os valores utilizados nos restantes métodos.
        :param lseqs: lista de sequências de sequências introduzidas
        :param pwm: matriz de probabilidades
        :param alphabet: tipo de caracteres da sequência introduzida
        """
        if lseqs: #se o parâmetro introduzido for uma sequência, tem de ter as seguintes instâncias.
            self.size = len(lseqs[0]) #comprimento dos caracteres das sequências
            self.seqs = lseqs  #objetos da classe MySeq
            self.alphabet = lseqs[0].checkSeqType() #objeto da classe Myseq, verifica o tipo
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
        for seq in self.seqs: #para cada sequência na lista de sequências
            for i in range(self.size): #para cada índice da sequência
                lin = self.alphabet.index(seq[i]) #as linhas da matriz correspondem à ordem dos caracteres no alfabeto
                self.mat_count[lin][i] += 1 #incrementa para fazer o resto da matriz

    def createPWM(self):
        """
        Método que cria a matriz probabilística. As PWM são representações probabilística dos caracteres
        em sequências biológicas, ou seja, calcula a probabilidade do nucleótido i ser encontrado na posição j.
        """
        if self.mat_count == None: #se a matriz de contagens não tiver sido feita
            self.doCounts() #fazer matriz de contagens
        self.pwm = createMatZeros(len(self.alphabet), self.size) #cria uma matriz de zeros para estruturar a PWM
        for i in range(len(self.alphabet)): #percorre o tipo de caracteres da sequência
            for j in range(self.size): #percorre a sequência
                self.pwm[i][j] = float(self.mat_count[i][j]) / len(self.seqs)
                #calcula a probabilidade para cada célula através da fórmula:
                # contagens verificadas / número de sequências.

    def consensus(self):
        """
        Método que gera uma sequência consensus. As sequências consensus guarda os caractéres mais conservados
        em cada posição do padrão, ou seja, o valor mais alto de cada coluna da matriz de contagens.
        :return: string da sequência consensus.
        """
        cons_seq = "" #abre uma string vazia para introduzir a sequência de caracteres
        for j in range(self.size): #percorre as colunas da matriz que tem o mesmo comprimento que a sequência
            max_col = self.mat_count[0][j] #retorna o valor da primeira linha da coluna j
            index_maxval = 0 #define como valor inicial
            for i in range(1, len(self.alphabet)): #percorre todas as linhas, ou seja,
                # os caracteres do tipo de sequência
                if self.mat_count[i][j] > max_col: #se o valor da contagem for superior ao último valor guardado
                    max_col = self.mat_count[i][j] #devolve o valor em causa
                    index_maxval = i #guarda o index do caractér com maior valor de contagem
            cons_seq += self.alphabet[index_maxval] #adiciona à string o caractér
        return cons_seq

    def maskedConsensus(self):
        """
        Método que gera a sequência consensus que é obtida com com os caracteres
        que têm uma incidência superior a 50%.
        :return: string da sequência consensus com incidência superior a 50%.
        """
        cons_seq = "" #abre uma string vazia para introduzir a sequência de caracteres
        for j in range(self.size): #percorre as colunas da matriz que tem o mesmo comprimento que a sequência
            max_col = self.mat_count[0][j] #retorna o valor da primeira linha da coluna j
            index_maxval = 0 #define como valor inicial
            for i in range(1, len(self.alphabet)): #percorre todas as linhas, ou seja,
                # os caracteres do tipo de sequência
                if self.mat_count[i][j] > max_col: #se o valor da contagem for superior ao último valor guardado
                    max_col = self.mat_count[i][j] #devolve o valor em causa
                    index_maxval = i #guarda o index do caractér com maior valor de contagem
            if max_col > len(self.seqs) / 2: #se o valor máximo da coluna for superior a metade do número de sequências
                cons_seq += self.alphabet[index_maxval] #devolve o caractér
            else:
                cons_seq += "-" #se não tiver uma incidência superior a 50% não devolve um caracter
        return cons_seq

    def probabSeq(self, seq):
        """
        Método que calcula a probabilidade de um padrão ser encontrado numa sequência.
        :param seq: sequência introduzida
        :return: a probabilidade de um padrão ser encontrado na sequência
        """
        prob = 1.0 #define a probabilidade inicial como 1
        for i in range(self.size): #percorre a sequência de zero até ao comprimento das sequências introduzidas
            lin = self.alphabet.index(seq[i]) #as linhas da matriz correspondem à ordem dos caracteres no alfabeto
            prob *= self.pwm[lin][i] #multiplica o valor da célula pelo valor inicialmente definido
        return prob

    def probAllPositions(self, seq):
        """
        Método implementado para calcular a probabilidade de encontrar padrões em sequências mais longas
        e calcular a probabilidade de o padrão ocorrer a cada caracter da sequência, ou seja,
        de ocorrer a cada sub-sequência do tamanho do padrão.
        :param seq: sequência introduzida
        :return: lista de probabilidades do padrão ocorrer a cada subsequência
        """
        subseq_prob = [] #lista vazia para devolver as probabilidades
        for i in range(len(seq)-self.size + 1): #percorre a da sequência introduzida menos o comprimento do padrão
            #mais um, de forma a percorrer a totalidade da sequência até atingir uma correspondência
            subseq_prob.append(self.probabSeq(seq)) #adiciona a probabilidade em lista
        return subseq_prob

    def mostProbableSeq(self, seq):
        """
        Método implementado para determinar a sub-sequência com a maior probabilidade de corresponder
        ao padrão em procura.
        :param seq: sequência introduzida
        :return: o índice da sub-sequência com maior probabilidade de correpsonder ao padrão em procura.
        """
        max_p = - 1.0 #define o mínimo da probabilidade
        max_ind = - 1 #define o valor inicial para o índice com maior probabilidade
        for k in range(len(seq)-self.size): #percorre a totalidade da sequência menos o comprimento do padrão
            p = self.probabSeq(seq[k:k + self.size]) #calcula a probabilidade de encontra na sub-sequência correspondete
            #da posição k à posição k + o comprimento da
            if (p > max_p): #se a probabilidade for superior a - 1.0
                max_p = p #define p como a probabilidade máxima
                max_ind = k #define o índice atual como o índice com o valor máximo de probabilidade
        return max_ind