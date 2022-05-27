# -*- coding: utf-8 -*-
"""
Package dos algoritmos implementados em aula
Algoritmos Avançados de Bioinformática
"""

"""
Class: Implementação de Algoritmos Evolucionários - População
"""

from indiv import Indiv, IndivInt
from random import random


class Popul:
    """
    Classe para implementar populações de indivíduos com representações binárias
    """

    def __init__(self, popsize: int, indsize: int, indivs = []) -> None:
        """
        :param popsize: número de indivíduos da população
        :param indsize: tamanho dos indivíduos
        :param indivs: indivíduos
        """
        self.popsize = popsize # número de indivíduos
        self.indsize = indsize # tamanho dos indivíduos
        if indivs:
            self.indivs = indivs
        else:
            self.initRandomPop()

    def getIndiv(self, index) -> list:
        """
        Método que vai buscar indivíduos pelo seu index
        :param index: lista de posições do indivíduo
        :return: lista de posições dos indivíduos
        """
        return self.indivs[index] # dá a posição do indivíduo

    def initRandomPop(self) -> None:
        """
        Método para gerar indivíduos de forma aleatória.
        """
        self.indivs = []
        for _ in range(self.popsize):
            indiv_i = Indiv(self.indsize, [])
            self.indivs.append(indiv_i) # adicionar os indivíduos à lista

    def getFitnesses(self, indivs = None) -> list:
        """
        Método que vai buscar todas as fitnesses dos indivíduos (valores de aptidão).
        :param indivs: indivíduos
        :return: lista de fitnesses dos indivíduos
        """
        fitnesses = [] # lista vazia para posterior append
        if not indivs:
            indivs = self.indivs
        for ind in indivs:
            fitnesses.append(ind.getFitness()) #
        return fitnesses

    def bestSolution(self):
        """
        Método que retorna a melhor solução dos indivíduos.
        :return: melhor solução dos indivíduos
        """
        return max(self.indivs)

    def bestFitness(self):
        """
        Método que retorna o melhor fitness dos indivíduos.
        :return: melhor fitness de uma solução de indivíduos
        """
        indv = self.bestSolution()
        return indv.getFitness()


    def selection(self, n, indivs = None) -> list:
        """
        Método que retorna uma lista com o mecanismo de seleção para reprodução.
        :param n: número de novos descendentes
        :param indivs: indivíduos
        :return:
        """
        res = []
        fitnesses = list(self.linscaling(self.getFitnesses(indivs))) # vai buscar fitnesses e faz a normalização
        for _ in range(n):
            sel = self.roulette(fitnesses)
            fitnesses[sel] = 0.0
            res.append(sel)
        return res

    def roulette(self, f: list) -> int:
        """
        Método roleta.
        :param f: lista
        :return: indivíduos com melhor aptidão
        """
        tot = sum(f)
        val = random()
        acum = 0.0
        ind = 0
        while acum < val:
            acum += (f[ind] / tot)
            ind += 1 # incrementar um indivíduo
        return ind-1

    def linscaling(self, fitnesses: list) -> list:
        """
        Método para fazer a normalização do valor de aptidão para [0, 1]
        :param fitnesses:
        :return: lista de fitnesses
        """
        mx = max(fitnesses) # máximo valor de aptidão
        mn = min(fitnesses) # mínimo valor de aptidão
        res = [] # lista de fitnesses para a normalização
        for f in fitnesses:
            val = (f-mn)/(mx-mn)
            res.append(val)
        return res

    def recombination(self, parents: list, noffspring: int) -> list:
        """
        Método de recombinação que usa cruzamento para criar novas soluções e aplica mutação a cada nova solução.
        :param parents: progenitores
        :param noffspring:
        :return: lista de descendência
        """
        offspring = []
        new_inds = 0
        while new_inds < noffspring: # enquanto a lista de novos indivíduos é menor que a da população existente,
            parent1 = self.indivs[parents[new_inds]] # vai buscar o progenitor 1
            parent2 = self.indivs[parents[new_inds+1]] # vai buscar o progenitor 1
            offsp1, offsp2 = parent1.crossover(parent2) # faz o cruzamento entre o progenitor 1 e 2
            offsp1.mutation() # aplica mutação a nova geração
            offsp2.mutation() # aplica mutação a nova geração
            offspring.append(offsp1) # append na lista de descendentes
            offspring.append(offsp2) # append na lista de descendentes
            new_inds += 2
        return offspring

    def reinsertion(self, offspring) -> None:
        """
        Método de reinserção.
        :param offspring: descendentes
        """
        tokeep = self.selection(self.popsize-len(offspring))
        ind_offsp = 0
        for i in range(self.popsize):
            if i not in tokeep:
                self.indivs[i] = offspring[ind_offsp]
                ind_offsp += 1


class PopulInt(Popul):
    """
    Extensão da classe Popul com implementação do método initRandomPop (override) para representações inteiras.
    """

    def __init__(self, popsize, indsize, ub, indivs=[]):
        """
        :param popsize: número de indivíduos da população
        :param indsize: tamanho dos indivíduos
        :param ub: upper bound
        :param indivs: indivíduos
        """
        self.ub = ub
        Popul.__init__(self, popsize, indsize, indivs)

    def initRandomPop(self):
        """
        Método para usar representações inteiras.
        """
        self.indivs = []
        for _ in range(self.popsize):
            indiv_i = IndivInt(self.indsize, [], 0, self.ub)
            self.indivs.append(indiv_i)