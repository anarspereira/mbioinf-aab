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
from typing import Union
from typing import List


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
            self.seq_type = seqs[0].checkSeqType() #guarda o tipo de caracteres da sequência
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
        self.seq_type = self.seqs[0].checkSeqType() #identifica o tipo de sequências

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
                               self.seqs[i].seq_type))
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
                nextS[i] = s[i] #igual a lista de possíveis index à lista de index para a mesma posição
            nextS[pos] = s[pos] + 1 #incrementa a última posição da lista de index mais um
            for i in range(pos+1, len(s)): #percore a lista de indices
                nextS[i] = 0 #acrescenta um zero à lista de possiveís indices na posição i
                #se esta não tiver os valores completos da lista de indices
        return nextS

    def exhaustiveSearch(self) -> list:
        """
        Método implementado para encontrar o motif com o vetor de melhor scores.
        Este método permite derivar o perfil e a sequência consensus.
        :return: vetor de melhor scores
        """
        best_score = -1 #define o melhor score como - 1
        score_vect = [] #cria uma lista para o vetor de scores
        s = [0] * len(self.seqs) #cria uma lista de zeros para os index das sequências
        while (s != None): #enquanto a lista de sequências não estiver vazia
            sc = self.score(s) #define os scores da lista de index
            if (sc > best_score): #verifica se os scores determinados são superiores ao scores definido
                best_score = sc #se sim, define como melhor score
                score_vect = s #se forem iguais, define a lista de melhores scores como a lista de ìndices
            s = self.nextSol(s) #se i score for inferior ao melhor score procura a próxima solução
        return score_vect

    def nextVertex(self, s: list) -> list:
        """
        Método implementado para encontrar o próximo vértice.
        :param s: lista de índices dos motifs nas sequências introduzidas.
        :return: lista de próximos vértices
        """
        vert_list = [] #cria uma lista vazia
        if len(s) < len(self.seqs):
            #se o comprimento da lista de índices for menor que o comprimento de sequências
            #significa que à partida todas as sequências estão incluidas
            #devolvendo a lista como a lista de vértices
            for i in range(len(s)): #percorre a lista
                vert_list.append(s[i]) #adiciona o index da posição i à lista
            vert_list.append(0) #adiciona um valor de 0 a mais
        else: #se for superior -> explicado no método anterior
            pos = len(s) - 1
            while pos >= 0 and s[pos] == self.seqSize(pos) - self.motifSize:
                pos -= 1
            if pos < 0:
                vert_list = None  # last solution
            else:
                for i in range(pos):
                    vert_list.append(s[i])
                vert_list.append(s[pos] + 1)
        return vert_list

    def bypass(self, s: list) -> list:
        """
        Método implementado para fazer bypass da condição explicada anteriormente.
        :param s: lista de índices dos motifs nas sequências introduzidas.
        :return: lista de índice com zeros nas posições não correpondentes
        """
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

    def branchAndBound(self) -> Union[list, List[int], None]:
        """
        Método implementado para iterar sobre a posição inicial da lista de soluções para encontrar o melhor motif.
        :return:
        """
        best_score = -1 #define o melhor score inicial
        best_motif = None #define o melhor motif inicial como None
        size = len(self.seqs)
        s = [0] * size # cria uma lista de zeros para os index das sequências
        while s != None: #se a lista não estiver vazia
            if len(s) < size: #se o comprimento da lista de index for inferior ao número de sequências
                optimScore = self.score(s) + (size-len(s)) * self.motifSize #o score ótimo é iguao aos scores mais
                #a soma da multiplicação do comprimento das sequências menos a lista de index vezes o tamanho do motif
                if optimScore < best_score: #se o score ótimo for menor que o melhor score
                    s = self.bypass(s) #bypass
                else: #se for superior
                    s = self.nextVertex(s) #procura a melhor solução
            else: #se o comprimento da lista de index for superior ao tamanho das sequências
                sc = self.score(s) #define o score da lista de index
                if sc > best_score: #se o score for superior ao melhor score
                    best_score = sc #melhor score iguala ao score
                    best_motif = s #melhor motif igual
                s = self.nextVertex(s) #procura o próximo vértice
        return best_motif

    def heuristicConsensus(self) -> list:
        """
        Método implementado para procurar as posições do motif nas duas primeiras sequências
        :return: lista de posições
        """
        mf = MotifFinding(self.motifSize, self.seqs[:2]) #faz procura exaustiva das primeiras sequências
        s = mf.exhaustiveSearch() #procura a posição inicial das duas sequências com o melhor score
        for a in range(2,len(self.seqs)): #percorre as duas primerias sequências na lista de sequências
            s.append(0)
            best_score = -1 #define o melhor score
            melhorPosition = 0 #define a melhor posição
            for b in range(self.seqSize(a) - self.motifSize + 1):
                s[a] = b #guarda b como o valor da posição de a na lista de sequências
                scoreatual = self.score(s) #calcula o score e define-o como valor atual
                if scoreatual > best_score: #se o score atual for superior ao melhor
                    best_score = scoreatual #guarda o atual como melhor
                    melhorPosition = b #retorna a melhor posição como a posição com o melhor score
                s[a] = melhorPosition #retorna o indice de a como a melhor posição
                # avalia a melhor posição para as sequências
        return s


    def heuristicStochastic(self) -> list:
        """
        Método que implementa o melhoramento do método heurístico.
        :return: lista de
        """
        s = [0] * len(self.seqs) # cria uma lista de zeros para os index das sequências
        for i in range(len(self.seqs)): #percorre a lista de sequências
            s[i] = randint(0, self.seqSize(i) - self.motifSize)
        best_score = self.score(s) #calcula o score
        improve = True #define o melhoramento como true
        while improve: #enquanto o melhoramento for verdadeiro
            motif = self.createMotifFromIndexes(s) #define os motifs a partir da lista de index
            motif.createPWM() #cria a PWM
            for i in range(len(self.seqs)): #percorre a lista de index no intervalo do número de sequências
                s[i] = motif.mostProbableSeq(self.seqs[i]) #calcula a sub_sequência
                # com maior probabilidade de ter o motif
            scr = self.score(s) #calculca os scores
            if scr > best_score: #altera o score se for superior ao melhor score
                best_score = scr
            else:
                improve = False
        return s

    def gibbs(self, num_iterations :int) -> list:
        """
        Método que implementa o algoritmo para testar a sequência introduzida,
        as sub-sequências e os scores correspondentes
        :param num_iterations: número de iterações
        :return: lista dos melhores scores
        """
        s = []
        for i in range(len(self.seqs)):
            s.append(randint(0, len(
                self.seqs[i]) - self.motifSize - 1))
        best_score = self.score(s)
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
            if score > best_score:
                best_score = score
                bests = list(s)
        return bests

    def roulette(self, f: list) -> int:
        """
        Método implementado para simular exemplos de uma rodade de uma roulette.
        :param f: lista de posições
        :return: valor escolhido
        """
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